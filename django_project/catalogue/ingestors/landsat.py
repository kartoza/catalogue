# coding=utf-8
"""Landsat 8 ingestor script"""

__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '3/3/16'

import os
import sys
import glob
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
    """A helper method to create a date object from a landsat time stamp.

    :param date_stamp: Date in this format:
    :type date_stamp: str

    Example format from Landsat:`1989-05-03T07:30:05.000` 20150303T10:35:18

    :returns: A python datetime object.
    :rtype: datetime
    """
    # print 'Parsing Date: %s\n' % theDate
    start_year = date_stamp[0:4]
    start_month = date_stamp[4:6]
    start_day = date_stamp[6:8]
    start_time = date_stamp[9:17]
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


def get_geometry(dom):
    """Extract the bounding box as a geometry from the xml file.
    :param dom: DOM Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: geoemtry
    """
    geo_area = dom.getElementsByTagName('SCENEDATAEXTENT')[0]

    ul_lat_value = geo_area.getElementsByTagName('UL_LAT')[0]
    ul_lat = ul_lat_value.firstChild.nodeValue

    ul_long_value = geo_area.getElementsByTagName('UL_LONG')[0]
    ul_long = ul_long_value.firstChild.nodeValue

    ur_lat_value = geo_area.getElementsByTagName('UR_LAT')[0]
    ur_lat = ur_lat_value.firstChild.nodeValue

    ur_long_value = geo_area.getElementsByTagName('UR_LONG')[0]
    ur_long = ur_long_value.firstChild.nodeValue

    lr_lat_value = geo_area.getElementsByTagName('LR_LAT')[0]
    lr_lat = lr_lat_value.firstChild.nodeValue

    lr_long_value = geo_area.getElementsByTagName('LR_LONG')[0]
    lr_long = lr_long_value.firstChild.nodeValue

    ll_lat_value = geo_area.getElementsByTagName('LL_LAT')[0]
    ll_lat = ll_lat_value.firstChild.nodeValue

    ll_long_value = geo_area.getElementsByTagName('LL_LONG')[0]
    ll_long = ll_long_value.firstChild.nodeValue

    polygon = 'POLYGON ((' ' %s %s, %s %s, %s %s, %s %s, %s %s' '))' % (
        ul_long, ul_lat,
        ur_long, ur_lat,
        lr_long, lr_lat,
        ll_long, ll_lat,
        ul_long, ul_lat,
    )

    polygon_geometry = WKTReader().read(polygon)
    return polygon_geometry


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
    start_date = dom.getElementsByTagName('CITATION')[0]
    start_element = start_date.getElementsByTagName('DATE')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parse_date_time(start_date)
    log_message('Product Start Date: %s' % start_date, 2)

    production_date = dom.getElementsByTagName('CITATION')[0]
    product_date = production_date.getElementsByTagName('DATE')[0]
    center_date = product_date.firstChild.nodeValue
    center_date = parse_date_time(center_date)
    log_message('Product Date: %s' % center_date, 2)

    return start_date, center_date


def get_band_count():
    # band_count = dom.getElementsByTagName('NBANDS')[0]
    # count = band_count.firstChild.nodeValue
    return 10


def get_original_product_id(dom, filename):
    constant = 'JSA00'
    # Get part of product name from dom
    dataset_name = dom.getElementsByTagName('ALTERNATETITLE')[0]
    product_name_full = dataset_name.firstChild.nodeValue
    tokens = product_name_full.split(' ')
    product_name_dom = tokens[2]

    # Get part of product name from filename.
    product_name_file = filename[0:3]
    product_name = product_name_file + product_name_dom + constant

    return product_name


def get_spatial_resolution_x(filename):
    """Spacial resolution
    :param filename: For getting version from filename
    """
    product_name_file = filename[2]
    if product_name_file == '7':
        return 15
    else:
        return 30


def get_spatial_resolution_y(filename):
    """Spacial resolution
    :param filename: For getting version from filename
    """
    product_name_file = filename[2]
    if product_name_file == '7':
        return 15
    else:
        return 30


