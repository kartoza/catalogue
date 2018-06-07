__author__ = 'boney - <--boney@kartoza.com-->'
__date__ = '31/5/18'

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
    """A helper method to create a date object from a RADARSAT time stamp.

    :param date_stamp: Date in this format:
    :type date_stamp: str

    Example format from RADARSAT:`2018-04-26T16:34:59.701050Z`

    :returns: A python datetime object.
    :rtype: datetime
    """
    start_year = date_stamp[0:4]
    start_month = date_stamp[5:7]
    start_day = date_stamp[8:10]
    start_time = date_stamp[11:19]
    tokens = start_time.split(':')
    start_hour = tokens[0]
    start_minute = tokens[1]
    start_seconds = tokens[2]

    parsed_date_time = datetime(
        int(start_year),
        int(start_month),
        int(start_day),
        int(start_hour),
        int(start_minute),
        int(start_seconds))
    return parsed_date_time

def get_geometry(log_message, dom):
    #TODO: how to parse the geometry from metadata?
    """Extract the bounding box as a geometry from the xml file.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: DOM Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: geoemtry
    """
    polygon = 'POLYGON((' '%s %s, ' \
              '%s %s, %s %s, %s %s, %s %s' '))' % (
        10.175218, -26.205927,
        11.655573, -26.186210,
        11.684172, -27.406972,
        10.187890, -27.427757,
        10.175218, -26.205927 )
    log_message('polygon: %s' % polygon, 2)

    myReader = WKTReader()
    myGeometry = myReader.read(polygon)
    log_message('Geometry: %s' % myGeometry, 2)
    return myGeometry


def get_dates(log_message, dom):
    """Get the start, mid scene and end dates.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: the start date
    :rtype: (datetime)
    """
    start_element = dom.getElementsByTagName('rawDataStartTime')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parse_date_time(start_date)
    log_message('Product Start Date: %s' % start_date, 2)
    return start_date

def get_original_product_id(foldername):
    # Get part of product name from folder name
    # file name = RS2_20180426_163459_0076_OSVN_HHHV_SCS_633151_3832_19230707
    folder_name = foldername.split('/')[-1]

    product_name = folder_name.split('_')

    return product_name[0] + product_name[1] + \
           product_name[2] + product_name[3]

def get_band_count(dom):
    #TODO: how to extract band_count from metadata?
    return 3

def get_solar_azimuth_angle(dom):
    #TODO: not sure about this, hardcoded for now
    return 241.648

def get_scene_row(dom):
    #TODO: not sure about this, hardcoded for now
    return 1

def get_scene_path(dom):
    #TODO: not sure about this, hardcoded for now
    return 9

def get_sensor_inclination():
    #TODO: not sure about this, hardcoded for now
    return 98.5

def get_spatial_resolution_x(dom):
    #TODO: not sure about this, hardcoded for now
    return 20

def get_spatial_resolution_y(dom):
    #TODO: not sure about this, hardcoded for now
    return 10

def get_product_profile(log_message, product_id):
    #TODO: not sure about this, some fields are hardcoded for now
    """Find the product_profile for this record.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """
    try:
        instrument_type = InstrumentType.objects.get(
            operator_abbreviation='SAR')
    except Exception, e:
        raise e
    log_message('Instrument Type %s' % instrument_type, 2)

    satellite = Satellite.objects.get(abbreviation='RSAT2')

    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise e
    log_message('Satellite Instrument Group %s' %
                satellite_instrument_group, 2)
    try:
        satellite_instrument = SatelliteInstrument.objects.get(
            satellite_instrument_group=satellite_instrument_group)
    except Exception, e:
        print e.message
        raise e
    log_message('Satellite Instrument %s' % satellite_instrument, 2)

    try:
        spectral_modes = SpectralMode.objects.filter(
            instrument_type=19)
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
    #TODO: not sure about this, hardcoded for now

    """Get the radiometric resolution for the supplied product record.

    :param resolution_element: Dom Document containing the bounds of the scene.
    :type resolution_element: DOM document.

    :returns: The bit depth for the image.
    :rtype: int
    """
    return 1


