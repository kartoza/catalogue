__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '4/28/16'


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


def parse_date_time(date_stamp):
    """A helper method to create a date object from a SPOT time stamp.

    :param date_stamp: Date in this format:
    :type date_stamp: str

    Example format from SPOT:`1989-05-03T07:30:05.000`

    :returns: A python datetime object.
    :rtype: datetime
    """
    #print 'Parsing Date: %s\n' % date_stamp
    start_year = date_stamp[0:4]
    start_month = date_stamp[5:7]
    start_day = date_stamp[8:10]
    start_time = date_stamp[11:19]
    tokens = start_time.split(':')
    start_hour = tokens[0]
    start_minute = tokens[1]
    start_seconds = tokens[2]
    #print "%s-%s-%sT%s:%s:%s" % (
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
    """Extract the bounding box as a geometry from the xml file.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: DOM Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: geoemtry
    """
    geo_area = dom.getElementsByTagName('Programming_Geo_Area')[0]
    points = geo_area.getElementsByTagName('CORNER')
    polygon = 'POLYGON(('
    is_first = True
    first_longitude = None
    first_latitude = None
    for point in points:
        latitude = point.getElementsByTagName('LATITUDE')[0]
        latitude = latitude.firstChild.nodeValue
        longitude = point.getElementsByTagName('LONGITUDE')[0]
        longitude = longitude.firstChild.nodeValue
        if not is_first:
            polygon += ','
        else:
            first_latitude = latitude
            first_longitude = longitude
            is_first = False
        polygon += '%s %s' % (longitude, latitude)
    polygon += ',%s %s))' % (first_longitude, first_latitude)
    log_message(polygon, 2)

    # Now make a geometry object
    myReader = WKTReader()
    myGeometry = myReader.read(polygon)
    #log_message('Geometry: %s' % myGeometry, 2)
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
    start_date = dom.getElementsByTagName('UTC_Acquisition_Range')[0]
    start_element = start_date.getElementsByTagName('START')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parse_date_time(start_date)
    log_message('Product Start Date: %s' % start_date, 2)

    production_date = dom.getElementsByTagName('Production')[0]
    product_date = production_date.getElementsByTagName('DATASET_PRODUCTION_DATE')[0]
    center_date = product_date.firstChild.nodeValue
    center_date = parse_date_time(center_date)
    log_message('Product Date: %s' % center_date, 2)

    return start_date, center_date

def get_band_count():
    return 5  # static value based on client information

def get_orbit_number(dom):
    value_orbit_number = dom.getElementsByTagName('ORBIT_NUMBER')[0]
    orbit_number = value_orbit_number.firstChild.nodeValue
    return orbit_number

def get_original_product_id(dom):
    dataset_name = dom.getElementsByTagName('DATASET_NAME')[0]
    product_name_full = dataset_name.firstChild.nodeValue
    tokens = product_name_full.split('_')
    # change according to Maite's explanation in kartoza/catalogue#496, constant always THUMBNAIL
    # if tokens[1] == "SPOT6":
    #    constant = "S6"
    # else: constant = "S7"
    constant = "THUMBNAIL_"
    # change according to Maite's explanation in kartoza/catalogue#496
    # product_name = constant + tokens[0] + tokens[2] + tokens[3]
    product_name = constant + tokens[2]
    return product_name

def get_spatial_resolution_x():
    return 1.5

def get_spatial_resolution_y():
    return 1.5

def get_product_profile(log_message, dom):
    """Find the product_profile for this record.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """
    # We need type, sensor and mission so that we can look up the
    # OpticalProductProfile that applies to this product
    sensor_value = "NAOMI"
    mission_index = dom.getElementsByTagName('PLATFORM_SERIAL_NUMBER')[0]
    mission_index_value = mission_index.firstChild.nodeValue

    try:
        instrument_type = InstrumentType.objects.get(
            operator_abbreviation=sensor_value)  # e.g. OLI_TIRS
    except Exception as e:
        #print e.message
        raise e
    log_message('Instrument Type %s' % instrument_type, 2)

    if mission_index_value == '6':
        mission_value = 'S6'
    elif mission_index_value == '7':
        mission_value = 'S7'
    else:
        raise Exception('Unknown mission in SPOT')
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


