__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '3/4/16'

import os
import sys
import glob
from cmath import log
from datetime import datetime
from xml.dom.minidom import parse
import traceback
import shutil

from django.db import transaction
from django.contrib.gis.geos import WKTReader
from django.core.management.base import CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from dictionaries.models import (
    SpectralMode,
    SatelliteInstrument,
    OpticalProductProfile,
    InstrumentType,
    Satellite,
    Projection,
    SatelliteInstrumentGroup,
    Quality
)
from catalogue.models import OpticalProduct
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_date_time(date_stamp):
    """A helper method to create a date object from a CBERS time stamp.

    :param date_stamp: Date in this format:
    :type date_stamp: str

    Example format from CBERS:`2015-12-03 10:40:23`

    :returns: A python datetime object.
    :rtype: datetime
    """

    

    # print 'Parsing Date: %s\n' % date_stamp
    start_year = date_stamp[0:4]
    start_month = date_stamp[5:7]
    start_day = date_stamp[8:10]
    start_time = date_stamp[11:19]
    tokens = start_time.split(':')
    start_hour = tokens[0]
    start_minute = tokens[1]
    start_seconds = tokens[2]
    # print "%s-%s-%sT%s:%s:%s" % (
    #    start_year, start_month, start_day,
    #    start_hour, start_minute, start_seconds)
    parsed_date_time = datetime(
        int(start_year),
        int(start_month),
        int(start_day),
        int(start_hour),
        int(start_minute),
        int(start_seconds))
    return parsed_date_time



def get_geometry(log_message, dom):
    """Extract the bounding box as a geometry from the XML file.

    :param log_message: A log_message function used for user feedback.
    :type log_message: function

    :param dom: DOM Document containing the bounds of the scene.
    :type dom: Document

    :return: Geometry or None if elements are missing.
    """
    required_tags = [
        'TopLeftLatitude', 'TopLeftLongitude',
        'TopRightLatitude', 'TopRightLongitude',
        'BottomLeftLatitude', 'BottomLeftLongitude',
        'BottomRightLatitude', 'BottomRightLongitude'
    ]

    # Extract values and return None if any tag is missing
    try:
        values = {tag: dom.getElementsByTagName(tag)[0].firstChild.nodeValue for tag in required_tags}
    except (IndexError, AttributeError):
        log_message("Error: One or more required elements are missing in the XML.", 2)
        return None
    
    polygon = f"POLYGON(({values['TopLeftLongitude']} {values['TopLeftLatitude']}, " \
              f"{values['TopRightLongitude']} {values['TopRightLatitude']}, " \
              f"{values['BottomRightLongitude']} {values['BottomRightLatitude']}, " \
              f"{values['BottomLeftLongitude']} {values['BottomLeftLatitude']}, " \
              f"{values['TopLeftLongitude']} {values['TopLeftLatitude']}))"

    # myGeometry = WKTReader(polygon)
    reader = WKTReader()
    myGeometry = reader.read(polygon)
    return myGeometry


def get_dates(log_message, dom):
    """Get the start, mid scene and end dates.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A two-tuple of dates for the start, and mid scene
        respectively.
    :rtype: (datetime, datetime)
    """
    start_element = dom.getElementsByTagName('StartTime')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parse_date_time(start_date)
    log_message('Product Start Date: %s' % start_date, 2)

    product_date = dom.getElementsByTagName('ProduceTime')[0]
    center_date = product_date.firstChild.nodeValue
    center_date = parse_date_time(center_date)
    log_message('Product Date: %s' % center_date, 2)

    return start_date, center_date


def get_original_product_id(filename):
    # Get part of product name from filename
    # file name = CB04-WFI-81-135-20160118-L20000024812
    tokens = filename.split('-')
    product_name = ''.join(tokens)
    return product_name


def get_band_count(dom):
    try:
        band_count_data = dom.getElementsByTagName('bands')[0]
        band_count = band_count_data.firstChild.nodeValue
    except (IndexError, AttributeError):
        band_count = 0
    if band_count == 0:
        return 0
    elif len(band_count) == 1:
        return 1
    else:
        return len(eval(band_count))


