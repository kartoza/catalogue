"""
  A utility script to migrate data from the legacy acs schema to the unified data model
  *** Warning ***
  Data sources, may be very large. If you find that
  this importer is using too much memory, set DEBUG=False in your settings. When
  Debug=True django automatically logs all sql
  statements contain geometries, it is easy to consume more memory than usual.

  To execute this script do:

  source ../python/bin/activate   <--activate your virtual environment
  python manage.py runscript --pythonpath=scripts -v 2 unified_model_migrator
  deactivate


  Above requires the dango command extension
"""
from datetime import datetime
import os
import shutil

from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

from django_project.catalogue.models import *
from acscatalogue.models import *


#various helper methods
from importutils import *

#Set this to the dir containing thumbs to be imported
#Should just be a flat dir with no heirachy
#mInScenesPath = "/mnt/cataloguestorage/scenes_out_projected/"
mInScenesPath = "/opt/thumbnails/SACC/"
#mOutScenesPath = "/cataloguestorage/scenes_out_projected_sorted/"
mOutScenesPath = "/opt/thumbnails/"
mSortThumbsFlag = True
mProgressInterval = 10000



def migrateSacc():
    """Migrate the data in this model into the GenericProduct/OpticalProduct models
    """
    mySuccessCount = 0
    myErrorCount = 0
    myThumbErrorCount = 0
    myRecords = Sacc.objects.all()
    for myRecord in myRecords:
        #example product:
        #S-C_MRS_hr-_rt--_022E_54_022S_38_20090207_000000_L1Ab_ORBIT.jpg
        # Generic
        mySatellite = "Sacc"
        ########################################################
        # Generic product foreign key attributes
        ########################################################
        myMissionName = "S-C"
        myMissionLongName = "SAC-C"
        myMission = getOrCreateMission( myMissionName, myMissionLongName)
        myMissionSensor = getOrCreateMissionSensor( "MRS", "SACC MRS" )
        myAcquisitionMode = getOrCreateAcquisitionMode( 'HR', 'HR', 0, 0 )
        mySensorType = getOrCreateSensorType("RT","RT")
        myProcessingLevel = getOrCreateProcessingLevel("1Ab","Level 1Ab")
        myInstitution = getOrCreateInstitution("Satellite Applications Centre", "Hartebeeshoek", "Gauteng", "South Africa", "0000")
        myLicense = getOrCreateLicense("SAC License","SAC License")
        # Projection
        myPoint = myRecord.the_geom.centroid
        #print "Centroid of frame: %s" % str( myPoint.coords )
        try:
            myEpsgCode, myProjectionName = utmZoneFromLatLon( myPoint )
        except:
            myErrorCount += 1
            continue
        myProjection = getOrCreateProjection( myEpsgCode,myProjectionName )
        myQuality = getOrCreateQuality("Unknown")
        myCreatingSoftware = getOrCreateCreatingSoftware("Unknown","None")
        ########################################################
        # Now create and populate the product
        ########################################################
        myProduct = OpticalProduct()
        myProduct.mission = myMission
        myProduct.mission_sensor = myMissionSensor
        myProduct.sensor_type = mySensorType
        myProduct.acquisition_mode = myAcquisitionMode
        myProduct.processing_level = myProcessingLevel
        myProduct.owner = myInstitution
        myProduct.license = myLicense
        myProduct.projection = myProjection
        myProduct.quality = myQuality
        myProduct.creating_software = myCreatingSoftware
        #S-C_MRS_hr-_rt--_022E_54_022S_38_20090207_000000_L1Ab_ORBIT.jpg
        myTokens = myRecord.sceneid.split("_")
        print "Date : %s" % myTokens[8]
        myDay   = int(myTokens[8][6:8])
        myMonth = int(myTokens[8][4:6])
        myYear  = int("20%s" % myTokens[8][2:4])
        myHour   = int(myTokens[9][0:2])
        myMinute = int(myTokens[9][2:4])
        mySecond  = int(myTokens[9][4:6])
        myProduct.product_acquisition_start = datetime( myYear, myMonth, myDay, myHour, myMinute, mySecond )
        myProduct.product_acquisition_end = None
        myProduct.spatial_coverage = myRecord.the_geom
        myProduct.geometric_accuracy_mean = None
        myProduct.geometric_accuracy_1sigma = None
        myProduct.geometric_accuracy_2sigma = None
        myProduct.spectral_accuracy = None
        myProduct.radiometric_signal_to_noise_ration = None
        myProduct.radiometric_percentage_error = None
        myProduct.geometric_resolution_x = 3000
        myProduct.geometric_resolution_y = 3000
        myProduct.band_count = 7
        myProduct.radiometric_resolution = 0
        myProduct.original_product_id = myRecord.sceneid
        myProduct.orbit_number = None
        myProduct.product_revision = None
        myProduct.path = myRecord.wrsp
        myProduct.path_offset = 0
        myProduct.row = myRecord.wrsr
        myProduct.row_offset = 0
        myProduct.offline_storage_medium_id =None
        myProduct.online_storage_medium_id = None
        #Descriptors for optical products
        myProduct.cloud_cover = 0
        myProduct.sensor_inclination_angle = None
        myProduct.sensor_viewing_angle = None
        myProduct.gain_name = None
        myProduct.gain_value_per_channel = None
        myProduct.gain_change_per_channel = None
        myProduct.bias_per_channel = None
        myProduct.solar_zenith_angle = None
        myProduct.solar_azimuth_angle = None
        myProduct.earth_sun_distance = None
        myProduct.metadata = ""
        myProduct.setSacProductId()
        print myProduct.product_id
        if len( GenericProduct.objects.filter(product_id=myProduct.product_id) ) == 0:
            print "Creating new product %s" % myProduct.product_id
            try:
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        else: #product already exists so update it by simply assigning the id of the one in the db
            print "Updating existing product %s" % myProduct.product_id
            try:
                myProduct.id = OpticalProduct.objects.get( product_id = myProduct.product_id ).id
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        print "Original product id : %s" % myRecord.sceneid
        if mSortThumbsFlag:
            # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
            # the thumb was saved as: myJpegThumbnail = os.path.join(mInScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
            myJpegThumbnail = os.path.join(mInScenesPath, str( myProduct.original_product_id ) + ".jpg")
            myWorldFile = os.path.join(mInScenesPath, str( myProduct.original_product_id ) + ".jgw")
            print "myJpegThumbnail %s" % myJpegThumbnail
            myOutputPath = os.path.join( mOutScenesPath, myProduct.thumbnailDirectory() )
            if not os.path.isdir( myOutputPath ):
                #print "Creating dir: %s" % myOutputPath
                try:
                    os.makedirs( myOutputPath )
                except OSError:
                    print "Failed to make output directory...quitting"
                    return "False"
            else:
                pass
            try:
                myNewJpgFile =  os.path.join( myOutputPath, myProduct.product_id + ".jpg" )
                myNewWorldFile =  os.path.join( myOutputPath, myProduct.product_id + ".wld" )
                print "New filename: %s" % myNewJpgFile
                shutil.move( myJpegThumbnail, myNewJpgFile )
                shutil.move( myWorldFile, myNewWorldFile )
            except:
                myThumbErrorCount += 1


        # Show progress occasionaly
        if mySuccessCount % mProgressInterval == 0:
            print "Records successfully processed: %s" % mySuccessCount