def get_radiometric_resolution():
    """Get the radiometric resolution for the supplied product record."""
    return 12  # static value based on client information

def get_projection():
    # If projection not found default to WGS84
    projection = Projection.objects.get(epsg_code=4326)
    return projection


def get_quality():
    """Get the quality for this record - currently hard coded to unknown.

    :returns: A quality object fixed to 'unknown'.
    :rtype: Quality
    """
    quality = Quality.objects.get(name='Unknown')
    return quality


def ingest(
        test_only_flag=True,
        source_path=(
            '/home/web/catalogue/django_project/catalogue/tests/sample_files/'
            'SPOT/'),
        verbosity_level=2,
        halt_on_error_flag=True,
        ignore_missing_thumbs=False):
    """
    Ingest a collection of SPOT metadata folders.

    :param test_only_flag: Whether to do a dummy run ( database will not be
        updated. Default False.
    :type test_only_flag: bool

    :param source_path: A SPOT created spot6/7 metadata xml file and thumbnail.
    :type source_path: str

    :param verbosity_level: How verbose the logging output should be. 0-2
        where 2 is very very very very verbose! Default is 1.
    :type verbosity_level: int

    :param halt_on_error_flag: Whather we should stop processing when the first
        error is encountered. Default is True.
    :type halt_on_error_flag: bool

    :param ignore_missing_thumbs: Whether we should raise an error
        if we find we are missing a thumbnails. Default is False.
    :type ignore_missing_thumbs: bool
    """
    def log_message(message, level=1):
        """Log a message for a given leven.

        :param message: A message.
        :param level: A log level.
        """
        if verbosity_level >= level:
            print(message)

    log_message((
        'Running SPOT 6/7 Importer with these options:\n'
        'Test Only Flag: %s\n'
        'Source Dir: %s\n'
        'Verbosity Level: %s\n'
        'Halt on error: %s\n'
        '------------------')
        % (test_only_flag, source_path, verbosity_level,
           halt_on_error_flag), 2)

    # Scan the source folder and look for any sub-folders
    # The sub-folder names should be e.g.
    # L5-_TM-_HRF_SAM-_0176_00_0078_00_920606_080254_L0Ra_UTM34S
    log_message('Scanning folders in %s' % source_path, 1)
    # Loop through each folder found

    ingestor_version = 'SPOT ingestor version 1.1'
    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    log_message('Starting directory scan...', 2)

    for myFolder in glob.glob(os.path.join(source_path, '*')):
        record_count += 1
        try:
            log_message('', 2)
            log_message('---------------', 2)
            # Get the folder name
            product_folder = os.path.split(myFolder)[-1]
            log_message(product_folder, 2)

            # Find the first and only xml file in the folder
            search_path = os.path.join(str(myFolder), '*.xml')
            log_message(search_path, 2)
            xml_file = glob.glob(search_path)[0]
            log_message(xml_file, 2)

            # Create a DOM document from the file
            dom = parse(xml_file)
            #
            # First grab all the generic properties that any spot will have...
            geometry = get_geometry(log_message, dom)
            start_date_time, center_date_time = get_dates(
                log_message, dom)
            # projection for GenericProduct
            projection = get_projection()
            original_product_id = get_original_product_id(dom)
            # Band count for GenericImageryProduct
            band_count = get_band_count()
            orbit_number = get_orbit_number(dom)
            # # Spatial resolution x for GenericImageryProduct
            spatial_resolution_x = float(get_spatial_resolution_x())
            # # Spatial resolution y for GenericImageryProduct
            spatial_resolution_y = float(
                get_spatial_resolution_y())
            log_message('Spatial resolution y: %s' % spatial_resolution_y, 2)
            #
            # # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
            spatial_resolution = (spatial_resolution_x + spatial_resolution_y) / 2
            log_message('Spatial resolution: %s' % spatial_resolution, 2)
            radiometric_resolution = get_radiometric_resolution()
            log_message('Radiometric resolution: %s' % radiometric_resolution, 2)
            quality = get_quality()
            # ProductProfile for OpticalProduct
            product_profile = get_product_profile(log_message, dom)
            # Get the original text file metadata
            metadata_file = file(xml_file, 'rt')
            metadata = metadata_file.readlines()
            metadata_file.close()
            log_message('Metadata retrieved', 2)

            unique_product_id = original_product_id
            # Check if there is already a matching product based
            # on original_product_id

            # Do the ingestion here...
            data = {
                'metadata': metadata,
                'spatial_coverage': geometry,
                'radiometric_resolution': radiometric_resolution,
                'band_count': band_count,
                'original_product_id': original_product_id,
                'unique_product_id': unique_product_id,
                'spatial_resolution_x': spatial_resolution_x,
                'spatial_resolution_y': spatial_resolution_y,
                'spatial_resolution': spatial_resolution,
                'product_profile': product_profile,
                'product_acquisition_start': start_date_time,
                'product_date': center_date_time,
                'orbit_number': orbit_number,
                'projection': projection,
                'quality': quality
            }
            log_message(data, 3)
            # Check if it's already in catalogue:
            try:
                today = datetime.today()
                time_stamp = today.strftime("%Y-%m-%d")
                log_message('Time Stamp: %s' % time_stamp, 2)
            except Exception as e:
                print(e.message)

            update_mode = True
            try:
                log_message('Trying to update')
                #original_product_id is not necessarily unique
                #so we use product_id
                product = OpticalProduct.objects.get(
                    original_product_id=original_product_id
                ).getConcreteInstance()
                log_message(('Already in catalogue: updating %s.'
                            % original_product_id), 2)
                new_record_flag = False
                message = product.ingestion_log
                message += '\n'
                message += '%s : %s - updating record' % (
                    time_stamp, ingestor_version)
                data['ingestion_log'] = message
                product.__dict__.update(data)
            except ObjectDoesNotExist:
                log_message('Not in catalogue: creating.', 2)
                update_mode = False
                message = '%s : %s - creating record' % (
                    time_stamp, ingestor_version)
                data['ingestion_log'] = message
                try:
                    product = OpticalProduct(**data)
                    log_message('Product: %s' % product)

                except Exception as e:
                    log_message(e.message, 2)

                new_record_flag = True
            except Exception as e:
                print(e.message)

            log_message('Saving product and setting thumb', 2)
            try:
                product.save()
                if update_mode:
                    updated_record_count += 1
                else:
                    created_record_count += 1

                    if test_only_flag:
                        log_message('Testing: image not saved.', 2)
                        pass
                    else:
                        # Store thumbnail
                        thumbs_folder = os.path.join(
                            settings.THUMBS_ROOT,
                            product.thumbnailDirectory())
                        try:
                            os.makedirs(thumbs_folder)
                        except OSError:
                            # TODO: check for creation failure rather than
                            # attempt to  recreate an existing dir
                            pass

                        jpeg_path = os.path.join(str(myFolder))
                        jpeg_path = jpeg_path.replace(".XML", "-THUMB.JPG")

                        if jpeg_path:
                            new_name = '%s.JPG' % product.original_product_id
                            shutil.copyfile(
                                os.path.join(jpeg_path, new_name),
                                os.path.join(thumbs_folder,new_name))
                            print(new_name)
                        else:
                            raise Exception('Missing thumbnail in %s' % jpeg_path)

                if new_record_flag:
                    log_message('Product %s imported.' % record_count, 2)
                    pass
                else:
                    log_message('Product %s updated.' % updated_record_count, 2)
                    pass
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                raise CommandError('Cannot import: %s' % e)

            if test_only_flag:
                transaction.rollback()
                log_message('Imported scene : %s' % product_folder, 1)
                log_message('Testing only: transaction rollback.', 1)
            else:
                transaction.commit()
                log_message('Imported scene : %s' % product_folder, 1)
        except Exception as e:
            log_message('Record import failed. AAAAAAARGH! : %s' %
                        product_folder, 1)
            failed_record_count += 1
            if halt_on_error_flag:
                print(e.message)
                break
            else:
                continue

    # To decide: should we remove ingested product folders?

    print('===============================')
    print('Products processed : %s ' % record_count)
    print('Products updated : %s ' % updated_record_count)
    print('Products imported : %s ' % created_record_count)
    print('Products failed to import : %s ' % failed_record_count)
    print('===============================')