def get_solar_azimuth_angle(dom):
    try:
        sun_azimuth = dom.getElementsByTagName('sunAzimuthElevation')[0]
        solar_azimuth = sun_azimuth.firstChild.nodeValue
        return solar_azimuth
    except (IndexError, AttributeError):
        return None

def get_scene_row(dom):
    try:
        scene_row = dom.getElementsByTagName('sceneRow')[0]
        row = scene_row.firstChild.nodeValue
        return row
    except (IndexError, AttributeError):
        return None


def get_scene_path(dom):
    try:
        scene_path = dom.getElementsByTagName('scenePath')[0]
        path = scene_path.firstChild.nodeValue
        return path
    except (IndexError, AttributeError):
        return None

def get_sensor_inclination():
    # The static value of sensor inclination angle
    # source http://www.cbers.inpe.br/ingles/satellites/orbit_cbers3_4.php
    return 98.5


def get_spatial_resolution_x(dom):
    try:
        spatial_resolution_data = dom.getElementsByTagName('pixelSpacing')[0]
        spatial_resolution = spatial_resolution_data.firstChild.nodeValue
        return spatial_resolution
    except (IndexError, AttributeError):
        return 0

def get_spatial_resolution_y(dom):
    try:
        spatial_resolution_data = dom.getElementsByTagName('pixelSpacing')[0]
        spatial_resolution = spatial_resolution_data.firstChild.nodeValue
        return spatial_resolution
    except (IndexError, AttributeError):
        return 0


def get_product_profile(log_message, product_id):
    """Find the product_profile for this record.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """

    print(f"PRODUCT ID {product_id}")
    # We need type, sensor and mission so that we can look up the
    # OpticalProductProfile that applies to this product
    sensor_value = product_id[4:7]
    mission_index = product_id[0:4]
    print(f"sensor_value {sensor_value}")
    print(f"mission_index {mission_index}")
    instrument_type = ""
    try:
        instrument_type = InstrumentType.objects.get(
            operator_abbreviation=sensor_value)  # e.g. MUX, P10
    except Exception as e:
        # print e.message
        raise Exception(f'ERROR: {e}')
    
    if mission_index == 'CB04':
        mission_value = 'CB04'
    elif mission_index == 'CB05':
        mission_value = 'CB05'
    else:
        raise Exception('Unknown mission in CBERS')
    satellite = Satellite.objects.get(abbreviation=mission_value)

    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception as e:
        print(e.message)
        raise e
    log_message('Satellite Instrument Group %s' %
                satellite_instrument_group, 2)
    try:
        satellite_instrument = SatelliteInstrument.objects.get(
            satellite_instrument_group=satellite_instrument_group)
    except Exception as e:
        print(e.message)
        raise e
    log_message('Satellite Instrument %s' % satellite_instrument, 2)

    try:
        spectral_modes = SpectralMode.objects.filter(
            instrument_type=instrument_type)
    except Exception as e:
        print(e.message)
        raise
    log_message('Spectral Modes %s' % spectral_modes, 2)

    try:
        product_profile = OpticalProductProfile.objects.get(
            satellite_instrument=satellite_instrument,
            spectral_mode__in=spectral_modes)
    except Exception as e:
        print(e.message)
        print('Searched for satellite instrument: %s and spectral modes %s' % (
            satellite_instrument, spectral_modes
        ))
        raise e
    log_message('Product Profile %s' % product_profile, 2)

    return product_profile