def migrateCBERS():
    """Migrate the data in this model into the GenericProduct/OpticalProduct models
    """
    print "Processing CBERS"
    mySuccessCount = 0
    myErrorCount = 0
    myThumbErrorCount = 0
    myRecords = Cbers.objects.all()
    for myRecord in myRecords:
        print "Next rec"
        # Generic
        print "Record %s" % mySuccessCount
        mySatellite = "CBERS"
        ########################################################
        # Generic product foreign key attributes
        ########################################################
        myMissionName = "C2B"
        myMissionLongName = "CBERS"
        myMission = getOrCreateMission( myMissionName, myMissionLongName)
        myMissionSensor = getOrCreateMissionSensor( "CCD", "CBERS CCD" )
        mySensorType = getOrCreateSensorType("MSS", "Multispectral")
        # clean up bug in generated sceneids from sarmes
        myRecord.sceneid = myRecord.sceneid.replace(myRecord.sceneid.split("_")[11],"ORBIT" )
        myRecord.sceneid = "_".join(myRecord.sceneid.split("_")[0:12])
        print "Scene ID: %s" % myRecord.sceneid
        myMode = myRecord.sceneid.split("_")[3]
        myAcquisitionMode = getOrCreateAcquisitionMode( myMode, myMode, 0, 0 )
        myProcessingLevel = getOrCreateProcessingLevel("1Ab","Level 1Ab")
        myInstitution = getOrCreateInstitution("Satellite Applications Centre", "Hartebeeshoek", "Gauteng", "South Africa", "0000")
        myLicense = getOrCreateLicense("SAC License","SAC License")
        # Projection
        myPoint = myRecord.the_geom.centroid
        #print "Centroid of frame: %s" % str( myPoint.coords )
        try:
            myEpsgCode, myProjectionName = utmZoneFromLatLon( myPoint )
        except:
            myErrorCount += 1
            continue
        myProjection = getOrCreateProjection( myEpsgCode,myProjectionName )
        myQuality = getOrCreateQuality("Unknown")
        myCreatingSoftware = getOrCreateCreatingSoftware("SARMES1","Sarmes1")
        ########################################################
        # Now create and populate the product
        ########################################################
        myProduct = OpticalProduct()
        myProduct.mission = myMission
        myProduct.mission_sensor = myMissionSensor
        myProduct.sensor_type = mySensorType
        myProduct.acquisition_mode = myAcquisitionMode
        myProduct.processing_level = myProcessingLevel
        myProduct.owner = myInstitution
        myProduct.license = myLicense
        myProduct.projection = myProjection
        myProduct.quality = myQuality
        myProduct.creating_software = myCreatingSoftware
        #adate    | 20081212
        #ayear    | 2008
        #amonth   | 12
        #aday     | 12
        #ahour    | 07
        #amin     | 23
        #asec     | 34
        myProduct.product_acquisition_start = datetime( int(myRecord.ayear),
                                                        int(myRecord.amonth),
                                                        int(myRecord.aday),
                                                        int(myRecord.ahour),
                                                        int(myRecord.amin),
                                                        int(myRecord.asec ) )
        myProduct.product_acquisition_end = None
        myProduct.spatial_coverage = myRecord.the_geom
        myProduct.geometric_accuracy_mean = None
        myProduct.geometric_accuracy_1sigma = None
        myProduct.geometric_accuracy_2sigma = None
        myProduct.spectral_accuracy = None
        myProduct.radiometric_signal_to_noise_ration = None
        myProduct.radiometric_percentage_error = None
        myProduct.geometric_resolution_x = 3000
        myProduct.geometric_resolution_y = 3000
        myProduct.band_count = 7
        myProduct.radiometric_resolution = 0
        myProduct.original_product_id = myRecord.sceneid
        myProduct.orbit_number = None
        myProduct.product_revision = None
        myProduct.path = myRecord.k
        myProduct.path_offset = 0
        myProduct.row = myRecord.j
        myProduct.row_offset = 0
        myProduct.offline_storage_medium_id =None
        myProduct.online_storage_medium_id = None
        #Descriptors for optical products
        myProduct.cloud_cover = 0
        myProduct.sensor_inclination_angle = None
        myProduct.sensor_viewing_angle = None
        myProduct.gain_name = None
        myProduct.gain_value_per_channel = None
        myProduct.gain_change_per_channel = None
        myProduct.bias_per_channel = None
        myProduct.solar_zenith_angle = myRecord.sazia
        myProduct.solar_azimuth_angle = myRecord.seleva
        myProduct.earth_sun_distance = None
        myProduct.metadata = ""
        myProduct.setSacProductId()
        print myProduct.product_id
        if len( GenericProduct.objects.filter(product_id=myProduct.product_id) ) == 0:
            print "Creating new product %s" % myProduct.product_id
            try:
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        else: #product already exists so update it by simply assigning the id of the one in the db
            print "Updating existing product %s" % myProduct.product_id
            try:
                myProduct.id = OpticalProduct.objects.get( product_id = myProduct.product_id ).id
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        print "Original product id : %s" % myRecord.sceneid
        if mSortThumbsFlag:
            # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
            # the thumb was saved as: myJpegThumbnail = os.path.join(mInScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
            myJpegThumbnail = os.path.join(mInScenesPath, str( myProduct.original_product_id ) + ".jpg")
            myWorldFile = os.path.join(mInScenesPath, str( myProduct.original_product_id ) + ".jgw")
            print "myJpegThumbnail %s" % myJpegThumbnail
            myOutputPath = os.path.join( mOutScenesPath, myProduct.thumbnailDirectory() )
            if not os.path.isdir( myOutputPath ):
                #print "Creating dir: %s" % myOutputPath
                try:
                    os.makedirs( myOutputPath )
                except OSError:
                    print "Failed to make output directory...quitting"
                    return "False"
            else:
                pass
            try:
                myNewJpgFile =  os.path.join( myOutputPath, myProduct.product_id + ".jpg" )
                myNewWorldFile =  os.path.join( myOutputPath, myProduct.product_id + ".wld" )
                print "New filename: %s" % myNewJpgFile
                shutil.move( myJpegThumbnail, myNewJpgFile )
                shutil.move( myWorldFile, myNewWorldFile )
            except:
                myThumbErrorCount += 1


        # Show progress occasionaly
        if mySuccessCount % mProgressInterval == 0:
            print "Records successfully processed: %s" % mySuccessCount


