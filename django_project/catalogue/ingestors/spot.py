# coding=utf-8
"""
SANSA-EO Catalogue - metadata importer - SPOT.

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without express permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.


  Sample data from one record:
  wkt_geom   POLYGON((5.381600 15.316700,5.507500 15.847000,6.055500
             15.725200,5.928300 15.195200,5.381600 15.316700))
  A21        50673191101191017402J
  SC_NUM     17670901
  SEG_NUM    6729479
  SATEL      5
  ANG_INC    5.884188
  ANG_ACQ    5.2
  DATE_ACQ   19/01/2011
  MONTH_ACQ  01
  TIME_ACQ   10:17:40
  CLOUD_QUOT AAAAAAAA
  CLOUD_PER  0
  SNOW_QUOT  00000000
  LAT_CEN    15.521
  LON_CEN    5.7172
  LAT_UP_L   15.847
  LON_UP_L   5.5075
  LAT_UP_R   15.725
  LON_UP_R   6.0555
  LAT_LO_L   15.316
  LON_LO_L   5.3816
  LAT_LO_R   15.195
  LON_LO_R   5.9283
  RESOL      2.5
  MODE       COLOR
  TYPE       T
  URL_QL     http://sirius.spotimage.fr/url/catalogue.aspx?ID=
             -1&ACTION=Scenes%3AgetQuicklook&CODEA21=
             50673191101191017402J&SEGMENT=6524011&SAT=0
"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__version__ = '0.1'
__date__ = '29/01/2014'
__copyright__ = 'South African National Space Agency'

import os
import sys
from datetime import datetime
import traceback
import urllib2
from mercurial import lock, error
from django.core.management.base import CommandError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.feature import Feature

# from django.db import transaction
# from django.contrib.gis.geos import WKTReader
# from django.core.management.base import CommandError
# from django.core.exceptions import ObjectDoesNotExist
# from django.conf import settings

from dictionaries.models import (
    SpectralMode,
    SatelliteInstrument,
    OpticalProductProfile,
    InstrumentType,
    Satellite,
    SatelliteInstrumentGroup,
    Projection,
    Quality)

from ..models import OpticalProduct


def get_dates(log_message, feature):
    """Get the start, mid scene and end dates.

    We keep the same implementation style as the iif ingestor logic but note
    that for SPOT products we can only see the acquisition date and time but
    not the scene start, end and center times. Because of this we use the
    same date/time for ALL three!

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param feature: Feature from a shp.
    :type feature: Feature

    :return: A three-tuple of dates for the start, mid scene and end dates
        respectively.
    :rtype: (datetime, datetime, datetime)
    """
    # e.g. 20/01/2011
    date_parts = feature.get('DATE_ACQ').split('/')
    # e.g. 08:29:01
    time_parts = feature.get('TIME_ACQ').split(':')
    log_message('Parsing date: %s' % date_parts, 2)
    image_date = datetime(
        int(date_parts[2]),  # year
        int(date_parts[1]),  # month
        int(date_parts[0]),  # day
        int(time_parts[0]),  # hour
        int(time_parts[1]),  # minutes
        int(time_parts[2]))  # seconds
    log_message('Product date: %s' % image_date, 2)
    return image_date, image_date, image_date


def get_product_profile(log_message, feature):
    """Find the product_profile for this record.

    It can be that one or more spectral modes are associated with an
    instrument. For example SPOT5 might have Pan (1 band), Multispectral (4
    bands) modes associated with a single product (total 5 bands).

    Because of this there is a many to many relationship on
    OpticalProductProfile and to get a specific OpticalProductProfile record
    we would need to know the satellite instrument and all the associated
    spectral modes to that profile record.

    We use the following elements to reverse engineer what the
    OpticalProductProfile is::

    * type
    * sensor
    * mission

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

    :param feature: A shapefile feature.
    :type feature: Feature

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """
    # We need type, sensor and mission so that we can look up the
    # OpticalProductProfile that applies to this product

    # Work out the satellite
    satellite_number = int(feature.get('SATEL'))
    log_message('Satellite number: %s' % satellite_number, 2)
    if not int(satellite_number) in (1, 2, 3, 4, 5):
        raise CommandError(
            'Unknown Spot mission number'
            '(should be 1-5) %s.' % satellite_number)

    satellite_abbreviation = 'SPOT-%s' % satellite_number
    log_message('Satellite abbreviation: %s' % satellite_abbreviation, 2)
    satellite = Satellite.objects.get(
        operator_abbreviation=satellite_abbreviation)
    log_message('Satellite: %s' % satellite, 2)

    # Work out the instrument type
    instrument_type_abbreviation = None
    if satellite_number in [1, 2, 3]:
        instrument_type_abbreviation = 'HRV'
    elif satellite_number == 4:
        instrument_type_abbreviation = 'HRVIR'
    elif satellite_number == 5:
        instrument_type_abbreviation = 'HRG'

    instrument_type = InstrumentType.objects.get(
        operator_abbreviation=instrument_type_abbreviation)
    log_message('Instrument type: %s' % instrument_type, 2)

    # Work out the instrument group
    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise e
    log_message(
        'Satellite Instrument Group %s' %
        satellite_instrument_group, 2)

    # Work out the Instrument

    # Note that in SPOT you may get more that one instrument
    # matched. When the time comes you will need to add more filtering
    # rules to ensure that you end up with only one instrument.

    camera_number = feature.get('A21')[-2:-1]
    satellite_instrument_abbreviation = 'S%s-%s%s' % (
        satellite_number, instrument_type_abbreviation, camera_number
    )
    try:
        satellite_instrument = SatelliteInstrument.objects.get(
            satellite_instrument_group=satellite_instrument_group,
            operator_abbreviation=satellite_instrument_abbreviation)
    except Exception, e:
        print e.message
        log_message('Abbreviation: %s' % satellite_instrument_abbreviation, 2)
        raise e
    log_message('Satellite Instrument %s' % satellite_instrument, 2)

    # Work out the spectral mode

    # Note that you can get more than one spectral mode for an instrument
    # type (e.g. J, T, A, B) so we need to filter on the instrument_type and
    # the spectral mode string provided in the TYPE field of the SPOT
    # shapefile.

    spectral_mode_string = feature.get('TYPE')
    try:
        spectral_modes = SpectralMode.objects.filter(
            instrument_type=instrument_type,
            abbreviation=spectral_mode_string)
    except Exception, e:
        print e.message
        raise
    log_message('Spectral Modes %s' % spectral_modes, 2)

    # Work out the product profile

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


def skip_record(feature):
    """Determine if this feature should be skipped.

    We skip scenes with

    "MODE"  = 'COLOR' AND "TYPE" = 'T'
    "TYPE" = 'H'

    Because they are spot image value added products not supplied by SANSA.

    :param feature: A shapefile feature.
    :type feature: Feature

    :returns: True if the feature should be skipped.
    :rtype: bool
    """
    # work out the sensor type
    scene_type = feature.get('TYPE')
    # Some additional rules from Linda to skip unwanted records
    colour_mode = feature.get('MODE')
    if scene_type == 'H':
        return True
    elif scene_type == 'T' and colour_mode == 'COLOR':
        return True
    else:
        # Record is ok to ingest
        return False


def get_band_count(feature):
    """Get the number of bands for the scene represented by a feature.

    :param feature: A shapefile feature.

    :returns: The number of bands in the scene.
    :rtype: int
    """
    # work out the sensor type
    spectral_mode_string = feature.get('TYPE')

    # Spot 4 and 5 only
    if spectral_mode_string in ['J', 'I']:
        band_count = 4
    # Spot 4 and 5 only
    elif spectral_mode_string in ['M', 'A', 'B', 'T']:
        band_count = 1
    # Spot 1,2 or 3 only
    elif spectral_mode_string in ['X']:
        band_count = 3
    # Spot 1,2 or 3 only
    elif spectral_mode_string in ['P']:
        band_count = 1
    else:
        raise Exception(
            'Sensor type %s as per shp not recognised' %
            spectral_mode_string)
    return band_count


def get_projection(feature):
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.

    We will always return EPSG:4326 currently until some way is determined in
    the future to get a more meaningful result.

    :param feature: A shapefile feature.
    :type feature: Feature

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """
    _ = feature
    projection = Projection.objects.get(epsg_code=4326)
    return projection


