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

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__version__ = '0.1'
__date__ = '29/01/2014'
__copyright__ = 'South African National Space Agency'

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
    SatelliteInstrumentGroup)

from catalogue.models import (
    OpticalProduct,
    Projection,
    Quality)
from mercurial import lock, error
from django.core.management.base import CommandError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.gdal import DataSource

from ..models import (
    Quality,
    License,
    CreatingSoftware,
    Institution,
    OpticalProduct,
)
from dictionaries.models import Satellite


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

    image_date = datetime(
        int(date_parts[2][-2:]),  # year
        int(date_parts[1]),  # month
        int(date_parts[0]),  # day
        int(time_parts[0]),  # hour
        int(time_parts[1]),  # minutes
        int(time_parts[2]))  # seconds

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
    satellite_number = feature.get('SATEL')
    if not int(satellite_number) in (1, 2, 3, 4, 5):
        raise CommandError(
            'Unknown Spot mission number'
            '(should be 1-5) %s.' % satellite_number)

    mission_value = 'S%s' % satellite_number
    satellite = Satellite.objects.get(abbreviation=mission_value)

    abbreviation = None
    if satellite_number in [1, 2, 3]:
        abbreviation = 'HRV'
    elif satellite_number == 4:
        abbreviation = 'HRVIR'
    elif satellite_number == 5:
        abbreviation = 'HRG'

    instrument_type = InstrumentType.objects.get(
        operator_abbreviation=abbreviation)

    abbreviation = None
    # If it is a spot 1,2 or three assume the sensor type
    # is HRV-1 or HRV-2 or HRV-3.
    if satellite_number in [1, 2, 3]:
        abbreviation = 'HRV-%s' % satellite_number
    # If it is a spot 4 image then assume the sensor type
    # is HIR
    elif satellite_number == 4:
        abbreviation = 'HRVIR-4'
    # If it is a spot 5 image then assume the sensor type
    # is a HRG
    elif satellite_number == 5:
            abbreviation = 'HRG-5'

    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception, e:
        print e.message
        raise e
    log_message('Satellite Instrument Group %s' %
                satellite_instrument_group, 2)

    # Note that in SPOT you may get more that one instrument
    # groups matched. When the time comes you will need to add more filtering
    # rules to ensure that you end up with only one instrument group.
    # For the mean time, we can assume that SPOT will return only one.

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


def skip_record(feature):
    """Determine if this feature should be skipped.

    :param feature: A shapefile feature.
    :type feature: Feature

    :returns: True if the feature should be skipped.
    :rtype: bool
    """
    # work out the sensor type
    spectral_mode_string = feature.get('TYPE')
    # Some additional rules from Linda to skip unwanted records
    colour_mode = feature.get('MODE')
    if spectral_mode_string == 'H':
        return True

    elif spectral_mode_string == 'T' and colour_mode == 'COLOR':
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
        raise(
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

    for myPolygon in data_source[0]:
        if area_of_interest is None:
            yield myPolygon
        else:
            if area_of_interest.intersects(myPolygon.geom):
                yield myPolygon

@transaction.commit_manually
def ingest(
        shapefile,
        download_thumbs=False,
        area_of_interest=None,
        test_only_flag=True,
        verbosity_level=2,
        halt_on_error_flag=True):
    """
    Ingest a collection of Spot scenes from a shapefile.

    Understanding SPOT a21 scene id:
    Concerning the SPOT SCENE products, the name will be
    the string 'SCENE ' followed by 'formated A21 code'.
    e.g. 41573401101010649501M
    e.g. 4 157 340 11/01/01 06:49:50 1 M
    Formated A21 code is defined as :
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

    :param download_thumbs: Whether thumbs should be retrieved. If they are not
        fetched on ingestion, they will be fetched on demand as searches are
        made.

    :param area_of_interest: A geometry in well known text (WKT) defining which
        features to include.

    :param test_only_flag: Whether to do a dummy run ( database will not be
        updated. Default False.

    :param verbosity_level: How verbose the logging output should be. 0-2
        where 2 is very very very very verbose! Default is 1.

    :param halt_on_error_flag: Whather we should stop processing when the first
        error is encountered. Default is True.
    """
    def log_message(message, level=1):
        """Log a message for a given leven.

        :param message: A message.
        :param level: A log level.
        """
        if verbosity_level >= level:
            print message

    try:
        lockfile = lock.lock('/tmp/spot_harvest.lock', timeout=60)
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

        if skip_record():
            skipped_record_count += 1
            continue

        try:
            log_message('', 2)
            log_message('---------------', 2)
            log_message('Ingesting %s' % feature, 2)

            # First grab all the generic properties that any scene will have...

            original_product_id = feature.get('A21')
            log_message('Product Number: %s' % original_product_id, 2)

            geometry = feature.geom.geos

            start_date_time, center_date_time, end_date_time = get_dates(
                log_message, feature)

            # projection for GenericProduct
            #print specific_parameters.toxml()
            projection = get_projection(feature)
            log_message('Projection: %s' % projection, 2)

            # Band count for GenericImageryProduct
            band_count = band_count(feature)
            log_message('Band count: %s' % band_count, 2)

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
            path = feature.get('a21')[1:4].rjust(4, '0'),
            log_message('Path: %s' % path, 2)

            # row for GenericSensorProduct
            row = feature.get('a21')[4:7].rjust(4, '0')
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

            # ProductProfile for OpticalProduct
            product_profile = get_product_profile(
                log_message, specific_parameters)

            # Get the original text file metadata
            metadata = '\n'.join(['%s=%s' % (
                f, feature.get(f)) for f in feature.fields])
            log_message('Metadata retrieved', 2)

            # Metadata comes from shpfile dump not DIMS...
            dims_product_id = None

            log_message('DIMS product ID: %s' % dims_product_id)
            # Check if there is already a matching product based
            # on original_product_id

            # Do the ingestion here...
            data = {
                'metadata': metadata,
                'spatial_coverage': geometry,
                'radiometric_resolution': radiometric_resolution,
                'band_count': band_count,
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

                    jpeg_path = os.path.join(str(myFolder), '*.jpeg')
                    log_message(jpeg_path, 2)
                    jpeg_path = glob.glob(jpeg_path)[0]
                    new_name = '%s.jpg' % product.original_product_id
                    shutil.copyfile(
                        jpeg_path,
                        os.path.join(thumbs_folder, new_name))
                    # Transform and store .wld file
                    log_message('Referencing thumb', 2)
                    try:
                        path = product.georeferencedThumbnail()
                        log_message('Georeferenced Thumb: %s' % path, 2)
                    except:
                        traceback.print_exc(file=sys.stdout)

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
    print 'Products skipped : %s ' % skipped_record_count
    print 'Products updated : %s ' % updated_record_count
    print 'Products imported : %s ' % created_record_count
    print 'Products failed to import : %s ' % failed_record_count
    print '==============================='
