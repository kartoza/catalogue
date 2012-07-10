"""
SPOT harvesting

Tool for harvesting catalogue records from SPOT coverage maps

http://catalog.spotimage.com

From the menu of above site, go:

My Searches - Download of Coverages

This script is written based on the Africa* shp coverages,
though it should work on others too.

Tim Sutton May 2011

Sample data from one record:
  wkt_geom   POLYGON((5.381600 15.316700,5.507500 15.847000,6.055500 15.725200,5.928300 15.195200,5.381600 15.316700))
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
  URL_QL     http://sirius.spotimage.fr/url/catalogue.aspx?ID=-1&ACTION=Scenes%3AgetQuicklook&CODEA21=50673191101191017402J&SEGMENT=6524011&SAT=0



"""

import os
from optparse import make_option
import tempfile
import subprocess
from mercurial import lock, error

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.geometries import Polygon

from catalogue.models import *
from catalogue.dims_lib import dimsWriter
import traceback


# Hardcoded constants
PROJECTION            = 'ORBIT'
RADIOMETRIC_RESOLUTION= 16
MISSION_SENSOR        = 'REI'
GEOMETRIC_RESOLUTION  = 5
PRODUCT_ACQUISITION_START_TIME = '0900'
SOLAR_ZENITH_ANGLE    = 0
SOLAR_AZIMUTH_ANGLE   = 0


def get_row_path_from_polygon(poly, as_int=False, no_compass=False):
    """
    Given a polygon, returns row, row_shift, path, path_shift
    informations of the centroid as a string
    As indicated in the docs (8.1.3)
    """
    path, path_shift = ("%.2f" % poly.centroid.x).split('.')
    row, row_shift = ("%.2f" % poly.centroid.y).split('.')
    if as_int:
        return int(path), int(path_shift), int(row), int(row_shift)
    if no_compass:
        return path, path_shift, row, row_shift
    if poly.centroid.x < 0:
        path = "%sW" % path
    else:
        path = "%sE" % path
    if poly.centroid.y < 0:
        row = "%sS" % row
    else:
        row = "%sN" % row
    return path, path_shift, row, row_shift