def get_mission_value(filename):
    if 'L07' in filename or 'LC07' in filename:
        return 'L7'
    else:
        return 'L8'


def get_product_profile(log_message, dom):
    """Find the product_profile for this record.

    It can be that one or more spectral modes are associated with a product.
    For example Landsat8 might have Pan (1 band), Multispectral (8 bands) and
    Thermal (2 bands) modes associated with a single product (total 11 bands).

    Because of this there is a many to many relationship on
    OpticalProductProfile and to get a specific OpticalProductProfile record
    we would need to know the satellite instrument and all the associated
    spectral modes to that profile record.

    We use the following elements to reverse engineer what the
    OpticalProductProfile is::

        <feature key="type">HRF</feature>
        <feature key="sensor">OLI_TIRS</feature>
        <feature key="mission">LANDSAT8</feature>

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """
    # We need type, sensor and mission so that we can look up the
    # OpticalProductProfile that applies to this product
    sensor_value_landsat = dom.getElementsByTagName('INSTRUMENTNAME')[0]
    sensor_value = sensor_value_landsat.firstChild.nodeValue
    mission_index = dom.getElementsByTagName('PLATFORMNAME')[0]
    mission_index_value = mission_index.firstChild.nodeValue

    try:
        instrument_type = InstrumentType.objects.get(
            operator_abbreviation=sensor_value)  # e.g. OLI_TIRS
    except Exception, e:
        # print e.message
        raise e
    log_message('Instrument Type %s' % instrument_type, 2)

    if mission_index_value == 'Landsat-7':
        mission_value = 'L7'
    elif mission_index_value == 'Landsat-8':
        mission_value = 'L8'
    else:
        raise Exception('Unknown mission in Landsat')
    satellite = Satellite.objects.get(abbreviation=mission_value)

    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise e
    log_message('Satellite Instrument Group %s' %
                satellite_instrument_group, 2)

    # Note that in some cases e.g. Landsat you may get more that one instrument
    # groups matched. When the time comes you will need to add more filtering
    # rules to ensure that you end up with only one instrument group.
    # For the mean time, we can assume that Landsat will return only one.

    try:
        satellite_instrument = SatelliteInstrument.objects.get(
            satellite_instrument_group=satellite_instrument_group)
    except Exception, e:
        print e.message
        raise e
    log_message('Satellite Instrument %s' % satellite_instrument, 2)

    try:
        spectral_modes = SpectralMode.objects.filter(
            instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise
    log_message('Spectral Modes %s' % spectral_modes, 2)

    try:
        product_profile = OpticalProductProfile.objects.get(
            satellite_instrument=satellite_instrument,
            spectral_mode__in=spectral_modes)
    except Exception, e:
        print e.message
        print 'Searched for satellite instrument: %s and spectral modes %s' % (
            satellite_instrument, spectral_modes
        )
        raise e
    log_message('Product Profile %s' % product_profile, 2)

    return product_profile


def get_radiometric_resolution(dom):
    """Get the radiometric resolution for the supplied product record."""

    mission_index = dom.getElementsByTagName('PLATFORMNAME')[0]
    mission_index_value = mission_index.firstChild.nodeValue
    if mission_index_value == 'Landsat-7':
        return 8
    elif mission_index_value == 'Landsat-8':
        return 16


def get_cloud_cover(dom):
    """Get the scene's cloud cover"""
    return dom.getElementsByTagName(
        'CLOUDCOVERPERCENTAGE')[0].firstChild.nodeValue


def get_solar_zenith_angle(dom):
    """Get the solar zenith angle"""
    return dom.getElementsByTagName(
        'ILLUMINATIONELEVATIONANGLE')[0].firstChild.nodeValue


def get_solar_azimuth_angle(dom):
    """Get the solar azimuth angle"""
    return dom.getElementsByTagName(
        'ILLUMINATIONELEVATIONAZIMUTH')[0].firstChild.nodeValue


def get_projection(dom):
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.

    In Landsat we only get 'UTM' for the CRS which is basically unusable for
    us (since we need the zone too) so we will always fail and return EPSG:4326

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """
    epsg_default_code = '32'
    zone_value = dom.getElementsByTagName('ZONE')[0]
    zone = zone_value.firstChild.nodeValue
    location_code = '7'  # 6 for north and 7 for south
    epsg_code = epsg_default_code + location_code + zone

    projection = Projection.objects.get(epsg_code=epsg_code)
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
            'landsat/'),
        verbosity_level=2,
        halt_on_error_flag=True,
        use_txt_flag=True,
        ignore_missing_thumbs=False):
    """
    Ingest a collection of Landsat metadata folders.

    :param test_only_flag: Whether to do a dummy run ( database will not be
        updated. Default False.
    :type test_only_flag: bool

    :param source_path: A Landsat created Landsat6 metadata xml file and thumbnail.
    :type source_path: str

    :param verbosity_level: How verbose the logging output should be. 0-2
        where 2 is very very very very verbose! Default is 1.
    :type verbosity_level: int

    :param halt_on_error_flag: Whather we should stop processing when the first
        error is encountered. Default is True.
    :type halt_on_error_flag: bool

    :param use_txt_flag: Whether to read a txt or xml file. Default False.
    :type use_txt_flag: bool

    :param ignore_missing_thumbs: Whether we should raise an error
        if we find we are missing a thumbnails. Default is False.
    :type ignore_missing_thumbs: bool
    """
    def log_message(log_message_content, level=1):
        """Log a message for a given level.

        :param log_message_content: A message.
        :param level: A log level.
        """
        if verbosity_level >= level:
            print log_message_content

    log_message((
        'Running Landsat 7/8 Importer with these options:\n'
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

    ingestor_version = 'Landsat7/8 ingestor version 1.2'
    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    log_message('Starting directory scan...', 2)

    for myFolder in glob.glob(os.path.join(source_path, '*')):
        try:
            log_message('', 2)
            log_message('---------------', 2)
            # Get the folder name
            product_folder = os.path.split(myFolder)[-1]
            log_message('product folder: %s ' % product_folder, 2)

            # Find the first and only xml file in the folder
            if use_txt_flag:
                search_path = os.path.join(str(myFolder), '*.txt')
            else:
                search_path = os.path.join(str(myFolder), '*.xml')
            log_message('search path: %s ' % search_path, 2)

            # xml_file = glob.glob(search_path)[0]
            for xml_file in glob.glob(search_path):
                log_message('xml_file: %s ' % xml_file, 2)
                record_count += 1

                if use_txt_flag:
                    log_message('processing txt metadata', 2)
                    data = ingest_txt(xml_file)
                    original_product_id = data['original_product_id']
                else:
                    log_message('processing xml metadata', 2)
                    file_path = os.path.basename(xml_file)
                    filename = os.path.splitext(file_path)[0]
                    # Create a DOM document from the file
                    dom = parse(xml_file)
                    #
                    # First grab all the generic properties that any
                    # Landsat will have...
                    geometry = get_geometry(dom)
                    start_date_time, center_date_time = get_dates(
                        log_message, dom)
                    # projection for GenericProduct
                    projection = get_projection(dom)
                    original_product_id = get_original_product_id(dom, filename)
                    # Band count for GenericImageryProduct
                    band_count = get_band_count()
                    # orbit_number = get_orbit_number(dom) -- NOT SPECIFIED IN METADATA
                    # # Spatial resolution x for GenericImageryProduct
                    spatial_resolution_x = float(get_spatial_resolution_x(filename))
                    # # Spatial resolution y for GenericImageryProduct
                    spatial_resolution_y = float(
                        get_spatial_resolution_y(filename))
                    log_message('Spatial resolution y: %s' % spatial_resolution_y, 2)
                    # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
                    spatial_resolution = (
                                             spatial_resolution_x + spatial_resolution_y) / 2
                    log_message('Spatial resolution: %s' % spatial_resolution, 2)
                    radiometric_resolution = get_radiometric_resolution(dom)
                    log_message(
                        'Radiometric resolution: %s' % radiometric_resolution, 2)
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

                    # Other data
                    cloud_cover = get_cloud_cover(dom)
                    solar_zenith_angle = get_solar_zenith_angle(dom)
                    solar_azimuth_angle = get_solar_azimuth_angle(dom)

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
                        # 'orbit_number': orbit_number,  # Not in current metadata
                        'cloud_cover': cloud_cover,
                        'projection': projection,
                        'quality': quality,
                        'solar_zenith_angle': solar_zenith_angle,
                        'solar_azimuth_angle': solar_azimuth_angle
                    }

                # Check if it's already in catalogue:
                try:
                    today = datetime.today()
                    time_stamp = today.strftime("%Y-%m-%d")
                    log_message('Time Stamp: %s' % time_stamp, 2)
                except Exception, e:
                    print e.message

                update_mode = True
                try:
                    log_message('Trying to update')
                    # original_product_id is not necessarily unique
                    # so we use product_id
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

                    except Exception, e:
                        log_message(e.message, 1)

                    new_record_flag = True
                except Exception, e:
                    print e.message

                log_message('Saving product and setting thumb', 1)
                try:
                    product.save()
                    if update_mode:
                        updated_record_count += 1
                    else:
                        created_record_count += 1
                    if new_record_flag:
                        log_message('Product %s imported.' % record_count, 2)
                        pass
                    else:
                        log_message('Product %s updated.' % updated_record_count, 2)
                        pass
                except Exception, e:
                    traceback.print_exc(file=sys.stdout)
                    raise CommandError('Cannot import: %s' % e)

                if test_only_flag:
                    log_message('Testing: image not saved.', 1)
                    pass
                else:
                    thumbs_folder = os.path.join(
                        settings.THUMBS_ROOT,
                        product.thumbnailDirectory())
                    try:
                        os.makedirs(thumbs_folder)
                    except OSError:
                        # TODO: check for creation failure rather than
                        # attempt to  recreate an existing dir
                        pass

                    jpeg_path = os.path.join(str(xml_file))
                    if use_txt_flag:
                        jpeg_path = jpeg_path[:-7] + 'BQA.TIF'
                    else:
                       jpeg_path = jpeg_path.replace(".XML", "-THUMB.jpg")
                    log_message('jpeg_path: %s' % jpeg_path, 2)

                    new_name = '%s.jpg' % product.original_product_id

                    if jpeg_path:
                        try:
                            if use_txt_flag:
                                shutil.copyfile(
                                    jpeg_path,
                                    os.path.join(thumbs_folder, new_name))
                            else:
                                shutil.copyfile(
                                    os.path.join(jpeg_path, new_name),
                                    os.path.join(thumbs_folder, new_name))
                                print new_name
                        except IOError as e:
                            if ignore_missing_thumbs:
                                continue
                            else:
                                raise Exception('Missing thumbnail in %s' % jpeg_path)
                        # Transform and store .wld file
                    #     log_message('Referencing thumb', 2)
                    #     try:
                    #         path = product.georeferencedThumbnail()
                    #         log_message('Georeferenced Thumb: %s' % path, 2)
                    #     except:
                    #         traceback.print_exc(file=sys.stdout)
                    # elif ignore_missing_thumbs:
                    #         log_message('IGNORING missing thumb:')
                    else:
                        raise Exception('Missing thumbnail in %s' % jpeg_path)

                if new_record_flag:
                    log_message('Product %s imported.' % record_count, 2)
                    pass
                else:
                    log_message('Product %s updated.' % updated_record_count, 2)
                    pass

                if test_only_flag:
                    transaction.rollback()
                    log_message('Imported scene : %s' % product_folder, 2)
                    log_message('Testing only: transaction rollback.', 2)
                else:
                    transaction.commit()
                    log_message('Imported scene : %s' % product_folder, 2)

        except Exception as e:
            log_message('Record import failed. AAAAAAARGH! : %s %s' %
                        (product_folder, e), 1)
            failed_record_count += 1
            if halt_on_error_flag:
                print e.message
                break
            else:
                continue

    # To decide: should we remove ingested product folders?

    print '==============================='
    print 'Products processed : %s ' % record_count
    print 'Products updated : %s ' % updated_record_count
    print 'Products imported : %s ' % created_record_count
    print 'Products failed to import : %s ' % failed_record_count
    print '==============================='


list_keywords = ['CORNER_UL_LAT_PRODUCT',
                 'CORNER_UL_LON_PRODUCT',
                 'CORNER_UR_LAT_PRODUCT',
                 'CORNER_UR_LON_PRODUCT',
                 'CORNER_LL_LAT_PRODUCT',
                 'CORNER_LL_LON_PRODUCT',
                 'CORNER_LR_LAT_PRODUCT',
                 'CORNER_LR_LON_PRODUCT',
                 'FILE_DATE',
                 'CLOUD_COVER',
                 'SENSOR_ID',
                 'UTM_ZONE'
                 ]


def get_cloud_cover_txt(list_values):
    return float(list_values['CLOUD_COVER'])


def get_geometry_txt(list_values):
    polygon = 'POLYGON ((' ' %s %s, %s %s, %s %s, %s %s, %s %s' '))' % (
        list_values['CORNER_UL_LON_PRODUCT'], list_values['CORNER_UL_LAT_PRODUCT'],
        list_values['CORNER_UR_LON_PRODUCT'], list_values['CORNER_UR_LAT_PRODUCT'],
        list_values['CORNER_LR_LON_PRODUCT'], list_values['CORNER_LR_LAT_PRODUCT'],
        list_values['CORNER_LL_LON_PRODUCT'], list_values['CORNER_LL_LAT_PRODUCT'],
        list_values['CORNER_UL_LON_PRODUCT'], list_values['CORNER_UL_LAT_PRODUCT'],
    )
    polygon_geometry = WKTReader().read(polygon)
    return polygon_geometry


def get_dates_txt(list_values):
    start_date = list_values['FILE_DATE']

    start_year = start_date[0:4]
    start_month = start_date[5:7]
    start_day = start_date[:8:10]
    start_time = start_date[11:18]
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


def get_original_product_id_txt(filename):
    constant = 'JSA00'
    product_name_file = filename[0:3]
    splitted_filename = filename.split('_')
    if len(splitted_filename) > 3:
        # example filename: LC08_L1TP_170083_20180111_20180119_01_T1_MTL
        product_filename = splitted_filename[1] + splitted_filename[2] + \
                           splitted_filename[3] + splitted_filename[4]
    else:
        # example filename: LO81750672017347JSA00_MTL
        product_filename = filename[3:16]

    # Get part of product name from filename.
    product_name = product_name_file + product_filename + constant
    return product_name


def get_product_profile_txt(list_values, filename):
    """Find the product_profile for this record.

    It can be that one or more spectral modes are associated with a product.
    For example Landsat8 might have Pan (1 band), Multispectral (8 bands) and
    Thermal (2 bands) modes associated with a single product (total 11 bands).

    Because of this there is a many to many relationship on
    OpticalProductProfile and to get a specific OpticalProductProfile record
    we would need to know the satellite instrument and all the associated
    spectral modes to that profile record.

    We use the following elements to reverse engineer what the
    OpticalProductProfile is::

        <feature key="type">HRF</feature>
        <feature key="sensor">OLI_TIRS</feature>
        <feature key="mission">LANDSAT8</feature>

    :param list_values: A list of values from txt file.
    :type list_values: dict

    :param filename: A full path file name.
    :type filename: String.

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """
    # We need type, sensor and mission so that we can look up the
    # OpticalProductProfile that applies to this product
    sensor_value = list_values['SENSOR_ID'].strip('"')
    mission_value = get_mission_value(filename)

    try:
        instrument_type = InstrumentType.objects.get(
            operator_abbreviation=sensor_value)  # e.g. OLI_TIRS
    except Exception, e:
        # print e.message
        raise e

    satellite = Satellite.objects.get(abbreviation=mission_value)

    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise e

    # Note that in some cases e.g. Landsat you may get more that one instrument
    # groups matched. When the time comes you will need to add more filtering
    # rules to ensure that you end up with only one instrument group.
    # For the mean time, we can assume that Landsat will return only one.

    try:
        satellite_instrument = SatelliteInstrument.objects.get(
            satellite_instrument_group=satellite_instrument_group)
    except Exception, e:
        print e.message
        raise e

    try:
        spectral_modes = SpectralMode.objects.filter(
            instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise

    try:
        product_profile = OpticalProductProfile.objects.get(
            satellite_instrument=satellite_instrument,
            spectral_mode__in=spectral_modes)
    except Exception, e:
        print e.message
        print 'Searched for satellite instrument: %s and spectral modes %s' % (
            satellite_instrument, spectral_modes
        )
        raise e

    return product_profile


def get_projection_txt(list_values):
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.

    In Landsat we only get 'UTM' for the CRS which is basically unusable for
    us (since we need the zone too) so we will always fail and return EPSG:4326

    :param list_values: A list of values from txt file.
    :type list_values: dict

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """
    epsg_default_code = '32'
    zone = list_values['UTM_ZONE']
    location_code = '7'  # 6 for north and 7 for south
    epsg_code = epsg_default_code + location_code + zone

    projection = Projection.objects.get(epsg_code=epsg_code)
    return projection


def get_radiometric_resolution_txt(filename):
    """Get the radiometric resolution for the supplied product record.

    :param filename: A full path file name.
    :type filename: String.

    :returns: Either 8 or 16.
    :rtype: integer.
    """
    mission_index_value = filename[0:3]
    if mission_index_value == 'L07':
        return 8
    elif mission_index_value == 'L08':
        return 16


def ingest_txt(search_path):
    """
    Ingest a collection of Landsat metadata folders using txt files.

    The entry point is from ingest function.

    :param search_path: A path to the Landsat folder.
    :type search_path: String

    :returns: A dictionary of data to be populated to database.
    :rtype: dict
    """
    def log_message(log_message_content, level=1):
        """Log a message for a given level.

        :param log_message_content: A message.
        :param level: A log level.
        """
        if level == 1:
            print log_message_content

    try:
        log_message('Processing txt files', 1)
        file_path = os.path.basename(search_path)
        filename = os.path.splitext(file_path)[0]

        list_values = {}
        metadata = ""
        # find the keywords and save it to the list
        with open(search_path, 'r') as f:
            for line in f:
                loi = line.strip().split(' = ')
                search_keyword = loi[0]
                metadata += line
                if search_keyword in list_keywords:
                    search_value = loi[1]
                    list_values[search_keyword] = search_value

        geometry = get_geometry_txt(list_values)
        radiometric_resolution = get_radiometric_resolution_txt(filename)
        original_product_id = get_original_product_id_txt(filename)
        unique_product_id = original_product_id

        cloud_cover = get_cloud_cover_txt(list_values)
        projection = get_projection_txt(list_values)
        quality = get_quality()
        start_date_time = get_dates_txt(list_values)
        center_date_time = get_dates_txt(list_values)
        spatial_resolution_x = get_spatial_resolution_x(filename)
        spatial_resolution_y = get_spatial_resolution_y(filename)
        spatial_resolution = (spatial_resolution_x + spatial_resolution_y) / 2
        product_profile = get_product_profile_txt(list_values, filename)

        data = {
            'metadata': metadata,
            'spatial_coverage': geometry,
            'radiometric_resolution': radiometric_resolution,
            # 'band_count': band_count,
            'band_count': 9,
            'original_product_id': original_product_id,
            'unique_product_id': unique_product_id,
            'spatial_resolution_x': spatial_resolution_x,
            'spatial_resolution_y': spatial_resolution_y,
            'spatial_resolution': spatial_resolution,
            'product_profile': product_profile,
            'product_acquisition_start': start_date_time,
            'product_date': center_date_time,
            # 'orbit_number': orbit_number,  # Not in current metadata
            'cloud_cover': cloud_cover,
            'projection': projection,
            'quality': quality,
            'solar_zenith_angle': 45.00,
            'solar_azimuth_angle': 45.00
            # 'solar_zenith_angle': solar_zenith_angle,
            # 'solar_azimuth_angle': solar_azimuth_angle
        }
        log_message(data, 3)
    except Exception as e:
        log_message('Error on ingest_txt: %s' % e, 1)
    return data