def migrateSumbandilasat():
    """Migrate the data in this model into the GenericProduct/OpticalProduct models
       ZA2_MSS_R3B_FMC4_015E_27_024S_44_100214_073646_L1A-_ORBIT-
    """
    print "Processing sumbandilesat"
    mySuccessCount = 0
    myErrorCount = 0
    myThumbErrorCount = 0
    myRecords = Sumb.objects.all()
    for myRecord in myRecords:
        print "Next rec"
        # Generic
        print "Record %s" % mySuccessCount
        mySatellite = "ZA2"
        ########################################################
        # Generic product foreign key attributes
        ########################################################
        myMissionName = "ZA2"
        myMissionLongName = "Sumbandilasat"
        myMission = getOrCreateMission( myMissionName, myMissionLongName)
        myMissionSensor = getOrCreateMissionSensor( "SMS", "Sumbandilasat MSS" )
        mySensorType = getOrCreateSensorType("R3B", "R3B")
        myAcquisitionMode = getOrCreateAcquisitionMode( 'FMC4', 'FMC4', 0, 0 )
        myProcessingLevel = getOrCreateProcessingLevel("1Ab","Level 1Ab")
        myInstitution = getOrCreateInstitution("Satellite Applications Centre", "Hartebeeshoek", "Gauteng", "South Africa", "0000")
        myLicense = getOrCreateLicense("SAC License","SAC License")
        # Projection
        myPoint = myRecord.the_geom.centroid
        #print "Centroid of frame: %s" % str( myPoint.coords )
        try:
            myEpsgCode, myProjectionName = utmZoneFromLatLon( myPoint )
        except:
            myErrorCount += 1
            continue
        myProjection = getOrCreateProjection( myEpsgCode,myProjectionName )
        myQuality = getOrCreateQuality("Unknown")
        myCreatingSoftware = getOrCreateCreatingSoftware("SARMES1","Sarmes1")
        ########################################################
        # Now create and populate the product
        ########################################################
        myProduct = OpticalProduct()
        myProduct.mission = myMission
        myProduct.mission_sensor = myMissionSensor
        myProduct.sensor_type = mySensorType
        myProduct.acquisition_mode = myAcquisitionMode
        myProduct.processing_level = myProcessingLevel
        myProduct.owner = myInstitution
        myProduct.license = myLicense
        myProduct.projection = myProjection
        myProduct.quality = myQuality
        myProduct.creating_software = myCreatingSoftware
        # ZA2_MSS_R3B_FMC4_106E_01_006S_14_100326_014243_L1A-_ORBIT-
        myTokens = myRecord.sceneid.split("_")
        myDay   = int(myTokens[8][4:6])
        myMonth = int(myTokens[8][2:4])
        myYear  = int("20%s" % myTokens[8][0:2])
        myHour   = int(myTokens[9][0:2])
        myMinute = int(myTokens[9][2:4])
        mySecond  = int(myTokens[9][4:6])

        myProduct.product_acquisition_start = datetime( myYear, myMonth, myDay, myHour, myMinute, mySecond )
        myProduct.product_acquisition_end = None
        myProduct.spatial_coverage = myRecord.the_geom
        myProduct.geometric_accuracy_mean = None
        myProduct.geometric_accuracy_1sigma = None
        myProduct.geometric_accuracy_2sigma = None
        myProduct.spectral_accuracy = None
        myProduct.radiometric_signal_to_noise_ration = None
        myProduct.radiometric_percentage_error = None
        myProduct.geometric_resolution_x = 3000
        myProduct.geometric_resolution_y = 3000
        myProduct.band_count = 7
        myProduct.radiometric_resolution = 0
        #/S/INT/RI/SS1/2010_04_09/raw/20100326_I0137_Jakarta_Indonesia/16bit
        #use 7th token e.g. 20100326_I0137_Jakarta_Indonesia
        #for original id so we can map it to raw products
        myProduct.original_product_id = myRecord.source.split("/")[7]
        myProduct.orbit_number = None
        myProduct.product_revision = None
        myProduct.path = 0
        myProduct.path_offset = 0
        myProduct.row = 0
        myProduct.row_offset = 0
        myProduct.offline_storage_medium_id =None
        myProduct.online_storage_medium_id = None
        #Descriptors for optical products
        myProduct.cloud_cover = 0
        myProduct.sensor_inclination_angle = 0
        myProduct.sensor_viewing_angle = 0
        myProduct.gain_name = None
        myProduct.gain_value_per_channel = None
        myProduct.gain_change_per_channel = None
        myProduct.bias_per_channel = None
        myProduct.solar_zenith_angle = None
        myProduct.solar_azimuth_angle = None
        myProduct.earth_sun_distance = None
        myProduct.metadata = ""
        myProduct.product_id = myRecord.sceneid.replace("1A-","1Ab")
        print myProduct.product_id
        if len( GenericProduct.objects.filter(product_id=myProduct.product_id) ) == 0:
            print "Creating new product %s" % myProduct.product_id
            try:
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        else: #product already exists so update it by simply assigning the id of the one in the db
            print "Updating existing product %s" % myProduct.product_id
            try:
                myProduct.id = OpticalProduct.objects.get( product_id = myProduct.product_id ).id
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        if mSortThumbsFlag:
            # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
            # the thumb was saved as: myJpegThumbnail = os.path.join(mInScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
            myJpegThumbnail = os.path.join(mInScenesPath, str( myProduct.product_id ) + ".jpg")
            myWorldFile = os.path.join(mInScenesPath, str( myProduct.product_id ) + ".wld")
            print "myJpegThumbnail %s" % myJpegThumbnail
            myOutputPath = os.path.join( mOutScenesPath, myProduct.thumbnailDirectory() )
            if not os.path.isdir( myOutputPath ):
                #print "Creating dir: %s" % myOutputPath
                try:
                    os.makedirs( myOutputPath )
                except OSError:
                    print "Failed to make output directory...quitting"
                    return "False"
            else:
                pass
            try:
                myNewJpgFile =  os.path.join( myOutputPath, myProduct.product_id + ".jpg" )
                myNewWorldFile =  os.path.join( myOutputPath, myProduct.product_id + ".wld" )
                print "New filename: %s" % myNewJpgFile
                shutil.move( myJpegThumbnail, myNewJpgFile )
                #currently there are no world files for sumb
                #shutil.copy( myWorldFile, myNewWorldFile )
            except:
                myThumbErrorCount += 1


        # Show progress occasionaly
        if mySuccessCount % mProgressInterval == 0:
            print "Records successfully processed: %s" % mySuccessCount

