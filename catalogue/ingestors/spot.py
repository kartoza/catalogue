"""
SANSA-EO Catalogue - Initialization, generic and helper methods

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import os

from django.core.management.base import CommandError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal.geometries import Polygon
from django.contrib.gis.gdal import DataSource
from catalogue.models import *
from mercurial import lock, error
import traceback


@transaction.commit_manually
def ingest(theShapeFile,
           myDownloadThumbsFlag = False,
           theTestOnlyFlag = False,
           theVerbosityLevel = 1,
           theLicense = 'SANSA Commercial License',
           theOwner = 'Astrium',
           theSoftware = 'TS5',
           theArea = None,
           theQuality = 'Unknown',
           # We should use 1A here but we need to write migration
           # logic for all existing records and rename all existing thumbs!
           theProcessingLevel = '1B'):
    """
    Ingest a SPOT dataset as provided by spot image

    Args:
        theShapefile - (Required) A shapefile downloaded from
           http://catalog.spotimage.com/pagedownload.aspx
        myDownloadThumbsFlag = (Optional) Defaults to False. Whether thumbs
           should be retrieved. If they are not fetched on ingestion, they
           will be fetched on demand as searches are made.
        theTestOnlyFlag - (Optional) Defaults to False. Whether to do a dummy
           run (database will not be updated).
        theVerboseFlag - (Optional) Defaults to 1. How verbose the logging
           output should be. 0-2 where 2 is very very very very verbose!
        theLicense - (Optional) Defaults to 'SANSA Commercial License', License
           holder of the product.
        theOwner - (Optional) Defaults to 'Astrium', Original provider / owner
           of the data.
        theSoftware - (Optional) Defaults to 'TS5', The software used to create
           / extract the product.
        theArea -(Optional) A geometry defining which features to include.
        theQuality - (Optional) Defaults to 'Unknown', A quality assessment for
           these images. Note from Tim & Linda: This doesnt really make sense!
           TODO: Remove this parameter?
        theProcessingLevel = '1B'
    Returns:
        None
    Exceptions:
        Any unhandled exceptions will be raised.
    """

    def logMessage(theMessage, theLevel=1):
        if theVerbosityLevel >= theLevel:
            print theMessage

    print 'Importing with owner: %s' % theOwner
    try:
        lockfile = lock.lock('/tmp/spot_harvest.lock', timeout=60)
    except error.LockHeld:
        # couldn't take the lock
        raise CommandError, 'Could not acquire lock.'

    # Hardcoded
    myProjection = 'ORBIT'
    myRadiometricResolution= 8
    mySolarZenithAngle = 0
    mySolarAzimuthAngle = 0

    myAreaOfInterest  = None

    logMessage('Getting verbose (level=%s)... ' % theVerbosityLevel, 2)
    if theTestOnlyFlag:
        logMessage('Testing mode activated.', 2)
        pass

    try:
        # Validate area_of_interest
        if theArea is not None:
            try:
                myAreaOfInterest = Polygon(theArea)
                if not myAreaOfInterest.area:
                    raise CommandError('Unable to create the area of interest'
                                        ' polygon: invalid polygon.')
                if not myAreaOfInterest.geom_type.name == 'Polygon':
                    raise CommandError('Unable to create the area of interest'
                                        ' polygon: not a polygon.')
            except Exception, e:
                raise CommandError('Unable to create the area of interest'
                                    ' polygon: %s.' % e)
            logMessage('Area of interest filtering activated.', 2)

        # Get the params
        try:
            theSoftware = CreatingSoftware.objects.get_or_create(
                name=theSoftware, defaults={'version': 0})[0]
        except CreatingSoftware.DoesNotExist:
            raise CommandError, ('Creating Software %s does not exists '
                                 ' and cannot create: aborting' % theSoftware)
        # Get the license
        try:
            theLicense = License.objects.get_or_create(
                name=theLicense,
                defaults={'type': License.LICENSE_TYPE_COMMERCIAL,
                          'details': theLicense})[0]
        except License.DoesNotExist:
            raise CommandError, ('License %s does not exists and cannot '
                                 ' create: aborting' % theLicense)
        # Get the owner
        try:
            myOwner = Institution.objects.get_or_create(
                name=theOwner,
                defaults={'address1': '',
                          'address2': '',
                          'address3': '',
                          'post_code': '', })[0]
        except Institution.DoesNotExist:
            #logMessage('Institution %s does not exists and '
            #         'cannot be created.' % owner, 2)
            raise CommandError, ('Institution %s does not exist and '
                                  'cannot create: aborting' % theOwner)
        try:
            theQuality = Quality.objects.get_or_create(name=theQuality)[0]
        except Quality.DoesNotExist:
            logMessage('Quality %s does not exists and cannot be created,'
                       ' it will be read from metadata.' % theQuality, 2)
            raise CommandError, ('Quality %s does not exists and cannot '
                                 ' be created: aborting' % theQuality)

        try:
            myRecordCount = 0
            myUpdatedRecordCount = 0
            myCreatedRecordCount = 0
            myDiscardedRecordCount = 0
            logMessage('Starting index dowload...', 2)
            for myPackage in fetchGeometries(theShapeFile, myAreaOfInterest):
                #if imported > 5:
                #  transaction.commit()
                #  return
                if (myRecordCount % 10000 == 0 and
                    myRecordCount > 0):
                    print 'Products processed : %s ' % myRecordCount
                    print 'Products updated : %s ' % myUpdatedRecordCount
                    print 'Products imported : %s ' % myCreatedRecordCount
                    transaction.commit()
                logMessage('Ingesting %s' % myPackage, 2)
                myRecordCount += 1
                # Understanding SPOT a21 scene id:
                # Concerning the SPOT SCENE products, the name will be
                # the string 'SCENE ' followed by 'formated A21 code'.
                # e.g. 41573401101010649501M
                # e.g. 4 157 340 11/01/01 06:49:50 1 M
                # Formated A21 code is defined as :
                # N KKK-JJJ YY/MM/DD HH:MM:SS I C
                # (with N: Satellite number, KKK-JJJ :
                #  GRS coordinates, YY/MM/DD :
                #  Center scene date, HH:MM:SS :
                #  Center scene time, I :
                #  Instrument number (1,2), C :
                #  Sensor Code (P, M, X, I, J, A, B, S, T, M+X, M+I).
                #  For shift along the track products, SAT value is added
                # after KKK-JJJ info : '/SAT' (in tenth of scene (0 to 9))
                # http://www.spotimage.com/dimap/spec/dictionary/
                #    Spot_Scene/DATASET_NAME.htm
                # Some of these data are explicitly defined in fields in the
                # catalogue shp dumps so
                # we dont try to parse everthing from the a21 id

                myOriginalProductId = myPackage.get('A21')
                # Gets the mission
                myMissionId = myPackage.get('SATEL')
                if not int(myMissionId) in (1,2,3,4,5):
                    raise CommandError('Unknown Spot mission number'
                                       '(should be 1-5) %s.' % myMissionId)
                try:
                    #sac=# select * from catalogue_mission where
                    #       operator_abbreviation = 'SPOT-5';
                    #-[ RECORD 1 ]---------+----------------------------------
                    # id                    | 18
                    # abbreviation          | S5
                    # name                  | Systeme Pour l'Observation de e 5
                    # mission_group_id      | 1
                    # owner                 | CNES
                    # operator_abbreviation | SPOT-5

                    myMissionAbbreviation = 'SPOT-%s' % myMissionId
                    mySpotMission = Mission.objects.get(
                        operator_abbreviation = myMissionAbbreviation)

                    #sac=# select * from catalogue_missionsensor where
                    #             mission_id = 18;
                    #-[ RECORD 1 ]---------+----------------------------------
                    #id                    | 10
                    #abbreviation          | HRG
                    #name                  |   SPOT 5 HRG
                    #description           | High Resolution Geometric Spot 5
                    #has_data              | t
                    #mission_id            | 18
                    #is_taskable           | t
                    #is_radar              | f
                    #operator_abbreviation | HRG-5
                    #-[ RECORD 2 ]---------+----------------------------------
                    #id                    | 26
                    #abbreviation          | HRS
                    #name                  | SPOT 5 HRS Stereo
                    #description           | High Resolution Stereoscopic Spot 5
                    #has_data              | f
                    #mission_id            | 18
                    #is_taskable           | t
                    #is_radar              | f
                    #operator_abbreviation | HRS-5
                    #-[ RECORD 3 ]---------+----------------------------------
                    #id                    | 27
                    #abbreviation          | VMI
                    #name                  | VEGETATION-5
                    #description           | Vegetation Monitoring Instrument
                    #                           / Vegetation Spot 5
                    #has_data              | f
                    #mission_id            | 18
                    #is_taskable           | t
                    #is_radar              | f
                    #operator_abbreviation | Vegetation-5

                    myMissionSensors = MissionSensor.objects.filter(
                        mission=mySpotMission)

                    #sac=# select * from catalogue_sensortype where
                    # mission_sensor_id in (10, 26, 27) and
                    # operator_abbreviation = 'A';
                    #-[ RECORD 1 ]---------+-------------
                    #id                    | 40
                    #abbreviation          | A
                    #name                  | Panchromatic
                    #mission_sensor_id     | 10
                    #operator_abbreviation | A


                    # work out the sensor type
                    myType = myPackage.get('TYPE')

                    # Some additional rules from Linda to skip unwanted records
                    myColourMode = myPackage.get('MODE')
                    if myType == 'H':
                        myDiscardedRecordCount += 1
                        continue
                    if myType == 'T' and myColourMode == 'COLOR':
                        myDiscardedRecordCount += 1
                        continue

                    if myType in ['J', 'I']:  # Spot 4 and 5 only
                        myBandCount = 4
                        myGrayScaleFlag = False
                    elif myType in ['M', 'A', 'B', 'T']: # Spot 4 and 5 only
                        myBandCount = 1
                        myGrayScaleFlag = True
                    elif myType in ['X']:  # Spot 1,2 or 3 only
                        myBandCount = 3
                        myGrayScaleFlag = False
                    elif myType in ['P']:
                        myBandCount = 1
                        myGrayScaleFlag = True
                    else:
                        # not recognised
                        continue

                    # The type abbreviation should be unique for its sensor
                    # so we chain two filters to get it
                    myTypes = SensorType.objects.filter(
                        mission_sensor__in=myMissionSensors).filter(
                        operator_abbreviation = myType)

                    if myTypes.count() < 1:
                        logMessage('Autoadding unmatched sensor type: %s' %
                                  myType, 0)
                        mySensorType = SensorType()
                        mySensorType.abbreviation = myType
                        mySensorType.name = myType
                        mySensorType.operator_abbreviation = myType
                        # Assume the first sensor for the mission -
                        # may need manual correction afterwards

                        # TODO:
                        # If it is a spot 1,2 or three assume the sensor type
                        # is HRV-1 or HRV-2 or HRV-3.

                        # If it is a spot 4 image then assume the sensor type
                        # is HIR

                        # If it is a spot 5 image then assume the sensor type
                        # is a HRG

                        mySensorType.mission_sensor = myMissionSensors[0]
                        mySensorType.save()

                        # Make sure we have acquisition modes for lookup later
                        myResolution = myPackage.get('RESOL')
                        # Create a new acquisition mode for camera 1 on this
                        # sensortype
                        myMode = AcquisitionMode()
                        myMode.sensor_type = mySensorType
                        myMode.abbreviation = str(
                            mySpotMission.abbreviation) + 'C1'
                        myMode.name = 'Camera 1'
                        myMode.geometric_resolution = myResolution
                        myMode.band_count = myBandCount
                        myMode.is_grayscale = myGrayScaleFlag
                        myMode.operator_abbreviation = str(
                            mySpotMission.abbreviation) + 'C1'
                        myMode.save()

                        # Create a new acquisition mode for camera 2 on this
                        # sensortype
                        myMode2 = AcquisitionMode()
                        myMode2.sensor_type = mySensorType
                        myMode2.abbreviation =  str(
                            mySpotMission.abbreviation) + 'C2'
                        myMode2.name = 'Camera 2'
                        myMode.geometric_resolution = myResolution
                        myMode.band_count = myBandCount
                        myMode.is_grayscale = myGrayScaleFlag
                        myMode2.operator_abbreviation = str(
                            mySpotMission.abbreviation) + 'C2'
                        myMode2.save()
                    else:
                        mySensorType = myTypes[0]
                    # The mode should be unique for its type so we
                    # chain two filters to get it
                    myMode = 'S%sC%s' % (
                        myMissionId, myPackage.get('A21')[-2:-1] )
                    acquisition_mode = AcquisitionMode.objects.filter(
                        sensor_type=mySensorType
                    ).filter(
                        operator_abbreviation=myMode)[0]
                    #
                    # Following for debugging info only
                    #
                    logMessage('Detected mission: %s' % mySpotMission, 2)
                    logMessage('Allowed sensors:', 2)
                    for mySensor in myMissionSensors:
                        #.operator_abbreviation
                        logMessage(mySensor, 2)
                    logMessage('Detected sensor type: %s' % mySensorType, 2)
                    logMessage('Detected acquisition mode: %s' %
                            acquisition_mode, 2)

                    #
                    # Debugging output ends
                    #
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue
                # e.g. 20/01/2011
                date_parts = myPackage.get('DATE_ACQ').split('/')
                # e.g. 08:29:01
                time_parts = myPackage.get('TIME_ACQ').split(':')
                # Fills the the product_id
                #SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN
                myProductId =(('%(SAT)s_%(SEN)s_%(TYP)s_%(MOD)s_%(KKKK)s_%(KS)'
                              's_%(JJJJ)s_%(JS)s_%(YYMMDD)s_%(HHMMSS)s_%(LEVL)'
                              's_%(PROJTN)s') %
                {
                  'SAT': mySpotMission.abbreviation.ljust(3, '-'),
                  'SEN': mySensorType.mission_sensor.abbreviation.ljust(3, '-'),
                  'TYP': mySensorType.abbreviation.ljust(3, '-'),
                  'MOD': acquisition_mode.abbreviation.ljust(4, '-'),
                  'KKKK': myPackage.get('a21')[1:4].rjust(4, '0'),
                  'KS': '00',
                  'JJJJ': myPackage.get('a21')[4:7].rjust(4, '0'),
                  'JS': '00',
                  'YYMMDD': date_parts[2][-2:]+date_parts[1]+date_parts[0],
                  'HHMMSS': time_parts[0]+time_parts[1]+time_parts[2],
                  'LEVL' : theProcessingLevel.ljust(4, '-'),
                  'PROJTN': myProjection.ljust(6, '-')
                })
                assert len(myProductId) == 58, ('Wrong len in product_id : %s'
                                                % myProductId)

                logMessage('Product ID %s' % myProductId, 2)

                # Do the ingestion here...
                myData = {
                  'metadata': '\n'.join(['%s=%s' %
                            (f,myPackage.get(f)) for f in myPackage.fields]),
                  'spatial_coverage': myPackage.geom.geos,
                  'product_id': myProductId,
                  'radiometric_resolution': myRadiometricResolution,
                  'band_count': myBandCount,
                  # integer percent
                  'cloud_cover': int(myPackage.get('CLOUD_PER')),
                  'owner_id': myOwner.id,
                  'license': theLicense,
                  'creating_software': theSoftware,
                  'quality': theQuality,
                  'sensor_inclination_angle': myPackage.get('ANG_INC'),
                  'sensor_viewing_angle': myPackage.get('ANG_ACQ'),
                  'original_product_id': myOriginalProductId,
                  'solar_zenith_angle': mySolarZenithAngle,
                  'solar_azimuth_angle': mySolarAzimuthAngle,
                  'spatial_resolution_x': myPackage.get('RESOL'),
                  'spatial_resolution_y': myPackage.get('RESOL'),
                }
                logMessage(myData, 2)

                # Check if it's already in catalogue:
                try:
                    #original_product_id is not necessarily unique
                    #so we use product_id
                    myProduct = OpticalProduct.objects.get(
                        product_id=myProductId
                    ).getConcreteInstance()
                    logMessage(('Already in catalogue: updating %s.'
                                % myProductId), 2)
                    myNewRecordFlag = False
                    myUpdatedRecordCount += 1
                    myProduct.__dict__.update(myData)
                except ObjectDoesNotExist:
                    myProduct = OpticalProduct(**myData)
                    logMessage('Not in catalogue: creating.', 2)
                    myNewRecordFlag = True
                    myCreatedRecordCount += 1
                    try:
                        myProduct.productIdReverse(True)
                    except Exception, e:
                        raise CommandError('Cannot get all mandatory data '
                        'from product id %s (%s).' % (myProductId, e))
                logMessage('Saving product and setting thumb', 2)
                try:
                    myProduct.save()
                    if theTestOnlyFlag:
                        logMessage('Testing: image not saved.', 2)
                        pass
                    else:
                        if myDownloadThumbsFlag:
                            # Store thumbnail
                            myThumbsFolder = os.path.join(
                                settings.THUMBS_ROOT,
                                myProduct.thumbnailDirectory())
                            try:
                                os.makedirs(myThumbsFolder)
                            except:
                                pass
                            # Download original jpeg thumbnail and
                            # creates a thumbnail
                            myDownloadedThumb = os.path.join(myThumbsFolder,
                                                myProduct.product_id + '.jpg')
                            myHandle = open(myDownloadedThumb, 'wb+')
                            myThumbnail = urllib2.urlopen(
                                myPackage.get('URL_QL'))
                            myHandle.write(myThumbnail.read())
                            myThumbnail.close()
                            myHandle.close()
                            # Transform and store .wld file
                            logMessage('Referencing thumb',2)
                            try:
                                myProduct.georeferenceThumbnail()
                            except:
                                traceback.print_exc(file=sys.stdout)
                        else:
                            # user opted not to ingest thumbs immediately
                            # only set the thumb url if it is a new product
                            # as existing products may already have cached a
                            # copy
                            if myNewRecordFlag:
                                myProduct.remote_thumbnail_url = (
                                      myPackage.get('URL_QL'))
                                myProduct.save()
                    if myNewRecordFlag:
                        logMessage('Product %s imported.' %
                                   myRecordCount, 2)
                        pass
                    else:
                        logMessage('Product %s updated.' %
                                   myUpdatedRecordCount, 2)
                        pass
                except Exception, e:
                    traceback.print_exc(file=sys.stdout)
                    raise CommandError('Cannot import: %s' % e)

            logMessage('%s packages imported' % myRecordCount)

            if theTestOnlyFlag:
                transaction.rollback()
                logMessage('Testing only: transaction rollback.')
            else:
                transaction.commit()
                logMessage('Committing transaction.', 2)
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('Uncaught exception (%s): %s' %
                               (e.__class__.__name__, e))
    except Exception, e:
        logMessage('Rolling back transaction due to exception.')
        traceback.print_exc(file=sys.stdout)
        if theTestOnlyFlag:
            from django.db import connection
            logMessage(connection.queries)
        transaction.rollback()
        raise CommandError('%s' % e)
    finally:
        lockfile.release()
    mySummary = ('Ingestion Summary:\n'
                 '-------------------------------------\n'
                 '%s records reviewed\n'
                 '%s records imported\n'
                 '%s records updated\n'
                 '%s records discarded (H and Colour T)\n'
                 '-------------------------------------\n' %
                 (myRecordCount,
                  myCreatedRecordCount,
                  myUpdatedRecordCount,
                  myDiscardedRecordCount))
    logMessage(mySummary, 0)

def fetchGeometries(theShapefile, theAreaOfInterest):
    """
    Download the index and parses it, returns a generator list of features.

    Args:
        theShapefile - (Required) A shapefile downloaded from
           http://catalog.spotimage.com/pagedownload.aspx
        theAreaOfInterest - (Optional) A geometry defining which features
          to include.

    Returns
        A list of geometries is returned, all intersecting with the area of
        interest if it was specified.:
    """
    try:
        print('Opening %s' % theShapefile)
        data_source = DataSource(theShapefile)
    except Exception, e:
        raise CommandError('Loading index failed %s' % e)

    for myPolygon in data_source[0]:
        if (not theAreaOfInterest or
           theAreaOfInterest.intersects(myPolygon.geom)):
            yield myPolygon