def get_projection(dom):
    #TODO: not sure about this, hardcoded for now
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.

    :param specific_parameters: Dom Document containing the bounds of the scene.
    :type specific_parameters: DOM document.

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """
    projection = Projection.objects.get(epsg_code='4326')
    return projection


def get_quality(dom):
    #TODO: not sure about this, hardcoded for now
    """Get the quality for this record - currently hard coded to unknown.

    :returns: A quality object fixed to 'unknown'.
    :rtype: Quality
    """
    quality = Quality.objects.get(name=9)
    return quality


def ingest(
        test_only_flag=True,
        source_path=(
            '/home/web/catalogue/django_project/catalogue/tests/sample_files/'
            'RADARSAT/'),
        verbosity_level=2,
        halt_on_error_flag=True,
        ignore_missing_thumbs=False):
    """
    Ingest a collection of RADARSAT metadata folders.

    :param test_only_flag: Whether to do a dummy run ( database will not be
        updated. Default False.
    :type test_only_flag: bool

    :param source_path: A RADARSAT created RADARSAT metadata xml file and thumbnail.
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
            print message

    log_message((
        'Running RADARSAT-2 Importer with these options:\n'
        'Test Only Flag: %s\n'
        'Source Dir: %s\n'
        'Verbosity Level: %s\n'
        'Halt on error: %s\n'
        '------------------')
        % (test_only_flag, source_path, verbosity_level,
           halt_on_error_flag), 2)

    # Scan the source folder and look for any sub-folders
    # The sub-folder names should be e.g.
    # RS2_20180426_163459_0076_OSVN_HHHV_SCS_633151_3832_19230707
    # the product name will be extracted from the folder name
    log_message('Scanning folders in %s' % source_path, 2)
    # Loop through each folder found

    ingestor_version = 'RADARSAT-2 ingestor version 0.1'
    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    log_message('Starting directory scan...', 2)

    # loop on subfolders
    for dirName, subdirlist, fileList in os.walk(source_path):
        # for each subfolder, search metadata and thumbnail
        for myFolder in glob.glob(os.path.join(source_path, dirName, '*.xml')):
            record_count += 1
            try:
                log_message('', 2)
                log_message('---------------', 2)
                # Get the folder name
                product_folder = os.path.split(myFolder)[-1]
                log_message(product_folder, 2)
                log_message(myFolder, 2)
                xml_file = glob.glob(myFolder)[0]
                original_product_id = get_original_product_id(dirName)

                # Create a DOM document from the file
                dom = parse(xml_file)

                geometry = get_geometry(log_message, dom)
                start_date_time = get_dates(
                    log_message, dom)
                # projection for GenericProduct
                projection = get_projection(dom)

                # Band count for GenericImageryProduct
                band_count = get_band_count(dom)
                row = get_scene_row(dom)
                path = get_scene_path(dom)
                solar_azimuth_angle = get_solar_azimuth_angle(dom)
                sensor_inclination = get_sensor_inclination()
                # # Spatial resolution x for GenericImageryProduct
                spatial_resolution_x = float(get_spatial_resolution_x(dom))
                # # Spatial resolution y for GenericImageryProduct
                spatial_resolution_y = float(
                    get_spatial_resolution_y(dom))
                log_message('Spatial resolution y: %s' % spatial_resolution_y, 2)

                # # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
                spatial_resolution = (spatial_resolution_x + spatial_resolution_y) / 2
                log_message('Spatial resolution: %s' % spatial_resolution, 2)
                radiometric_resolution = get_radiometric_resolution(dom)
                log_message('Radiometric resolution: %s' % radiometric_resolution, 2)
                quality = get_quality(dom)
                # ProductProfile for OpticalProduct
                product_profile = get_product_profile(log_message, original_product_id)

                # Do the ingestion here...
                data = {
                    'spatial_coverage': geometry,
                    'radiometric_resolution': radiometric_resolution,
                    'band_count': band_count,
                    'original_product_id': original_product_id,
                    'unique_product_id': original_product_id,
                    'spatial_resolution_x': spatial_resolution_x,
                    'spatial_resolution_y': spatial_resolution_y,
                    'spatial_resolution': spatial_resolution,
                    'product_profile': product_profile,
                    'product_acquisition_start': start_date_time,
                    'product_date': start_date_time,
                    'sensor_inclination_angle': sensor_inclination,
                    'solar_azimuth_angle': solar_azimuth_angle,
                    'row': row,
                    'path': path,
                    'projection': projection,
                    'quality': quality
                }
                log_message(data, 3)
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

                    except Exception, e:
                        log_message(e.message, 2)

                    new_record_flag = True
                except Exception, e:
                    print e.message

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

                        # the thumbnail names are expected to be BrowseImage.tif
                        jpeg_path = os.path.join(dirName, "BrowseImage.tif")

                        if jpeg_path:
                            print jpeg_path
                            new_name = '%s.JPG' % product.original_product_id
                            shutil.copyfile(
                                jpeg_path,
                                os.path.join(thumbs_folder, new_name))
                            print new_name
                        else:
                            raise Exception('Missing thumbnail in %s' %jpeg_path)
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
                    transaction.rollback()
                    log_message('Imported scene : %s' % product_folder, 2)
                    log_message('Testing only: transaction rollback.', 2)
                else:
                    transaction.commit()
                    log_message('Imported scene : %s' % product_folder, 2)
            except Exception, e:
                log_message('=== %s' % e, 2)
                log_message('Record import failed. AAAAAAARGH! : %s' %
                            product_folder, 2)
                failed_record_count += 1
                if halt_on_error_flag:
                    print e.message
                    break
                else:
                    continue

    print '==============================='
    print 'Products processed : %s ' % record_count
    print 'Products updated : %s ' % updated_record_count
    print 'Products imported : %s ' % created_record_count
    print 'Products failed to import : %s ' % failed_record_count
    print '==============================='