def migrateSpot5():
    """Migrate the data in this model into the GenericProduct/OpticalProduct models
           This is a special case since the data is loaded in shp files using a procedure like this:

           cd spotimport/SPOT_Shape_Africa_2006/
           shp2pgsql -c -s 4326 -I -S Africa_2006.shp import.spot5 | psql sac
           cd ..
           cd SPOT_Shape_Africa_2007/
           shp2pgsql -a -s 4326 -S Africa_2007.shp import.spot5 | psql sac
           cd ..
           cd SPOT_Shape_Africa_2008/
           shp2pgsql -a -s 4326 -S Africa_2008.shp import.spot5 | psql sac
           cd ..
           cd SPOT_Shape_Africa_2009/
           shp2pgsql -a -s 4326 -S Africa_2009.shp import.spot5 | psql sac
           cd ..
           cd SPOT_Shape_Africa_2010/
           shp2pgsql -a -s 4326 -S Africa_2010.shp import.spot5 | psql sac

           Note: In the SAC environment the above should be run on 'elephant' host

           The shpfiles are those acquired from the spot web site.
           http://sirius.spotimage.fr/PageDownload.aspx (you need to register first)
           After import, the spot5 model should be deleted, associated tables dropped,
           and the geometry columns entry for the spot5 table removed

           The spot5 model was generated using python manage.py inspectdb --database=default > /tmp/schema.sql

    """
    mySuccessCount = 0
    myErrorCount = 0
    myThumbErrorCount = 0
    myRecords = Spot5.objects.filter(satel="5")
    myPreviousRecord = None
    for myRecord in myRecords:
        if myPreviousRecord:
            myPreviousRecord.delete()
        myPreviousRecord = myRecord
        # Generic
        mySatellite = "Spot"
        # We will store the spot5 thumb url in the metadata field for now...
        myString = myRecord.url_ql

        ########################################################
        # Generic product foreign key attributes
        ########################################################
        myMissionName = "S5"
        myMissionLongName = "Spot 5"
        myMission = getOrCreateMission( myMissionName, myMissionLongName)
        myMissionSensor = getOrCreateMissionSensor( "Spot 5 HRG", "Spot 5 HRG" )
        mySensorType = getOrCreateSensorType("CAM1","Spot Camera 1") #this needs to be calculated properly
        myModeIndicator = myRecord.a21[-1] #-1 for last char
        if myModeIndicator == 'J':
            myAcquisitionMode = getOrCreateAcquisitionMode( 'J', 'Multispectral', 0, 0 )
        elif myModeIndicator in ['B','A']:
            myAcquisitionMode = getOrCreateAcquisitionMode( myModeIndicator, 'Panchromatic', 0, 0 )
        myProcessingLevel = getOrCreateProcessingLevel("2A","Level 2A")
        myInstitution = getOrCreateInstitution("Satellite Applications Centre", "Hartebeeshoek", "Gauteng", "South Africa", "0000")
        myLicense = getOrCreateLicense("SAC License","SAC License")
        # Projection
        myPoint = Point( myRecord.lon_cen, myRecord.lat_cen, srid=4326 )
        #print "Centroid of frame: %s" % str( myPoint.coords )
        try:
            myEpsgCode, myProjectionName = utmZoneFromLatLon( myPoint )
        except:
            myErrorCount += 1
            continue
        myProjection = getOrCreateProjection( myEpsgCode,myProjectionName )
        myQuality = getOrCreateQuality("Unknown")
        myCreatingSoftware = getOrCreateCreatingSoftware("Unknown","None")
        ########################################################
        # Now create and populate the product
        ########################################################
        myProduct = OpticalProduct()
        myProduct.mission = myMission
        myProduct.mission_sensor = myMissionSensor
        myProduct.sensor_type = mySensorType
        myProduct.acquisition_mode = myAcquisitionMode
        myProduct.processing_level = myProcessingLevel
        myProduct.owner = myInstitution
        myProduct.license = myLicense
        myProduct.projection = myProjection
        myProduct.quality = myQuality
        myProduct.creating_software = myCreatingSoftware
        myDateTokens = myRecord.date_acq.split("/")
        myDay   = int(myDateTokens[0])
        myMonth = int(myDateTokens[1])
        myYear  = int(myDateTokens[2])
        myTimeTokens = myRecord.time_acq.split(":")
        myHour   = int(myTimeTokens[0])
        myMinute = int(myTimeTokens[1])
        mySecond  = int(myTimeTokens[2])

        myProduct.product_acquisition_start = datetime.datetime( myYear, myMonth, myDay, myHour, myMinute, mySecond )
        myProduct.product_acquisition_end = None
        myProduct.spatial_coverage = myRecord.the_geom
        myProduct.geometric_accuracy_mean = None
        myProduct.geometric_accuracy_1sigma = None
        myProduct.geometric_accuracy_2sigma = None
        myProduct.spectral_accuracy = None
        myProduct.radiometric_signal_to_noise_ration = None
        myProduct.radiometric_percentage_error = None
        myProduct.geometric_resolution_x = 3000
        myProduct.geometric_resolution_y = 3000
        myProduct.band_count = 7
        myProduct.radiometric_resolution = 0
        myProduct.original_product_id = myRecord.a21
        myProduct.orbit_number = None
        myProduct.product_revision = None
        myProduct.path = int(myRecord.a21[1:4]) #K
        myProduct.path_offset = 0
        myProduct.row = int(myRecord.a21[4:7]) #J
        myProduct.row_offset = 0
        myProduct.offline_storage_medium_id =None
        myProduct.online_storage_medium_id = None
        #Descriptors for optical products
        myProduct.cloud_cover = myRecord.cloud_per
        myProduct.sensor_inclination_angle = myRecord.ang_inc
        myProduct.sensor_viewing_angle = myRecord.ang_acq
        myProduct.gain_name = None
        myProduct.gain_value_per_channel = None
        myProduct.gain_change_per_channel = None
        myProduct.bias_per_channel = None
        myProduct.solar_zenith_angle = None
        myProduct.solar_azimuth_angle = None
        myProduct.earth_sun_distance = None
        myProduct.remote_thumbnail_url = myString
        try:
            myProduct.setSacProductId()
        except:
            myErrorCount += 1
            continue
        #print myProduct.product_id
        if len( GenericProduct.objects.filter(product_id=myProduct.product_id) ) != 0:
                # product already has been imported
            continue
        if len( GenericProduct.objects.filter(original_product_id=myProduct.original_product_id) ) == 0:
            # Set thumb to spotimage server for now - will be blanked when a local copy is made
            myProduct.remote_thumbnail_url = myString
            try:
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue
        else: #product already exists so update it by simply assigning the id of the one in the db
            # Note we dont set the thumb here because it may have already been cached
            try:
                myProduct.id = OpticalProduct.objects.get( original_product_id = myProduct.original_product_id ).id
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                continue

        # Show progress occasionaly
        if mySuccessCount % mProgressInterval == 0:
            print "Records successfully processed: %s" % mySuccessCount

####################################################################
# Starting point
####################################################################

def run( ):
    #refreshSacIds()
    migrateSpot5()
    #migrateSumbandilasat()
    #migrateCBERS()
    #migrateSacc()
    return

if __name__ == "__main__":
    run()