def get_quality():
    """Get the quality for this record - currently hard coded to unknown.

    :returns: A quality object fixed to 'unknown'.
    :rtype: Quality
    """
    quality = Quality.objects.get(name='Unknown')
    return quality


def fetch_features(shapefile, area_of_interest):
    """
    Open the index and parses it, returns a generator list of features.

    :param shapefile: A shapefile downloaded from
           http://catalog.spotimage.com/pagedownload.aspx

    :param area_of_interest: A geometry defining which features to include.

    :returns: A list of geometries is returned, all intersecting with the area
        of interest if it was specified.

    """
    try:
        print('Opening %s' % shapefile)
        data_source = DataSource(shapefile)
    except Exception, e:
        raise CommandError('Loading index failed %s' % e)

    for feature in data_source[0]:
        if area_of_interest is None:
            yield feature
        else:
            if area_of_interest.intersects(feature.geom):
                yield feature


# noinspection PyDeprecation
@transaction.commit_manually
def ingest(
        shapefile,
        download_thumbs_flag=False,
        area_of_interest=None,
        test_only_flag=True,
        verbosity_level=2,
        halt_on_error_flag=True):
    """
    Ingest a collection of Spot scenes from a shapefile.

    Understanding SPOT a21 scene id:
    Concerning the SPOT SCENE products, the name will be
    the string 'SCENE ' followed by 'formatted A21 code'.
    e.g. 41573401101010649501M
    e.g. 4 157 340 11/01/01 06:49:50 1 M
    Formatted A21 code is defined as :
    N KKK-JJJ YY/MM/DD HH:MM:SS I C
    (with N: Satellite number, KKK-JJJ :
    GRS coordinates, YY/MM/DD :
    Center scene date, HH:MM:SS :
    Center scene time, I :
    Instrument number (1,2), C :
    Sensor Code (P, M, X, I, J, A, B, S, T, M+X, M+I).
    For shift along the track products, SAT value is added
    after KKK-JJJ info : '/SAT' (in tenth of scene (0 to 9))
    http://www.spotimage.com/dimap/spec/dictionary/
       Spot_Scene/DATASET_NAME.htm
    Some of these data are explicitly defined in fields in the
    catalogue shp dumps so
    we dont try to parse everything from the a21 id

    :param shapefile: A shapefile downloaded from
            http://catalog.spotimage.com/pagedownload.aspx

    :param download_thumbs_flag: Whether thumbs should be retrieved. If they
        are not fetched on ingestion, they will be fetched on demand as
        searches are made.

    :param area_of_interest: A geometry in well known text (WKT) defining which
        features to include.

    :param test_only_flag: Whether to do a dummy run ( database will not be
        updated. Default False.

    :param verbosity_level: How verbose the logging output should be. 0-2
        where 2 is very very very very verbose! Default is 1.

    :param halt_on_error_flag: Whether we should stop processing when the first
        error is encountered. Default is True.
    """
    def log_message(message, level=1):
        """Log a message for a given level.

        :param message: A message.
        :param level: A log level.
        """
        if verbosity_level >= level:
            print message

    try:
        lock_file = lock.lock('/tmp/spot_harvest.lock', timeout=60)
    except error.LockHeld:
        # couldn't take the lock
        raise CommandError('Could not acquire lock.')

    ingestor_version = 'SPOT ingestor version 3'
    log_message((
        'Running SPOT Importer v%s with these options:\n'
        'Test Only Flag: %s\n'
        'Shapefile: %s\n'
        'Area of Interest: %s\n'
        'Verbosity Level: %s\n'
        'Halt on error: %s\n'
        '------------------')
        % (ingestor_version, test_only_flag, shapefile, area_of_interest,
           verbosity_level, halt_on_error_flag), 2)

    aoi_geometry = None
    # Validate area_of_interest
    if area_of_interest is not None:
        try:
            aoi_geometry = OGRGeometry(area_of_interest)
            if not aoi_geometry.area:
                raise CommandError(
                    'Unable to create the area of interest'
                    ' polygon: invalid polygon.')
            if not aoi_geometry.geom_type.name == 'Polygon':
                raise CommandError(
                    'Unable to create the area of interest'
                    ' polygon: not a polygon.')
        except Exception, e:
            raise CommandError(
                'Unable to create the area of interest'
                ' polygon: %s.' % e)
        log_message('Area of interest filtering activated.', 1)

    record_count = 0
    skipped_record_count = 0
    updated_record_count = 0
    created_record_count = 0
    failed_record_count = 0
    log_message('Starting directory scan...', 2)

    for feature in fetch_features(shapefile, aoi_geometry):
        record_count += 1

        if record_count % 10000 == 0 and record_count > 0:
            print 'Products processed : %s ' % record_count
            print 'Products updated : %s ' % updated_record_count
            print 'Products imported : %s ' % created_record_count
            transaction.commit()

        original_product_id = feature.get('A21')

        # SPOT has a wierd thing they do on their catalogue where they
        # assign the same number to two kinds of products. For example:
        #
        # 51204201301160834432A  5m A BW image (the original product) and
        # 51204201301160834432A  2.5m T BW image (supersampled from A and B)
        #
        # Attempting to import both will cause errors because upstream
        # vendor ID's should be unique per product. To deal with this we
        # are replacing the terminating 'A' with a 'T' for the supersampled
        # products. Decision made by Linda & Tim in Jan workshop 2014
        #
        if feature.get('RESOL') == 2.5 and feature.get('TYPE') == 'T':
            original_product_id = list(original_product_id)
            original_product_id[-1:] = 'T'
            original_product_id = "".join(original_product_id)

        log_message('', 2)
        log_message('---------------', 2)
        log_message('Ingesting %s' % original_product_id, 2)

        if skip_record(feature):
            skipped_record_count += 1
            log_message('%s Skipped' % original_product_id, 1)
            continue

        try:
            # First grab all the generic properties that any scene will have...
            geometry = feature.geom.geos

            start_date_time, center_date_time, end_date_time = get_dates(
                log_message, feature)

            # projection for GenericProduct
            #print specific_parameters.toxml()
            projection = get_projection(feature)
            log_message('Projection: %s' % projection, 2)

            # Band count for GenericImageryProduct
            product_band_count = get_band_count(feature)
            log_message('Band count: %s' % product_band_count, 2)

            # Spatial resolution x for GenericImageryProduct
            spatial_resolution_x = feature.get('RESOL')
            log_message('Spatial resolution x: %s' % spatial_resolution_x, 2)

            # Spatial resolution y for GenericImageryProduct (same as x)
            spatial_resolution_y = feature.get('RESOL')
            log_message('Spatial resolution y: %s' % spatial_resolution_y, 2)

            # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
            spatial_resolution = spatial_resolution_x
            log_message('Spatial resolution: %s' % spatial_resolution, 2)

            # Radiometric resolution for GenericImageryProduct
            radiometric_resolution = 8  # 8 bits will need to change in spot 6

            # path for GenericSensorProduct
            path = feature.get('a21')[1:4].rjust(4, '0')[0]
            log_message('Path: %s' % path, 2)

            # row for GenericSensorProduct
            row = feature.get('a21')[4:7].rjust(4, '0')[0]
            log_message('Row: %s' % row, 2)

            # earth_sun_distance for OpticalProduct
            # Not provided

            # solar azimuth angle for OpticalProduct
            # Not provided

            # solar zenith angle for OpticalProduct
            # Not provided

            # sensor viewing angle for OpticalProduct
            sensor_viewing_angle = feature.get('ANG_ACQ')
            log_message('Sensor viewing angle: %s' % sensor_viewing_angle, 2)

            # sensor inclination angle for OpticalProduct
            sensor_inclination_angle = feature.get('ANG_INC')
            log_message(
                'Sensor inclination angle: %s' % sensor_inclination_angle, 2)

            # cloud cover as percentage for OpticalProduct
            # integer percent - must be scaled to 0-100 for all ingestors
            cloud_cover = int(feature.get('CLOUD_PER'))
            log_message('Cloud cover percentage: %s' % cloud_cover, 2)

            # Get the quality for GenericProduct
            quality = get_quality()
            log_message('Quality: %s' % quality, 2)

            # ProductProfile for OpticalProduct
            product_profile = get_product_profile(log_message, feature)
            log_message('Product Profile: %s' % product_profile, 2)

            # Get the original text file metadata
            metadata = '\n'.join(['%s=%s' % (
                f, feature.get(f)) for f in feature.fields])
            log_message('Metadata retrieved', 2)

            # Metadata comes from shpfile dump not DIMS...
            dims_product_id = original_product_id
            log_message('Using original product ID for DIMS ID', 2)

            # Check if there is already a matching product based
            # on original_product_id

            # Do the ingestion here...
            data = {
                'metadata': metadata,
                'spatial_coverage': geometry,
                'radiometric_resolution': radiometric_resolution,
                'band_count': product_band_count,
                'cloud_cover': cloud_cover,
                'sensor_inclination_angle': sensor_inclination_angle,
                'sensor_viewing_angle': sensor_viewing_angle,
                'original_product_id': original_product_id,
                'unique_product_id': dims_product_id,
                'spatial_resolution_x': spatial_resolution_x,
                'spatial_resolution_y': spatial_resolution_y,
                'spatial_resolution': spatial_resolution,
                'product_profile': product_profile,
                'product_acquisition_start': start_date_time,
                'product_acquisition_end': end_date_time,
                'product_date': center_date_time,
                'path': path,
                'row': row,
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
                #original_product_id is not necessarily unique
                #so we use product_id
                log_message(('Already in catalogue: updating %s.'
                            % original_product_id), 2)
                product = OpticalProduct.objects.get(
                    original_product_id=original_product_id
                ).getConcreteInstance()
                new_record_flag = False
                update_message = product.ingestion_log
                update_message += '\n'
                update_message += '%s : %s - updating record' % (
                    time_stamp, ingestor_version)
                data['ingestion_log'] = update_message
                product.__dict__.update(data)
                log_message('Updated %s' % original_product_id, 1)
            except ObjectDoesNotExist:
                log_message('Creating %s' % original_product_id, 2)
                update_mode = False
                create_message = '%s : %s - creating record' % (
                    time_stamp, ingestor_version)
                data['ingestion_log'] = create_message
                try:
                    product = OpticalProduct(**data)
                    log_message('Creating %s' % original_product_id, 1)

                except Exception, e:
                    log_message(e.message, 2)

                new_record_flag = True
            except MultipleObjectsReturned, e:
                print (
                    'There are more than one products with '
                    'original_product_id of %s' % original_product_id)
                raise e

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

                    if download_thumbs_flag:
                        # Download original jpeg thumbnail and
                        # creates a thumbnail
                        new_name = '%s.jpg' % product.original_product_id
                        handle = open(new_name, 'wb+')
                        thumbnail = urllib2.urlopen(feature.get('URL_QL'))
                        handle.write(thumbnail.read())
                        thumbnail.close()
                        handle.close()
                        # Transform and store .wld file
                        log_message('Referencing thumb', 2)
                        # noinspection PyBroadException
                        try:
                            path = product.georeferencedThumbnail()
                            log_message('Georeferenced Thumb: %s' % path, 2)
                        except:
                            traceback.print_exc(file=sys.stdout)
                    else:
                        # user opted not to ingest thumbs immediately
                        # only set the thumb url if it is a new product
                        # as existing products may already have cached a
                        # copy
                        if new_record_flag:
                            product.remote_thumbnail_url = (
                                feature.get('URL_QL'))
                            product.save()

                if new_record_flag:
                    log_message('Product %s imported' % record_count, 2)
                    pass
                else:
                    log_message('Product %s updated' % updated_record_count, 2)
                    pass
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                raise CommandError('Cannot import: %s' % e)

            log_message('Imported scene : %s' % original_product_id, 2)
            if test_only_flag:
                transaction.rollback()
                log_message('Testing only: transaction rollback.', 2)
            else:
                transaction.commit()

        except Exception, e:
            # if original_product_id == '51194111302060828412B':
            #     print e
            #     raise e
            log_message('Record import failed. AAAAAAARGH! : %s' %
                        original_product_id, 0)
            failed_record_count += 1
            if halt_on_error_flag is True:
                print 'Halt on error flag was set to %s ' % halt_on_error_flag
                print e.message
                break
            else:
                continue

    lock_file.release()
    print '==============================='
    print 'Products processed : %s ' % record_count
    print 'Products skipped (H and COLOR T): %s ' % skipped_record_count
    print 'Products updated : %s ' % updated_record_count
    print 'Products imported : %s ' % created_record_count
    print 'Products failed to import : %s ' % failed_record_count
    print '==============================='
    print 'Notes:'
    print 'The SPOT IMAGE Catalog shapefile may contain duplicate products'
    print 'For example 51174181401200819562J (from 2014 shapefile) has'
    print 'two MODE COLOR, TYPE J images. There are small differences between'
    print 'the geometries of the duplicate records for this scene but'
    print 'the scenes are the same. For this reason it is quite likely to get'
    print 'updated records in the report above even if you have never imported'
    print 'records from this time period before.'
