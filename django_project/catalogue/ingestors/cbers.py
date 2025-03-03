import os
import glob
import shutil
import traceback
import logging
from datetime import datetime
from xml.dom.minidom import parse

from django.db import transaction
from django.core.management.base import CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django.contrib.gis.geos import WKTReader

from dictionaries.models import (
    SpectralMode,
    SatelliteInstrument,
    OpticalProductProfile,
    InstrumentType,
    Satellite,
    Projection,
    SatelliteInstrumentGroup,
    Quality,
)
from catalogue.models import OpticalProduct

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_date_time(date_str):
    """
    Create a datetime object from a CBERS-style timestamp.

    Example: "2015-12-03 10:40:23"
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.exception(f"Error parsing date: {date_str}")
        return None


def get_dom_element(dom, tag_name, default=None):
    """
    Safely fetch the text value of the first DOM element with the given tag.
    Returns `default` if element is missing or empty.
    """
    try:
        element = dom.getElementsByTagName(tag_name)[0]
        return element.firstChild.nodeValue.strip()
    except (IndexError, AttributeError):
        return default


def get_geometry(dom):
    """
    Extract the bounding box as a geometry from the XML file.

    Return the WKT geometry or None if elements are missing.
    """
    required_tags = [
        'TopLeftLatitude', 'TopLeftLongitude',
        'TopRightLatitude', 'TopRightLongitude',
        'BottomLeftLatitude', 'BottomLeftLongitude',
        'BottomRightLatitude', 'BottomRightLongitude'
    ]

    values = {}
    for tag in required_tags:
        val = get_dom_element(dom, tag)
        if val is None:
            logger.error(f"Missing geometry tag: {tag}")
            return None
        values[tag] = val

    # Construct a WKT polygon from bounding coordinates
    polygon = (
        f"POLYGON(({values['TopLeftLongitude']} {values['TopLeftLatitude']}, "
        f"{values['TopRightLongitude']} {values['TopRightLatitude']}, "
        f"{values['BottomRightLongitude']} {values['BottomRightLatitude']}, "
        f"{values['BottomLeftLongitude']} {values['BottomLeftLatitude']}, "
        f"{values['TopLeftLongitude']} {values['TopLeftLatitude']}))"
    )

    reader = WKTReader()
    return reader.read(polygon)


def get_dates(dom):
    """
    Get the start, mid scene (a.k.a. product) dates from the DOM.
    Returns a tuple (start_date, product_date).
    """
    start_str = get_dom_element(dom, 'StartTime')
    product_str = get_dom_element(dom, 'ProduceTime')

    if not start_str or not product_str:
        logger.error("Missing required date fields: StartTime or ProduceTime")
        return None, None

    start_dt = parse_date_time(start_str)
    product_dt = parse_date_time(product_str)

    return start_dt, product_dt


def get_original_product_id(filename):
    """
    Build the product name from the filename.
    Example: "CB04-WFI-81-135-20160118-L20000024812.xml" => "CB04WFI8113520160118L20000024812"
    """
    base = os.path.splitext(os.path.basename(filename))[0]
    return "".join(base.split("-"))


def get_band_count(dom):
    """
    Retrieve the band count from the DOM. If the 'bands' node is absent or has
    no content, returns 0. If it's a list representation, uses length of eval.
    """
    bands_str = get_dom_element(dom, 'bands')
    if not bands_str:
        return 0

    # If the 'bands' tag looks like a python list, e.g., "[1,2,3]"
    try:
        band_list = eval(bands_str)
        return len(band_list)
    except Exception:
        # If single-digit or unexpected
        return 1 if len(bands_str) == 1 else 0


def get_sensor_inclination():
    """
    Returns the static sensor inclination angle for CBERS satellites.
    Source: http://www.cbers.inpe.br/ingles/satellites/orbit_cbers3_4.php
    """
    return 98.5


def get_spatial_resolution(dom):
    """
    Returns the average of spatial resolution from 'pixelSpacing' tag
    (assuming X and Y are the same or missing).
    """
    spacing_str = get_dom_element(dom, 'pixelSpacing')
    if spacing_str is None:
        return 0.0, 0.0, 0.0

    try:
        spatial_val = float(spacing_str)
    except ValueError:
        spatial_val = 0.0

    # For X, Y, and average. You can adapt if they're truly different in the future.
    return spatial_val, spatial_val, spatial_val


def get_product_profile(product_id):
    """
    Find or create the product_profile for the record using the product_id.

    :returns: OpticalProductProfile or None on failure.
    """
    # Example:
    # product_id = 'CB04WFI...'
    sensor_value = product_id[4:7]
    mission_index = product_id[:4]

    # Create or get the instrument type
    instrument_type, _ = InstrumentType.objects.get_or_create(
        operator_abbreviation=sensor_value,
        defaults={'name': sensor_value}
    )

    # Check satellite mission
    if mission_index in ('CB04', 'CB05'):
        mission_value = mission_index
    else:
        logger.error(f"Unknown mission index: {mission_index}")
        return None

    # Create/get the Satellite
    satellite, _ = Satellite.objects.get_or_create(
        abbreviation=mission_value,
        defaults={'name': mission_value}
    )

    # Create/get SatelliteInstrumentGroup
    group, _ = SatelliteInstrumentGroup.objects.get_or_create(
        satellite=satellite, instrument_type=instrument_type
    )

    # Create/get SatelliteInstrument
    try:
        instrument, _ = SatelliteInstrument.objects.get_or_create(
            satellite_instrument_group=group
        )
    except Exception as e:
        logger.exception("Error creating or fetching SatelliteInstrument")
        return None

    # Try to match spectral modes
    spectral_modes = SpectralMode.objects.filter(instrument_type=instrument_type)
    profiles = OpticalProductProfile.objects.filter(satellite_instrument=instrument)
    if spectral_modes.exists():
        profiles = profiles.filter(spectral_mode__in=spectral_modes)

    if not profiles.exists():
        # Create new if no profile found
        if spectral_modes.exists():
            for smode in spectral_modes:
                OpticalProductProfile.objects.get_or_create(
                    satellite_instrument=instrument,
                    spectral_mode=smode
                )
        else:
            OpticalProductProfile.objects.get_or_create(satellite_instrument=instrument)
        # Re-query after creation
        profiles = OpticalProductProfile.objects.filter(satellite_instrument=instrument)

    return profiles.first() if profiles.exists() else None


def get_radiometric_resolution(dom):
    """
    Determine the radiometric resolution from the sensor ID.

    MUXCAM  = 8 bits
    PANMUX  = 8 bits
    IRSCAM  = 8 bits
    WFICAM  = 10 bits

    Returns int bit depth or 0 if unknown.
    """
    sensor_id = get_dom_element(dom, 'sensorId')
    sensor_bits_map = {
        'MUX': 8,
        'P10': 8,
        'P5M': 8,
        'WFI': 10
    }
    return sensor_bits_map.get(sensor_id, 0)


def get_projection(dom):
    """
    Returns the Projection model for the computed EPSG code.

    The logic is to combine the base '32', a location code '7' (for south)
    and the two-digit zone from 'zone' tag.
    """
    epsg_default_code = '32'
    location_code = '7'  # 6 for north, 7 for south
    default_zone = '01'  # fallback if 'zone' is missing or invalid

    zone_val = get_dom_element(dom, 'zone', default=default_zone)
    zone = zone_val[:2] if len(zone_val) >= 2 else default_zone

    epsg_code = epsg_default_code + location_code + zone
    try:
        return Projection.objects.get(epsg_code=epsg_code)
    except ObjectDoesNotExist:
        logger.warning(f"Projection with EPSG code {epsg_code} does not exist.")
        return None


def get_quality(dom):
    """
    Return the Quality object from the 'overallQuality' tag, 
    or None if not found. 
    """
    quality_name = get_dom_element(dom, 'overallQuality')
    if not quality_name:
        return None
    try:
        return Quality.objects.get(name=quality_name)
    except ObjectDoesNotExist:
        logger.warning(f"Quality object '{quality_name}' not found.")
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

    :param test_only_flag: If True, rolls back transactions (dry run).
    :param source_path: The directory containing CBERS XML files.
    :param verbosity_level: Log verbosity threshold.
    :param halt_on_error_flag: If True, stops on first error.
    :param ignore_missing_thumbs: If True, do not treat missing thumbnails as errors.
    """
    logger.info(
        "Running CBERS 04 Importer with options:\n"
        f"  Test Only: {test_only_flag}\n"
        f"  Source Dir: {source_path}\n"
        f"  Verbosity: {verbosity_level}\n"
        f"  Halt on Error: {halt_on_error_flag}\n"
        "------------------------------------"
    )

    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    ingestor_version = "CBERS 04 ingestor version 1.1"

    xml_files = glob.glob(os.path.join(source_path, "*.[Xx][Mm][Ll]"))
    logger.info(f"Found {len(xml_files)} XML files in {source_path}.")

    for xml_file in xml_files:
        record_count += 1
        file_name = os.path.basename(xml_file)
        logger.info(f"\nProcessing file #{record_count}: {file_name}")

        try:
            original_product_id = get_original_product_id(xml_file)
            dom = parse(xml_file)

            # Extract metadata
            geometry = get_geometry(dom)
            if not geometry:
                logger.error(f"Missing geometry in {xml_file}")
                failed_record_count += 1
                if halt_on_error_flag:
                    break
                continue

            start_dt, center_dt = get_dates(dom)
            band_count = get_band_count(dom)
            row = get_dom_element(dom, 'sceneRow')
            path = get_dom_element(dom, 'scenePath')
            solar_azimuth_angle = get_dom_element(dom, 'sunAzimuthElevation')
            sensor_inclination = get_sensor_inclination()
            spatial_x, spatial_y, spatial_avg = get_spatial_resolution(dom)
            radiometric_resolution = get_radiometric_resolution(dom)
            quality = get_quality(dom)
            projection = get_projection(dom)
            product_profile = get_product_profile(original_product_id)

            data = {
                "spatial_coverage": geometry,
                "radiometric_resolution": radiometric_resolution,
                "band_count": band_count,
                "original_product_id": original_product_id,
                "unique_product_id": original_product_id,
                "spatial_resolution_x": spatial_x,
                "spatial_resolution_y": spatial_y,
                "spatial_resolution": spatial_avg,
                "product_profile": product_profile,
                "product_acquisition_start": start_dt,
                "product_date": center_dt,
                "sensor_inclination_angle": sensor_inclination,
                "solar_azimuth_angle": solar_azimuth_angle,
                "row": row,
                "path": path,
                "projection": projection,
                "quality": quality,
            }

            # Try to find existing product
            time_stamp = datetime.today().strftime("%Y-%m-%d")
            update_mode = True
            try:
                product = (OpticalProduct.objects
                           .get(original_product_id=original_product_id)
                           .getConcreteInstance())
                logger.info(f"Updating existing product: {original_product_id}")
                msg = product.ingestion_log + f"\n{time_stamp} : {ingestor_version} - updating record"
                data["ingestion_log"] = msg
                # Update in-place
                for key, value in data.items():
                    setattr(product, key, value)
            except OpticalProduct.DoesNotExist:
                logger.info(f"Creating new product: {original_product_id}")
                update_mode = False
                msg = f"{time_stamp} : {ingestor_version} - creating record"
                data["ingestion_log"] = msg
                product = OpticalProduct(**data)
            except Exception as e:
                logger.exception("Unexpected error checking product existence.")
                failed_record_count += 1
                if halt_on_error_flag:
                    break
                continue

            # Save product
            try:
                product.save()
                if update_mode:
                    updated_record_count += 1
                else:
                    created_record_count += 1

                # Handle thumbnail
                if not test_only_flag:
                    thumbs_folder = os.path.join(
                        settings.THUMBS_ROOT,
                        product.thumbnailDirectory()
                    )
                    os.makedirs(thumbs_folder, exist_ok=True)

                    jpeg_path = xml_file.replace(".XML", "-THUMB.JPG")
                    if os.path.exists(jpeg_path):
                        new_name = f"{product.original_product_id}.JPG"
                        shutil.copyfile(jpeg_path, os.path.join(thumbs_folder, new_name))
                        logger.info(f"Thumbnail saved: {new_name}")
                    elif not ignore_missing_thumbs:
                        raise FileNotFoundError(f"Missing thumbnail for {product.original_product_id}")

                # Commit or rollback
                if test_only_flag:
                    transaction.rollback()
                    logger.info(f"Test only: rolled back transaction for {file_name}")
                else:
                    transaction.commit()
                    logger.info(f"Successfully {'updated' if update_mode else 'created'} product: {file_name}")

            except Exception as e:
                logger.exception(f"Error saving product {original_product_id}")
                transaction.rollback()
                failed_record_count += 1
                if halt_on_error_flag:
                    break

        except Exception as e:
            logger.exception(f"Failed to process {file_name}")
            failed_record_count += 1
            if halt_on_error_flag:
                break

    print("\n===============================")
    print(f"Products Processed: {record_count}")
    print(f"Products Updated: {updated_record_count}")
    print(f"Products Imported: {created_record_count}")
    print(f"Products Failed: {failed_record_count}")
    print("===============================")