def get_radiometric_resolution(dom):
    """Get the radiometric resolution for the supplied product record.
    source = http://www.cbers.inpe.br/ingles/satellites/cameras_cbers3_4.php

    MUXCAM = 8 bits
    PANMUX = 8 bits
    IRSCAM = 8 bits
    WFICAM = 10 bits

    :param resolution_element: Dom Document containing the bounds of the scene.
    :type resolution_element: DOM document.

    :returns: The bit depth for the image.
    :rtype: int
    """
    try:
        get_sensor_id = dom.getElementsByTagName('sensorId')[0]
        sensor_id = get_sensor_id.firstChild.nodeValue
        # sensor_id : MUX, P10, P5M, WFI
        if sensor_id == 'MUX':
            return 8
        elif sensor_id == 'P10':
            return 8
        elif sensor_id == 'P5M':
            return 8
        elif sensor_id == 'WFI':
            return 10
        else:
            return 0
    except (IndexError, AttributeError):
        return 0

def get_projection(dom):
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.

    :param specific_parameters: Dom Document containing the bounds of the scene.
    :type specific_parameters: DOM document.

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """
    epsg_default_code = '32'
    default_zone = '1'  # Set your default zone value here (e.g., '01')
    location_code = '7'  # 6 for north and 7 for south

    try:
        get_zone = dom.getElementsByTagName('zone')[0]
        zone_value = get_zone.firstChild.nodeValue
        zone = zone_value[0:2]  # Extract the first two characters
    except (IndexError, AttributeError):
        # If the 'zone' tag is missing or has no value, use the default zone
        zone = default_zone

    epsg_code = epsg_default_code + location_code + zone

    try:
        projection = Projection.objects.get(epsg_code=epsg_code)
    except ObjectDoesNotExist:
        # Handle the case where the EPSG code is not found in the database
        print(f"Projection with EPSG code {epsg_code} does not exist.")
        return None  # Or provide a default projection if applicable

    return projection

def get_quality(dom):
    """Get the quality for this record - currently hard coded to unknown.

    :returns: A quality object fixed to 'unknown'.
    :rtype: Quality
    """
    try:
        overall_quality = dom.getElementsByTagName('overallQuality')[0]
        quality_xml = str(overall_quality.firstChild.nodeValue)
        quality = Quality.objects.get(name=quality_xml)
        return quality
    except (IndexError, AttributeError):
        return None

def ingest(
    test_only_flag=True,
    source_path="/home/web/catalogue/django_project/catalogue/tests/sample_files/CBERS/",
    verbosity_level=2,
    halt_on_error_flag=True,
    ignore_missing_thumbs=False
):
    """
    Ingest a collection of CBERS metadata folders.
    """

    def print_message(message, level=1):
        """Prints a message if verbosity level allows."""
        if verbosity_level >= level:
            print(message)

    print_message(f"""
    Running CBERS 04 Importer with options:
    Test Only Flag: {test_only_flag}
    Source Dir: {source_path}
    Verbosity Level: {verbosity_level}
    Halt on Error: {halt_on_error_flag}
    ------------------
    """, 2)

    # Track counts
    record_count, updated_record_count, created_record_count, failed_record_count = 0, 0, 0, 0
    ingestor_version = "CBERS 04 ingestor version 1.1"

    print_message(f"Scanning folders in {source_path}", 1)

    for xml_file in glob.glob(os.path.join(source_path, "*.[Xx][Mm][Ll]")):
        record_count += 1
        try:
            print_message("\n---------------", 2)
            print_message(f"Processing: {xml_file}", 2)

            file_name = os.path.splitext(os.path.basename(xml_file))[0]
            original_product_id = get_original_product_id(file_name)

            # Create a DOM document from the file
            dom = parse(xml_file)

            # Extract metadata
            geometry = get_geometry(print_message, dom)
            if geometry is None:
                print(f"Geometry Tags are missing in file {xml_file}")
                break
            start_date_time, center_date_time = get_dates(print_message, dom)
            projection = get_projection(dom)
            band_count = get_band_count(dom)
            row = get_scene_row(dom)
            path = get_scene_path(dom)
            solar_azimuth_angle = get_solar_azimuth_angle(dom)
            sensor_inclination = get_sensor_inclination()
            spatial_resolution_x = float(get_spatial_resolution_x(dom))
            spatial_resolution_y = float(get_spatial_resolution_y(dom))
            spatial_resolution = (spatial_resolution_x + spatial_resolution_y) / 2
            radiometric_resolution = get_radiometric_resolution(dom)
            quality = get_quality(dom)
            product_profile = get_product_profile(print_message, original_product_id)

            data = {
                "spatial_coverage": geometry,
                "radiometric_resolution": radiometric_resolution,
                "band_count": band_count,
                "original_product_id": original_product_id,
                "unique_product_id": original_product_id,
                "spatial_resolution_x": spatial_resolution_x,
                "spatial_resolution_y": spatial_resolution_y,
                "spatial_resolution": spatial_resolution,
                "product_profile": product_profile,
                "product_acquisition_start": start_date_time,
                "product_date": center_date_time,
                "sensor_inclination_angle": sensor_inclination,
                "solar_azimuth_angle": solar_azimuth_angle,
                "row": row,
                "path": path,
                "projection": projection,
                "quality": quality,
            }
            print_message(f"Extracted Data: {data}", 3)

            # Try to update or create record
            time_stamp = datetime.today().strftime("%Y-%m-%d")
            new_record_flag = False
            update_mode = True

            try:
                product = OpticalProduct.objects.get(original_product_id=original_product_id).getConcreteInstance()
                print_message(f"Already in catalogue: updating {original_product_id}.", 2)
                message = product.ingestion_log + f"\n{time_stamp} : {ingestor_version} - updating record"
                data["ingestion_log"] = message
                product.__dict__.update(data)
            except OpticalProduct.DoesNotExist:
                print_message("Not in catalogue: creating.", 2)
                update_mode = False
                message = f"{time_stamp} : {ingestor_version} - creating record"
                data["ingestion_log"] = message
                product = OpticalProduct(**data)
                new_record_flag = True
            except Exception as e:
                print("Unexpected error while checking record existence:", getattr(e, "message", str(e)))
                traceback.print_exc()
                continue

            # Save product and handle thumbnails
            print_message("Saving product and setting thumbnail", 2)
            try:
                product.save()
                if update_mode:
                    updated_record_count += 1
                else:
                    created_record_count += 1

                if not test_only_flag:
                    thumbs_folder = os.path.join(settings.THUMBS_ROOT, product.thumbnailDirectory())
                    os.makedirs(thumbs_folder, exist_ok=True)

                    jpeg_path = xml_file.replace(".XML", "-THUMB.JPG")
                    if os.path.exists(jpeg_path):
                        new_name = f"{product.original_product_id}.JPG"
                        shutil.copyfile(jpeg_path, os.path.join(thumbs_folder, new_name))
                        print_message(f"Thumbnail saved: {new_name}", 2)
                    elif not ignore_missing_thumbs:
                        raise FileNotFoundError(f"Missing thumbnail: {jpeg_path}")

                if new_record_flag:
                    print_message(f"Product {record_count} imported.", 2)
                else:
                    print_message(f"Product {updated_record_count} updated.", 2)
            except Exception as e:
                print("Error saving product:", getattr(e, "message", str(e)))
                traceback.print_exc()
                raise CommandError(f"Cannot import: {e}")

            # Commit or rollback
            if test_only_flag:
                transaction.rollback()
                print_message(f"Testing only: Transaction rollback for {file_name}.", 1)
            else:
                transaction.commit()
                print_message(f"Imported scene: {file_name}", 1)

        except Exception as e:
            print_message(f"Record import failed: {file_name}", 1)
            print("Error details:", getattr(e, "message", str(e)))
            traceback.print_exc()
            failed_record_count += 1
            if halt_on_error_flag:
                break
            continue

    # Summary
    print("\n===============================")
    print(f"Products Processed: {record_count}")
    print(f"Products Updated: {updated_record_count}")
    print(f"Products Imported: {created_record_count}")
    print(f"Products Failed: {failed_record_count}")
    print("===============================")