class Command(BaseCommand):
    help = "Imports RapidEye packages into the SAC catalogue"
    option_list = BaseCommand.option_list + (
        make_option('--file', '-f', dest='shapefile', action='store',
            help='Shapefile containing spot coverage data.', default=False),
        make_option('--download-thumbs', '-d', dest='download_thumbs', action='store',
            help='Whether thumbnails should be fetched to. If not fetched now they will be fetched on demand as needed.', default=False),
        make_option('--test_only', '-t', dest='test_only', action='store_true',
            help='Just test, nothing will be written into the DB.', default=False),
        make_option('--owner', '-o', dest='owner', action='store',
            help='Name of the Institution package owner. Defaults to: Rapideye AG.', default='Rapideye AG'),
        make_option('--creating_software', '-s', dest='creating_software', action='store',
            help='Name of the creating software. Defaults to: Unknown.', default='Unknown'),
        make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
            help='Name of the license. Defaults to: SAC Commercial License'),
        make_option('--area', '-a', dest='area', action='store',
            help='Area of interest, images which are external to this area will not be imported (WKT Polygon, SRID=4326)'),
        make_option('--quality', '-q', dest='quality', action='store',
            help='Quality code (will be created if does not exists). Defaults to: Unknown', default='Unknown'),
        make_option('--processing_level', '-r', dest='processing_level', action='store',
            help='Processing level code (will be created if does not exists). Defaults to: 1B', default='1B'),
    )

    @staticmethod
    def fetch_geometries(shapefile, area_of_interest):
        """
        Download the index and parses it, returns a generator list of features
        """
        try:
            print( "Opening %s" % shapefile )
            data_source = DataSource( shapefile )
        except Exception, e:
            raise CommandError("Loading index failed %s" % e)

        for pt in data_source[0]:
            if not area_of_interest or area_of_interest.intersects(pt.geom):
                yield pt


    @transaction.commit_manually
    def handle(self, *args, **options):
        """ command execution """
        def verblog(msg, level=1):
            if verbose >= level:
                print msg

        try:
            lockfile = lock.lock("/tmp/spot_harvest.lock", timeout=60)
        except error.LockHeld:
            # couldn't take the lock
            raise CommandError, 'Could not acquire lock.'

        shapefile             = options.get('shapefile')
        download_thumbs       = options.get('download_thumbs')
        test_only             = options.get('test_only')
        verbose               = int(options.get('verbosity'))
        license               = options.get('license')
        owner                 = options.get('owner')
        software              = options.get('creating_software')
        area                  = options.get('area')
        quality               = options.get('quality')
        processing_level      = options.get('processing_level')

        # Hardcoded
        projection            = PROJECTION
        radiometric_resolution= RADIOMETRIC_RESOLUTION
        mission_sensor        = MISSION_SENSOR
        solar_zenith_angle    = SOLAR_ZENITH_ANGLE
        solar_azimuth_angle   = SOLAR_AZIMUTH_ANGLE


        area_of_interest  = None


        verblog('Getting verbose (level=%s)... ' % verbose, 2)
        if test_only:
            verblog('Testing mode activated.', 2)

        try:
            # Validate area_of_interest
            if area:
                try:
                    area_of_interest = Polygon(area)
                    if not area_of_interest.area:
                        raise CommandError('Unable to create the area of interest polygon: invalid polygon.')
                    if not area_of_interest.geom_type.name == 'Polygon':
                        raise CommandError('Unable to create the area of interest polygon: not a polygon.')
                except Exception, e:
                    raise CommandError('Unable to create the area of interest polygon: %s.' % e)
                verblog('Area of interest filtering activated.', 2)

            # Get the params
            try:
                software = CreatingSoftware.objects.get_or_create(name=software, defaults={'version': 0})[0]
            except CreatingSoftware.DoesNotExist:
                raise CommandError, 'Creating Software %s does not exists and cannot create: aborting' % software
            try:
                license = License.objects.get_or_create(name=license, defaults={'type': License.LICENSE_TYPE_COMMERCIAL, 'details': license})[0]
            except License.DoesNotExist:
                raise CommandError, 'License %s does not exists and cannot create: aborting' % license

            try:
                owner = Institution.objects.get_or_create(name=owner, defaults={'address1': '','address2': '','address3': '','post_code': '', })[0]
            except Institution.DoesNotExist:
                verblog('Institution %s does not exists and cannot be created.' % owner, 2)
                raise CommandError, 'Institution %s does not exists and cannot create: aborting' % owner

            try:
                quality = Quality.objects.get_or_create(name=quality)[0]
            except Quality.DoesNotExist:
                verblog('Quality %s does not exists and cannot be creates, it will be read from metadata.' % quality, 2)
                raise CommandError, 'Quality %s does not exists and cannot be created: aborting' % quality

            try:
                imported = 0
                updated = 0
                created = 0
                verblog('Starting index dowload...', 2)
                for package in Command.fetch_geometries(shapefile, area_of_interest):
                    #if imported > 5:
                    #  transaction.commit()
                    #  return
                    if imported % 10000 == 0 and imported > 0:
                        print "Products processed : %s " % imported
                        print "Products updated : %s " % updated
                        print "Products imported : %s " % created
                        transaction.commit()
                    verblog("Ingesting %s" % package, 2)

                    # Understanding SPOT a21 scene id:
                    # Concerning the SPOT SCENE products, the name will be the string 'SCENE ' followed by 'formated A21 code'.
                    # e.g. 41573401101010649501M
                    # e.g. 4 157 340 11/01/01 06:49:50 1 M
                    # Formated A21 code is defined as : N KKK-JJJ YY/MM/DD HH:MM:SS I C
                    # (with N: Satellite number, KKK-JJJ :
                    #  GRS coordinates, YY/MM/DD :
                    #  Center scene date, HH:MM:SS :
                    #  Center scene time, I :
                    #  Instrument number (1,2), C :
                    #  Sensor Code (P, M, X, I, J, A, B, S, T, M+X, M+I).
                    #  For shift along the track products, SAT value is added after KKK-JJJ info : '/SAT' (in tenth of scene (0 to 9))
                    # http://www.spotimage.com/dimap/spec/dictionary/Spot_Scene/DATASET_NAME.htm
                    # Some of these data are explicitly defined in fields in the catalogue shp dumps so
                    # we dont try to parse everthing from the a21 id

                    original_id = package.get('A21')
                    # Gets the mission
                    mission_id = package.get('SATEL')
                    if not int(mission_id) in (1,2,3,4,5):
                        raise CommandError('Unknown Spot mission number (should be 1-5) %s.' % mission_id)
                    try:
                        mission_abbreviation = "SPOT-%s" % mission_id
                        spot_mission = Mission.objects.get( operator_abbreviation = mission_abbreviation )
                        mission_sensors = MissionSensor.objects.filter( mission=spot_mission )
                        # work out the sensor type
                        myType = package.get('TYPE')
                        # The type abbreviation should be unique for its sensor so we chain two filters to get it
                        myTypes = SensorType.objects.filter( mission_sensor__in=mission_sensors ).filter( operator_abbreviation = myType )
                        sensor_type = None
                        if myTypes.count() < 1:
                            verblog("Autoadding unmatched sensor type: %s" % myType,0)
                            sensor_type = SensorType()
                            sensor_type.abbreviation = myType
                            sensor_type.name = myType
                            sensor_type.operator_abbreviation = myType
                            #  Assume the first sensor for the mission - mayneed manual correction afterwards
                            sensor_type.mission_sensor = mission_sensors[0]
                            sensor_type.save()
                            myMode = AcquisitionMode()
                            myMode.sensor_type = sensor_type
                            myMode.abbreviation = str(spot_mission.abbreviation) + "C1"
                            myMode.name = "Camera 1"
                            myMode.geometric_resolution = 0
                            myMode.band_count = 0
                            myMode.is_grayscale = 0
                            myMode.operator_abbreviation = str(spot_mission.abbreviation) + "C1"
                            myMode.save()
                            myMode2 = AcquisitionMode()
                            myMode2.sensor_type = sensor_type
                            myMode2.abbreviation =  str(spot_mission.abbreviation) + "C2"
                            myMode2.name = "Camera 2"
                            myMode2.geometric_resolution = 0
                            myMode2.band_count = 0
                            myMode2.is_grayscale = 0
                            myMode2.operator_abbreviation = str(spot_mission.abbreviation) + "C2"
                            myMode2.save()
                        else:
                            sensor_type = myTypes[0]
                        # The mode should be unique for its type so we chain two filters to get it
                        myMode = "S%sC%s" % ( mission_id, package.get('A21')[-2:-1] )
                        acquisition_mode = AcquisitionMode.objects.filter( sensor_type=sensor_type ).filter( operator_abbreviation=myMode )[0]
                        #
                        # Following for debugging info only
                        #
                        verblog("Detected mission: %s" % spot_mission ,2)
                        verblog("Allowed sensors:",2)
                        for mySensor in mission_sensors:
                            verblog(mySensor,2) #.operator_abbreviation
                        verblog("Detected sensor type: %s" % sensor_type, 2 )
                        verblog("Detected acquisition mode: %s" % acquisition_mode, 2)
                        #
                        # Debugging output ends
                        #
                    except:
                        traceback.print_exc(file=sys.stdout)
                        continue
                    band_count            = 0;
                    date_parts = package.get('DATE_ACQ').split('/') # e.g. 20/01/2011
                    time_parts = package.get('TIME_ACQ').split(':') # e.g. 08:29:01
                    # Fills the the product_id
                    #SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN
                    product_id = "%(SAT)s_%(SEN)s_%(TYP)s_%(MOD)s_%(KKKK)s_%(KS)s_%(JJJJ)s_%(JS)s_%(YYMMDD)s_%(HHMMSS)s_%(LEVL)s_%(PROJTN)s" % \
                    {
                      'SAT': spot_mission.abbreviation.ljust(3, '-'),
                      'SEN': sensor_type.mission_sensor.abbreviation.ljust(3, '-'),
                      'TYP': sensor_type.abbreviation.ljust(3, '-'),
                      'MOD': acquisition_mode.abbreviation.ljust(4, '-'),
                      'KKKK': package.get('a21')[1:4].rjust(4, '0'),
                      'KS': '00',
                      'JJJJ': package.get('a21')[4:7].rjust(4, '0'),
                      'JS': '00',
                      'YYMMDD': date_parts[2][-2:]+date_parts[1]+date_parts[0],
                      'HHMMSS': time_parts[0]+time_parts[1]+time_parts[2],
                      'LEVL' : processing_level.ljust(4, '-'),
                      'PROJTN': projection.ljust(6, '-')
                    }
                    assert len(product_id) == 58, 'Wrong len in product_id : %s' % product_id

                    verblog("Product ID %s" % product_id, 2)

                    # Do the ingestion here...
                    data = {
                      'metadata': '\n'.join(["%s=%s" % (f,package.get(f)) for f in package.fields]),
                      'spatial_coverage': package.geom.geos,
                      'product_id': product_id,
                      'radiometric_resolution': radiometric_resolution,
                      'band_count': band_count,
                      'cloud_cover': int(package.get('CLOUD_PER')), # integer percent
                      'owner': owner,
                      'license': license,
                      'creating_software': software,
                      'quality': quality,
                      'sensor_inclination_angle': package.get('ANG_INC'),
                      'sensor_viewing_angle': package.get('ANG_ACQ'),
                      'original_product_id': package.get('A21'),
                      'solar_zenith_angle': solar_zenith_angle,
                      'solar_azimuth_angle': solar_azimuth_angle,
                      'spatial_resolution_x': package.get('RESOL'),
                      'spatial_resolution_y': package.get('RESOL'),
                    }
                    verblog(data, 2)

                    # Check if it's already in catalogue:
                    try:
                        op = OpticalProduct.objects.get(product_id=data.get('product_id')).getConcreteInstance()
                        verblog('Already in catalogue: updating.', 2)
                        is_new = False
                        updated += 1
                        op.__dict__.update(data)
                    except ObjectDoesNotExist:
                        op = OpticalProduct(**data)
                        verblog('Not in catalogue: creating.', 2)
                        is_new = True
                        created += 1
                        try:
                            op.productIdReverse(True)
                        except Exception, e:
                            raise CommandError('Cannot get all mandatory data from product id %s (%s).' % (product_id, e))
                    verblog("Saving product and setting thumb", 2)
                    try:
                        op.save()
                        if test_only:
                            verblog('Testing: image not saved.', 2)
                        else:
                            if download_thumbs:
                                # Store thumbnail
                                thumbnails_folder = os.path.join(settings.THUMBS_ROOT, op.thumbnailDirectory())
                                try:
                                    os.makedirs(thumbnails_folder)
                                except:
                                    pass
                                # Download original jpeg thumbnail and creates a thumbnail
                                downloaded_thumb = os.path.join(thumbnails_folder, op.product_id + ".jpg")
                                handle = open(downloaded_thumb, 'wb+')
                                thumbnail = urllib2.urlopen(package.get('URL_QL'))
                                handle.write(thumbnail.read())
                                thumbnail.close()
                                handle.close()
                                # Transform and store .wld file
                                verblog('Referencing thumb',2)
                                try:
                                    op.georeferenceThumbnail()
                                except:
                                    traceback.print_exc(file=sys.stdout)
                            else:
                                # user opted not to ingest thumbs immediately
                                # only set the thumb url if it is a new product
                                # as existing products may already have cached a copy
                                if is_new:
                                    op.remote_thumbnail_url = package.get('URL_QL')
                                    op.save()
                        if is_new:
                            verblog('Product %s imported.' % product_id, 1)
                        else:
                            verblog('Product %s updated.' % product_id, 1)
                        imported = imported + 1
                    except Exception, e:
                        traceback.print_exc(file=sys.stdout)
                        raise CommandError('Cannot import: %s' % e)

                verblog("%s packages imported" % imported)

                if test_only:
                    transaction.rollback()
                    verblog("Testing only: transaction rollback.")
                else:
                    transaction.commit()
                    verblog("Committing transaction.", 2)
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                raise CommandError('Uncaught exception (%s): %s' % (e.__class__.__name__, e))
        except Exception, e:
            verblog('Rolling back transaction due to exception.')
            if test_only:
                from django.db import connection
                verblog(connection.queries)
            transaction.rollback()
            raise CommandError("%s" % e)
        finally:
            lockfile.release()
