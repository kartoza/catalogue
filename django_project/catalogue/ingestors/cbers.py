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
from catalogue.models.pycsw import PycswExtraFields


def parse_date_time(date_stamp):
    """A helper method to create a date object from a CBERS time stamp.

    :param date_stamp: Date in this format:
    :type date_stamp: str

    Example format from CBERS:`2015-12-03 10:40:23`

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
    up_left_lat_value = dom.getElementsByTagName('productUpperLeftLat')[0]
    up_left_lat = up_left_lat_value.firstChild.nodeValue

    up_left_long_value = dom.getElementsByTagName('productUpperLeftLong')[0]
    up_left_long = up_left_long_value.firstChild.nodeValue

    up_right_lat_value = dom.getElementsByTagName('productUpperRightLat')[0]
    up_right_lat = up_right_lat_value.firstChild.nodeValue

    up_right_long_value = dom.getElementsByTagName('productUpperRightLong')[0]
    up_right_long = up_right_long_value.firstChild.nodeValue

    low_left_lat_value = dom.getElementsByTagName('productLowerLeftLat')[0]
    low_left_lat = low_left_lat_value.firstChild.nodeValue

    low_left_long_value = dom.getElementsByTagName('productLowerLeftLong')[0]
    low_left_long = low_left_long_value.firstChild.nodeValue

    low_right_lat_value = dom.getElementsByTagName('productLowerRightLat')[0]
    low_right_lat = low_right_lat_value.firstChild.nodeValue

    low_right_long_value = dom.getElementsByTagName('productLowerRightLong')[0]
    low_right_long = low_right_long_value.firstChild.nodeValue

    polygon = 'POLYGON((' '%s %s, ' \
              '%s %s, %s %s, %s %s, %s %s' '))' % (
        up_left_long, up_left_lat,
        up_right_long, up_right_lat,
        low_right_long, low_right_lat,
        low_left_long, low_left_lat,
        up_left_long, up_left_lat )

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

    :return: A two-tuple of dates for the start, and mid scene
        respectively.
    :rtype: (datetime, datetime)
    """
    start_element = dom.getElementsByTagName('imagingStartTime')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parse_date_time(start_date)
    log_message('Product Start Date: %s' % start_date, 2)

    product_date = dom.getElementsByTagName('productDate')[0]
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
    band_count_data = dom.getElementsByTagName('bands')[0]
    band_count = band_count_data.firstChild.nodeValue
    if len(band_count)==1:
        return 1
    else:
        return len(eval(band_count))

def get_solar_azimuth_angle(dom):
    sun_azimuth = dom.getElementsByTagName('sunAzimuthElevation')[0]
    solar_azimuth = sun_azimuth.firstChild.nodeValue
    return solar_azimuth

def get_scene_row(dom):
    scene_row = dom.getElementsByTagName('sceneRow')[0]
    row = scene_row.firstChild.nodeValue
    return row

def get_scene_path(dom):
    scene_path = dom.getElementsByTagName('scenePath')[0]
    path = scene_path.firstChild.nodeValue
    return path

def get_sensor_inclination():
    # The static value of sensor inclination angle
    # source http://www.cbers.inpe.br/ingles/satellites/orbit_cbers3_4.php
    return 98.5

def get_spatial_resolution_x(dom):
    spatial_resolution_data = dom.getElementsByTagName('pixelSpacing')[0]
    spatial_resolution = spatial_resolution_data.firstChild.nodeValue
    return spatial_resolution

def get_spatial_resolution_y(dom):
    spatial_resolution_data = dom.getElementsByTagName('pixelSpacing')[0]
    spatial_resolution = spatial_resolution_data.firstChild.nodeValue
    return spatial_resolution

def get_product_profile(log_message, product_id):
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
    sensor_value = product_id[4:7]
    mission_index = product_id[0:4]

    try:
        instrument_type = InstrumentType.objects.get(
            operator_abbreviation=sensor_value)  # e.g. MUX, P10
    except Exception, e:
        #print e.message
        raise e
    log_message('Instrument Type %s' % instrument_type, 2)

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
    get_sensor_id = dom.getElementsByTagName('sensorId')[0]
    sensor_id = get_sensor_id.firstChild.nodeValue
    # sensor_id : MUX, P10, P5M, WFI
    if sensor_id == 'MUX':
        return 8
    elif sensor_id == 'P10':
        return 8
    elif sensor_id =='P5M':
        return 8
    elif sensor_id == 'WFI':
        return 10
    else:
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
    get_zone = dom.getElementsByTagName('zone')[0]
    zone_value = get_zone.firstChild.nodeValue
    zone = zone_value[0:2]
    location_code = '7'  # 6 for north and 7 for south
    epsg_code = epsg_default_code + location_code + zone

    projection = Projection.objects.get(epsg_code=epsg_code)
    return projection


def get_quality(dom):
    """Get the quality for this record - currently hard coded to unknown.

    :returns: A quality object fixed to 'unknown'.
    :rtype: Quality
    """
    overall_quality = dom.getElementsByTagName('overallQuality')[0]
    quality_xml = str(overall_quality.firstChild.nodeValue)
    quality = Quality.objects.get(name=quality_xml)
    return quality


