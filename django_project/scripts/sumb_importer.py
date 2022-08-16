#
# Sort SUMBANDILASAT imagery into a standard folder heirachy
# See DATAIMPORT doc for details
#
#
# to run do:
# source ../python/bin/activate
# python manage.py runscript --pythonpath=scripts -v 2 sumb_importer
# from the dir above scripts dir
import shutil
import sys
import traceback

from django_project.catalogue.models import *
from importutils import *
from settings import *


mProgressInterval = 10
mSourcePath = "/mnt/cataloguestorage/imagery_processing/sumbandilasat/"

def importMetadata( theProjectDir ):
    """Migrate the data in the temporary Sumb model into the GenericProduct/OpticalProduct models
       ZA2_MSS_R3B_FMC4_015E_27_024S_44_100214_073646_L1A-_ORBIT-
    """
    mySuccessCount = 0
    myErrorCount = 0
    myThumbErrorCount = 0
    myRecords = Sumb.objects.all()
    print "%s records in Sumb table before processing starts for this project folder" % len( myRecords )
    myPreviousRecord = None
    for myRecord in myRecords:
        #clear successfully processed recs from the import.sumb db table as they are dealt with
        if myPreviousRecord:
            myPreviousRecord.delete()
        # Work out the path for the thumb
        myInputThumbnailsPath = os.path.join( mSourcePath, theProjectDir, "imp", "ThNl" )
        myJpegThumbnail = os.path.join(myInputThumbnailsPath, str( myRecord.sceneid.replace("1A-","1Ab")) + ".jpg")
        # if this thumb does not exist, stop this iteration right here
        # since the sumb rec we have is probably from another project
        # folder that is still to be processed. We test for the pox file
        # in case we are re-running the processing and the jpg has already been filed away
        if not os.path.exists(myJpegThumbnail+".pox"):
            print "%s missing, skipping rec" % myJpegThumbnail
            myPreviousRecord = None
            continue
        # Ok we have a matching thum so go on to process the record
        # and get it into the generic products table
        myPreviousRecord = myRecord
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
            myPreviousRecord = None
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
                myPreviousRecord = None
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
                myPreviousRecord = None
                continue
        # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
        myWorldFile = os.path.join(myInputThumbnailsPath, str( myProduct.product_id ) + ".wld")
        print "myJpegThumbnail %s" % myJpegThumbnail
        myOutputPath = os.path.join( settings.THUMBS_ROOT, myProduct.thumbnailDirectory() )
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
            shutil.copy( myJpegThumbnail, myNewJpgFile )
            #currently there are no world files for sumb
            #shutil.copy( myWorldFile, myNewWorldFile )
        except:
            pass

        try:
            # Now run the code to bring in the 1ab product
            if not importL1Ab( theProjectDir, myProduct ):
                myErrorCount += 1
                continue
            if not importL1Aa( theProjectDir, myProduct ):
                myErrorCount += 1

        except:
            traceback.print_exc(file=sys.stdout)
            myThumbErrorCount += 1

        # Show progress occasionaly
        if mySuccessCount % mProgressInterval == 0:
            print "Records successfully processed: %s" % mySuccessCount
    print "%s records in Sumb table after processing finished for this project folder" % len( myRecords )

def importL1Ab( theProjectDir, theProduct ):
    print "L1Ab import for %s" % theProduct.product_id
    myOutputPath = os.path.join( settings.IMAGERY_ROOT, theProduct.productDirectory() )
    myOutputFile = os.path.join( myOutputPath, theProduct.product_id + ".tif.bz2" )
    myPixSourceFile = os.path.join( mSourcePath, theProjectDir, "imp", theProduct.product_id + ".pix" )
    myTiffSourceFile = os.path.join( mSourcePath, theProjectDir, "imp", theProduct.product_id + ".tif" )
    myBzipSourceFile = myTiffSourceFile + ".bz2"
    if os.path.isfile( myTiffSourceFile ):
        print "Removing old tif"
        os.remove( myTiffSourceFile )
    if os.path.isfile( myBzipSourceFile ):
        print "Removing old tif.bz2"
        os.remove( myBzipSourceFile )
    if os.path.isfile( myPixSourceFile ):
        myString = "gdal_translate -of GTIFF %s %s" % ( myPixSourceFile, myTiffSourceFile )
        print myString
        print "Converting to tiff now"
        os.system( myString )
        print "Bzipping now using \n bzip2 %s" % myTiffSourceFile
        os.system( "bzip2 %s" % myTiffSourceFile )
        print "File bzipped now"
    if not os.path.isdir( myOutputPath ):
        print "Creating dir: %s" % myOutputPath
        try:
            os.makedirs( myOutputPath )
        except OSError:
            print "Failed to make output directory...quitting"
            return False
    else:
        print "Exists: %s" % myOutputPath
        pass
    print "Move: %s to %s" % (myBzipSourceFile, myOutputFile)
    try:
        shutil.move( myBzipSourceFile  , myOutputFile )
        myRelativePath = os.path.join( theProduct.productDirectory(), theProduct.product_id + ".tif.bz2" )
        print "Local storage path: %s" % myRelativePath
        theProduct.local_storage_path = myRelativePath
        theProduct.save()
    except:
        traceback.print_exc(file=sys.stdout)
        return False
    return True



def importL1Aa( theProjectDir, theProduct ):
    """Sort raw imagery into a standard folder heirachy"""
    myCwd = os.getcwd()
    myRawSourceDirParent = os.path.join( mSourcePath, theProjectDir, "raw" )
    os.chdir(myRawSourceDirParent)
    print "L1Aa import for %s" % theProduct.product_id
    myOutputPath = os.path.join( settings.IMAGERY_ROOT, theProduct.productDirectory().replace("1Ab","1Aa") )
    myOutputFile = os.path.join( myOutputPath, theProduct.product_id.replace("L1Ab","L1Aa") + ".tar.bz2" )
    mySourceDir = theProduct.original_product_id
    if not os.path.isdir( myOutputPath ):
        print "Creating dir: %s" % myOutputPath
        try:
            os.makedirs( myOutputPath )
        except OSError:
            print "Failed to make output directory...quitting"
            return False
    else:
        #print "Exists: %s" % myOutputPath
        pass
    # We make copies so we can rerun this script with a different naming scheme if needed
    if os.path.isfile( myOutputFile ): #dont try to recompress if it already exists
        print "File exists, skipping: %s" % myOutputFile
        return False
    if os.path.isdir( mySourceDir ): #dont try to recompress if it already exists
        try:
            # zip up the raw dir
            myCommand = "tar cfj %s %s" % ( myOutputFile, mySourceDir )
            print myCommand
            os.chdir(myRawSourceDirParent)
            print "Running from  %s " % os.getcwd()
            os.system( myCommand )
        except:
            traceback.print_exc( file=sys.stdout )
            return False
    else:
        print "Source dir %s does not exist" % mySourceDir
        print "Running from %s " % os.getcwd()
        myErrorCount += 1

    os.chdir( myCwd )
    return True


def run():
    myProjectsList = [
        "20101122_20101201",
        "20101206_20101213",
        "20110125_20110214",
        "20110215_20110228",
        "20100901_20100922",
        "20100801_20100830"
                     ]
    print "Processing sumbandilasat"
    for myProject in myProjectsList:
        print "Processing %s" % myProject
        importMetadata(myProject);
    print "All done"

if __name__ == "__main__":
    run()