def ingest(
        test_only_flag=True,
        source_path=(
            '/home/web/catalogue/django_project/catalogue/tests/sample_files/'
            'CBERS/'),
        verbosity_level=2,
        halt_on_error_flag=True,
        ignore_missing_thumbs=False):
    """
    Ingest a collection of CBERS metadata folders.

    :param test_only_flag: Whether to do a dummy run ( database will not be
        updated. Default False.
    :type test_only_flag: bool

    :param source_path: A CBERS created CBERS 04 metadata xml file and thumbnail.
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
        'Running CBERS 04 Importer with these options:\n'
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

    ingestor_version = 'CBERS 04 ingestor version 1.1'
    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    log_message('Starting directory scan...', 2)

    for myFolder in glob.glob(os.path.join(source_path, '*.XML')):
        record_count += 1
        try:
            log_message('', 2)
            log_message('---------------', 2)
            # Get the folder name
            product_folder = os.path.split(myFolder)[-1]
            log_message(product_folder, 2)

            # Find the first and only xml file in the folder
            # search_path = os.path.join(str(myFolder), '*.XML')
            log_message(myFolder, 2)
            xml_file = glob.glob(myFolder)[0]
            file = os.path.basename(xml_file)
            file_name = os.path.splitext(file)[0]
            original_product_id = get_original_product_id(file_name)

            # Create a DOM document from the file
            dom = parse(xml_file)

            # First grab all the generic properties that any CBERS will have...
            geometry = get_geometry(log_message, dom)
            start_date_time, center_date_time = get_dates(
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
                'product_date': center_date_time,
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
                    log_message(e.message, 2)

                new_record_flag = True
            except Exception, e:
                print e.message

            # now try to fill in the metadata
            # populate metadata into temp pycsw table here
            identifier = original_product_id
            sensor_id = original_product_id[4:7]
            satellite_id = original_product_id[0:4]
            data_pycsw = {
                'identifier': identifier,
                'type_name': 'pycsw:CoreMetadata',
                'schema': 'http://www.opengis.net/cat/csw/2.0.2',
                'mdsource': 'local',
                'insert_date': today,
                'xml': myFolder,
                'any_text': myFolder,
                'language': 'EN',
                # 'title': '',
                # 'abstract': '',
                # 'keywords': '',
                # 'keyword_type': '',
                'format': 'jpg',
                # 'source': '',
                'date': start_date_time,
                'modified_date': today,
                # 'type': '',
                'bounding_box': '[%s,%s]' % (spatial_resolution_x, spatial_resolution_y),
                'crs': projection.epsg_code,
                # 'alternate_title': '',
                'revision_date': today,
                'creation_date': today,
                'publication_date': today,
                # 'organization_name': 'SANSA',
                # 'security_constraints': '',
                # 'parent_identifier': '',
                # 'topic_category': '',
                # 'resource_language': '',
                # 'geo_desc_code': '',
                # 'denominator': '',
                # 'distance_value': '',
                # 'distance_uom': '',
                'temp_extent_begin': today,
                'temp_extent_end': today,
                # 'service_type': '',
                # 'service_type_version': '',
                # 'operation': '',
                # 'coupling_type': '',
                # 'operates_on': '',
                # 'operates_on_identifier': '',
                # 'operates_on_name': '',
                # 'degree': '',
                # 'access_constraints': '',
                # 'other_constraints': '',
                # 'classification': '',
                # # 'condition_applying_tau': '',
                # 'lineage': '',
                # 'responsible_party_role': '',
                # 'spec_title': '',
                #'spec_date': today,
                # 'spec_date_type': '',
                'creator': 'admin',
                'publisher': 'SANSA',
                'sensor_abbreviation': sensor_id,
                'satellite_abbreviation': satellite_id
                # 'contributor': '',
                # 'relation': '',
                # 'links': ''
            }
            try:
                # populate ingested_pycsw so it can be transferred to catalogue_pycsw later
                # ingested_pycsw = PycswCbers.objects.get(identifier=identifier)
                ingested_pycsw = PycswExtraFields.objects.get(identifier=identifier)


                # pycsw part
                ingested_pycsw.__dict__.update(data_pycsw)

            except ObjectDoesNotExist:
                # pycsw part
                try:
                    # ingested_pycsw = PycswCbers(**data_pycsw)
                    ingested_pycsw = PycswExtraFields(**data_pycsw)

                except Exception, e:
                    # log_message(e.message, 2)
                    log_message(e.message)

            log_message('Saving product and setting thumb', 2)
            try:
                product.save()
                ingested_pycsw.save()

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
                    # log_message(jpeg_path, 2)
                    jpeg_path = jpeg_path.replace(".XML", "-THUMB.JPG")

                    if jpeg_path:
                        print jpeg_path
                        new_name = '%s.JPG' % product.original_product_id
                        shutil.copyfile(
                            jpeg_path,
                            os.path.join(thumbs_folder, new_name))
                        print new_name
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
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                raise CommandError('Cannot import: %s' % e)

            if test_only_flag:
                transaction.rollback()
                log_message('Imported scene : %s' % product_folder, 1)
                log_message('Testing only: transaction rollback.', 1)
            else:
                transaction.commit()
                log_message('Imported scene : %s' % product_folder, 1)
        except Exception, e:
            log_message('Record import failed. AAAAAAARGH! : %s' %
                        product_folder, 1)
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