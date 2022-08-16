#!/usr/bin/python
#
#  To execute this script do:
#  source ../python/bin/activate   <--activate your virtual environment
#  python manage.py runscript --pythonpath=scripts -v 2 acs_importer
#  deactivate
#

#
# Currently the following filetypes exist:
#
# select t.file_type_name, count(*) from t_aux_files f inner join
# t_file_types t on f.file_type=t.id group by t.file_type_name;
#
# file_type_name  SHOWJPEG
# (count(*))      151406
#
# file_type_name  JPEG
# (count(*))      4343
#
# file_type_name  SHOWJPEG_B4
#(count(*))      31233
#
#

import sys
from acscatalogue.informix import *
import informixdb  # import the InformixDB module
import struct # for reading binary data into a struct
import os # for creating folders
import datetime
import traceback
import struct # for reading binary data into a struct
import glob
import time
import Image
from importutils import *
########################################################
# globals
########################################################

mReportFile = file( "blob_extract_report.txt","wt" )
# This is the directory where the blobs are extracted under.
# Blobs are raw informix db blobs which each contain a segment (swath)
# A yyyy/mm/dd directory will be created under this for each run of this script
mBlobDirBase = "/mnt/cataloguestorage/thumbnail_processing/thumb_blobs/"
# The raw blobs are then converted into jpeg images (ungeoreferenced)
# A yyyy/mm/dd directory will be created under this for each run of this script
mSegmentJpegDirBase = "/mnt/cataloguestorage/thumbnail_processing/segments_out/"
# This is where the segments are placed when they have been rectified
# A yyyy/mm/dd directory will be created under this for each run of this script
mRectifiedSegmentsPathBase = "/mnt/cataloguestorage/thumbnail_processing/georeferenced_segments_out/"
# The scene thumbs are clipped out from the above georeferenced segments and placed into this dir
# A yyyy/mm/dd directory will be created under this for each run of this script
mScenesPathBase = "/mnt/cataloguestorage/thumbnail_processing/georeferenced_thumbs_out/"
# This is the final place where georeferenced thumbs are lodged to be
# available to users of the catalogue
mProductionThumbsDirPath = "/mnt/cataloguestorage/thumbnails_master_copy/"
# Start blob number when the script starts fetching blobs
# we will use this to ensure we don't try to import old data
# that is already imported
mStartBlob = 0
# End blob number at the end of initial blob extraction
mEndBlob = 0

########################################################
# Helper functions for blob extraction to jpgs
########################################################

def getBlockPositionsForBlob( theBlob ):
    """In each blob is a series of embedded jpg images. This
       function computes the offset of the start of each
       jpg image by looking for the initial JFIF tag. It
       returns a list of these block offsets"""
    myLength = len( theBlob )
    #print "File Length: %s" % myLength
    myPosition = 0
    myLastPosition = 0
    theFileNo = 0
    myList = []
    while not myPosition < 0:
        theFileNo = theFileNo + 1
        myLastPosition = myPosition
        #print "Searching from : %s" % ( myPosition + 10 )
        myPosition = theBlob.find( "JFIF", myPosition + 10 ) - 6
        #print "JFIF at %s" % (myPosition )
        if myLastPosition > 0 and myPosition > 0:
            myList.append( myPosition )
        elif len( myList ) == 0:
            myList.append( myPosition )
        else:
            myList.append( myLength )
        #print "myPosition: %s " % myPosition
        #print "myLastPosition: %s " % myLastPosition

    return myList

def blockToData( theStart, theEnd, theBlob ):
    """Extracts a block of binary date from a blob"""
    theBlob.seek( theStart )
    myBlockValue = theBlob.read( theEnd - theStart )
    return myBlockValue

def dataToImage( theData, theFile ):
    """Saves a block of binary data as file"""
    #print "Saving %s" % theFile
    myJpg = open( theFile, mode='wb' )
    myJpg.write( theData )
    myJpg.close()

def createGroupFile( theFileList, theOutputFile ):
    """This function will merge 1 or more images into a single file.
       The images will be pasted into incremental positions down the file."""
    if len( theFileList ) < 1:
        return
    # Open the first image to get its dims
    myImage = Image.open( theFileList[0] )
    # Get the image metrics nicely so we can paste it into the quad image
    mySize = myImage.size
    myX = mySize[0]
    myY = mySize[1]
    #print str(myX) + "," + str(myY)
    mySize = ( myX, myY*len( theFileList, ) )
    myOutImage = Image.new( "RGB", mySize )

    myFileNumber = 0
    for myFile in theFileList:
        myImage = Image.open( theFileList[ myFileNumber ] )
        myFileNumber += 1
        #determine the position to paste the block into
        myBox = ( 0, myY * ( myFileNumber-1 ) )
        # now paste the blocks in
        try:
            myOutImage.paste( myImage, myBox )
        except IOError as e:
            traceback.print_exc(file=sys.stdout)
            raise e
    # save up
    print "Saving %s" % theOutputFile
    myOutImage.save( theOutputFile )

def removeBlocks( theArray ):
    """This function removes temporary files containing blocks
       (individual jpg sub images)."""
    for myBlockFile in theArray:
        try:
            os.remove( myBlockFile )
        except:
            pass
def cleanupJpgs( ):
    """This function removes temporary jpg images"""
    for myFile in glob.glob(os.path.join("/tmp/", '*.jpg')):
        os.remove( myFile )
        pass

def getSortedFileList( theDir ):
    """Retrieve a list of files sorted by date (newest first)
       Taken from : http://www.daniweb.com/code/snippet216688.html#
       Returns an array of tuples where array[x][0] is time and array[x][1] is the file name
    """

    # use a folder you have ...
    myFileList = []
    for myFile in glob.glob( os.path.join ( theDir, '*.blob' ) ):
        myStats = os.stat( myFile )
        # create tuple (year yyyy, month(1-12), day(1-31), hour(0-23), minute(0-59), second(0-59),
        # weekday(0-6, 0 is monday), Julian day(1-366), daylight flag(-1,0 or 1)) from seconds since epoch
        # note:  this tuple can be sorted properly by date and time
        myLastModifiedDate = time.localtime( myStats[8] )
        #print image_file, lastmod_date   # test
        # create list of tuples ready for sorting by date
        myTuple = myLastModifiedDate, myFile
        myFileList.append( myTuple )
    myFileList.sort()
    return myFileList

def getFilenameIndex( theArray, theFilename ):
    """Returns the position in the array where the given filename occurs.
       Useful if you want to partially process the glob of blob files
       e.g. in cases where processing was stopped and then restarted"""
    for myIndex, myValue in enumerate( theArray ):
        if myValue[1] == theFilename:
            return myIndex






def extractBlobToJpegs( theFile, theSegmentJpegDir ):
    cleanupJpgs()
    # Get the base name of the file
    myFileBase = os.path.split(theFile)[1]
    myFileBase = os.path.splitext(myFileBase)[0]
    #print "+------------------------------------+"
    #print myFile
    myBlob = open(theFile, mode='rb')
    myValue = myBlob.read()
    myArray = getBlockPositionsForBlob( myValue )
    #print myArray
    # used to hold filenames that will be combined into a single file
    myGroupFileArray = []
    myBlockTally = 0
    myErrorTally = 0
    #print "%s block(s) in this file" % ( len( myArray ) - 1 )
    for myPosition in range ( 0,len( myArray ) ):
        myBlockTally += 1
        if myPosition == 0:
            continue # skip the first position marker
        myStart = myArray[ myPosition -1 ]
        myEnd = myArray[ myPosition ]
        myData = blockToData( myStart, myEnd, myBlob )
        myJpgFile = "/tmp/block%s.jpg" % ( myBlockTally )
        dataToImage( myData, myJpgFile )
        myGroupFileArray.append( myJpgFile )
    # We are accummulating files in blocks of myBlocksInGroup
    # or any remaining at the end of the segment
    #write this group of myBlocksInGroup files into a single file
    #print "Block Tally: %s" % myBlockTally
    myJpgFile = "%s/%ssegment.jpg" % ( theSegmentJpegDir, myFileBase )
    #print 'Writing %s' % myJpgFile
    try:
        createGroupFile( myGroupFileArray, myJpgFile )
        removeBlocks( myGroupFileArray )
    except IOError as e:
        if e.errno == 28: #out of space exception
            print "Fatal Error - out of disk space!"
            print "Last file processed was: %s" % myFile
            print e
            traceback.print_exc(file=sys.stdout)
            sys.exit(0);
    except Exception as e:
        myErrorTally = myErrorTally + 1
        removeBlocks( myGroupFileArray )
        print e
        traceback.print_exc(file=sys.stdout)

    mReportFile.write( "+------------------------------------+\n" )
    mReportFile.write( "%s ImageGroups failed to export\n" % myErrorTally )
    mReportFile.write( "+------------------------------------+\n" )




def loadFrames( theRectifiedScenesPath, theAuxFile ):
    """Migrate data from the legacy acscatalogue clone into the new catalogue db"""
    mySuccessCount = 0
    myErrorCount = 0
    myThumbErrorCount = 0
    myMission = None
    mySegment = theAuxFile.segmentCommon
    mySensor = mySegment.sensor
    mySatellite = mySegment.satellite
    myFrames = FrameCommon.objects.filter(segment=mySegment)
    for myFrame in myFrames:
        # Generic
        myString = ""
        myString += "Satellite: %s\n" % mySatellite
        myString += "Sensor: %s\n" % mySensor
        myString += "Segment mission: %s\n" % mySegment.mission
        myString += "Frame Common Acquisition track: %s\n" % myFrame.trackOrbit
        myString += "Frame Common Acquisition frame: %s\n" % myFrame.frame
        myString += "Frame Common Cloud cover: %s\n" % myFrame.cloud
        myString += "Frame Common Cloud mean: %s\n" % myFrame.cloudMean
        myString += "Frame Common Sequence in segment: %s\n" % myFrame.ordinal
        myString += "SegmentCommon Begin Record Date: %s\n" % mySegment.begRecordDate
        myString += "SegmentCommon End Record Date: %s\n" % mySegment.endRecordDate
        myString += "SegmentCommon Original Id: %s\n" % mySegment.original_id
        myString += "Localization timestamp: %s\n" % myFrame.localization.timeStamp
        myString += getSatelliteSpecificMetadata( mySatellite.name , mySegment, myFrame )
        myString += "---------EOR---------"
        #print myString

        ########################################################
        # Generic product foreign key attributes
        ########################################################
        myMission = mySegment.mission
        myMissionName = mySatellite.name[0:1] + str( myMission ) #e.g. L5 for Landsat 5
        myMissionLongName = mySatellite.name + " " + str( myMission ) #e.g. Landsat 5
        myMission = getOrCreateMission( myMissionName, myMissionLongName)
        myMissionSensor = getOrCreateMissionSensor( mySensor.name[0:3], mySensor.common_name )
        mySensorType, myAcquisitionMode = getSensorAndMode( mySatellite.name, mySegment, myFrame )
        #myProcessingLevel = getOrCreateProcessingLevel("1Aa","Level 1Aa (import)")
        myProcessingLevel = getOrCreateProcessingLevel("2A","Level 2A")
        myInstitution = getOrCreateInstitution("Satellite Applications Centre", "Hartebeeshoek", "Gauteng", "South Africa", "0000")
        myLicense = getOrCreateLicense("SAC License","SAC License")
        # Projection
        myPoint = myFrame.localization.geometry.centroid
        #print "Centroid of frame: %s" % str( myPoint.coords )
        try:
            myEpsgCode, myProjectionName = utmZoneFromLatLon( myPoint )
        except:
            myErrorCount += 1
            del myMission
            del mySegment
            del myFrame

            continue
        myProjection = getOrCreateProjection( myEpsgCode,myProjectionName )
        myQuality = getOrCreateQuality("Unknown")
        myCreatingSoftware = getOrCreateCreatingSoftware("Unknown","None")
        ########################################################
        # Now create and populate the product
        ########################################################

        #print "Segment insertion date: %s" % mySegment.insertionDate
        #print "Segment begin record date: %s" % mySegment.begRecordDate
        #print "Segment end record date: %s" % mySegment.endRecordDate
        myProduct = None
        if getProductTypeForSatellite( mySatellite.name ) == "Optical":
            myProduct = OpticalProduct()
        else:
            myProduct = RadarProduct()
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
        myProduct.product_acquisition_start = myFrame.localization.timeStamp
        myProduct.product_acquisition_end = None
        myProduct.spatial_coverage = myFrame.localization.geometry
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
        myProduct.original_product_id = myFrame.localization.original_id
        myProduct.orbit_number = None
        myProduct.product_revision = None
        myProduct.path = myFrame.trackOrbit
        myProduct.path_offset = 0
        myProduct.row = myFrame.frame
        myProduct.row_offset = 0
        myProduct.offline_storage_medium_id =None
        myProduct.online_storage_medium_id = None
        #Descriptors for optical products
        myProduct.cloud_cover = int( myFrame.cloudMean )
        myProduct.sensor_inclination_angle = None
        myProduct.sensor_viewing_angle = None
        myProduct.gain_name = None
        myProduct.gain_value_per_channel = None
        myProduct.gain_change_per_channel = None
        myProduct.bias_per_channel = None
        myProduct.solar_zenith_angle = None
        myProduct.solar_azimuth_angle = None
        applySensorSpecificProperties( mySatellite.name, myProduct, mySegment, myFrame )
        myProduct.earth_sun_distance = None
        myProduct.metadata = myString
        myProduct.setSacProductId()
        #print myProduct.product_id
        if len( GenericProduct.objects.filter(product_id=myProduct.product_id) ) == 0:
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

            try:
                if getProductTypeForSatellite( mySatellite.name ) == "Optical":
                    myProduct.id = OpticalProduct.objects.get( product_id = myProduct.product_id ).id
                else: #assume radar as atmospheric products not implemented yet or needing migration
                    myProduct.id = RadarProduct.objects.get( product_id = myProduct.product_id ).id
                myProduct.save()
                mySuccessCount += 1
            except ValidationError, e:
                print "*****\nError: " +  str( e )  + "\n"
                myErrorCount += 1
                if myErrorCount % mProgressInterval == 0 and myErrorCount > 0:
                    print "Records with errors: %s" % myErrorCount
                del mySegment
                del myFrame
                del myProduct
                continue

        # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
        # the thumb was saved as: myJpegThumbnail = os.path.join(theRectifiedScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
        myJpegThumbnail = os.path.join(theRectifiedScenesPath, str( myFrame.id ) + "-rectified-clipped.jpg")
        myWorldFile = os.path.join(theRectifiedScenesPath, str( myFrame.id ) + "-rectified-clipped.wld")
        #print "myJpegThumbnail %s" % myJpegThumbnail
        myOutputPath = os.path.join( mProductionThumbsDirPath, myProduct.thumbnailDirectory() )
        if not os.path.isdir( myOutputPath ):
            #print "Creating dir: %s" % myOutputPath
            try:
                os.makedirs( myOutputPath )
            except OSError:
                print "Failed to make output directory...quitting"
                return "False"
        else:
            #print "Exists: %s" % myOutputPath
            pass
        # We make copies not rename so we can rerun this script with a different naming scheme if needed
        try:
            myNewJpgFile =  os.path.join( myOutputPath, myProduct.product_id + ".jpg" )
            myNewWorldFile =  os.path.join( myOutputPath, myProduct.product_id + ".wld" )
            print "New filename: %s" % myNewJpgFile
            shutil.copy( myJpegThumbnail, myNewJpgFile )
            shutil.copy( myWorldFile, myNewWorldFile )
        except:
            myThumbErrorCount += 1

        # we shouldnt need this but...
        del myProduct
    # also shouldnt be needed
    del myFrames

    print "+++++++++++++++++++++++++++++++++++++"
    print "Records successfully processed: %s" % mySuccessCount
    print "Records with errors: %s" % myErrorCount
    print "Thumbs with errors: %s" % myThumbErrorCount
    print "+++++++++++++++++++++++++++++++++++++"



def run():
    os.environ['INFORMIXSERVER']="catalog2"
    if not os.environ['INFORMIXSERVER']=="catalog2":
        print "We tried to set the INFORMIXSERVER environment variable for you but failed."
        print "You can try to set it manually before running this script from the bash prompt by doing this:"
        print "export INFORMIXSERVER=catalog2"
        sys.exit(0);

    ########################################################
    # Logic to initially obtain blobs from informix
    ########################################################

    # ------------------------------------
    # open connection to database 'stores'
    # ------------------------------------
    #myConnection = informixdb.connect('catalogue>informix', user='informix', password='')
    myConnection = informixdb.connect('catalogue@catalog2', user='informix', password='')

    # there should be a text file called 'lastblob.txt' in the mBlobDirBase
    # with the number of the last blob imported (the blob no is the t_aux_files id number)
    myLastBlobNo=None
    try:
        myLastBlobFile = file( os.path.join( mBlobDirBase, "lastblob.txt"), "rwt" )
        myLastBlobNo = myLastBlobFile.read()
        myLastBlobFile.close()
    except:
        print "To use this script there should be a file in "
        print mBlobDirBase
        print "Called lastblob.txt"
        print "Containing a single line with the id of the minimum "
        print "aux_file id to start importing from"
        print "On completion, this script will have created a YYYY/MM/DD directory"
        print "beneath " + mBlobDirBase + " containing the extracted blobs."
        print "It will also update the lastblob.txt with the id of the last blob imported"
        print "To manually compute the last imported blob no, you can cd to the most "
        print "recent import directory and do"
        print "ls | sort -n |tail -1 | sed 's/.blob//g'"
        print "Typical useage would be like this:"
        print "INFORMIXSERVER=catalog2; " + sys.argv[0]
        traceback.print_exc(file=sys.stdout)
        myConnection.close()
        sys.exit(0);

    #use global keyword to indicate we will overwrite the global var
    global mStartBlob # must be on its own line
    mStartBlob = myLastBlobNo

    # create the dir to dump the blobs into:
    myBlobDir = os.path.join( mBlobDirBase,
                        str( datetime.datetime.now().year ),
                        str( datetime.datetime.now().month ),
                        str( datetime.datetime.now().day ) )
    # create a dir to dump the blobs when they are converted into unreffed jpegs
    mySegmentJpegDir = os.path.join( mSegmentJpegDirBase,
                        str( datetime.datetime.now().year ),
                        str( datetime.datetime.now().month ),
                        str( datetime.datetime.now().day ) )

    print "Last blob imported has t_aux_file id of %s" % myLastBlobNo

    print "Last blob imported has t_aux_file id of %s" % myLastBlobNo
    print "Dropping blobs into: %s" % myBlobDir

    # ----------------------------------
    # allocate cursor and execute select
    # ----------------------------------
    myCursor = myConnection.cursor(rowformat = informixdb.ROW_AS_DICT)
    # this line is needed for blob retrieval to work!
    informixdb.Connection.Sblob(myConnection)
    mySQL = None
    myMaxBlobNo = int(myLastBlobNo) + 20000
    try:
        #process a max of 20k imaes at a time
        mySQL = "select * from t_aux_files where id > " + str( myLastBlobNo ) + " and id <= " + str( myMaxBlobNo ) + ";"

        print mySQL
        myCursor.execute(mySQL)
    except Exception as myError:
        print "Error with query::"
        print "SQL: " + mySQL
        print "Error: " + str( myError )
        myConnection.close()
        traceback.print_exc(file=sys.stdout)
        sys.exit(0);
    # make a dir for our images
    if not os.path.isdir(mySegmentJpegDir):
        try:
            os.makedirs(mySegmentJpegDir)
        except OSError:
            print "Failed to create segments directory:\n %s\nCheck permissions and retry..." % mySegmentJpegDir
            myConnection.close()
            sys.exit(0);

    # make a dir for our blobs
    if not os.path.isdir(myBlobDir):
        try:
            os.makedirs(myBlobDir)
        except OSError:
            print "Failed to create blobs directory:\n %s\nCheck permissions and retry..." % myBlobDir
            myConnection.close()
            sys.exit(0);

    myCount = 0
    mySkippedCount = 0
    for myRow in myCursor:
        myCount += 1
        # -------------------------------------------
        # delete myRow if column 'code' begins with 'C'
        # -------------------------------------------
        myFileBase = myBlobDir + '/' + str(myRow['id'])
        myFileName = myFileBase + '.blob'
        if os.path.isfile(myFileName):
            mySkippedCount += 1
            #print "Skipped " + myFileName
            continue
        #print "Writing blob %s to %s " % (myRow['id'], myBlobDir)
        myFile = file( myFileName, "wb")
        myBlob = myRow['file']
        try:
            myBlob.open()
            myStats = myBlob.stat()
            #print "Blob stats: size = %s" % str(myStats['size'])
        except Exception, myException:
            print "Sblob open failed (%s)" % str(myException)
        try:
            # First write the whole blob out to a file
            myData = myBlob.read(myBlob.stat()['size'])
            myFile.write(myData)

            #print "Wrote " + myFileName

        except Exception, myException:
            print "Sblob read failed (%s)" % str(myException)
            myConnection.close()
            sys.exit(0);

        #
        # Keep a record of the last blob no imported
        #
        myLastBlobFile = None
        try:
            myLastBlobFile = file( os.path.join( mBlobDirBase, "lastblob.txt"), "wt" )
            myLastBlobNo = myLastBlobFile.write(str(myRow['id']))
            myLastBlobFile.close()

        except:
            print "Failed to write lastblob no to \n%s" % myLastBlobFile
            traceback.print_exc(file=sys.stdout)
            myConnection.close()
            sys.exit(0);

        myBlob.close()
        myFile.close()

        #use global keyword to indicate we will overwrite the global var
        global mEndBlob # must be on its own line
        mEndBlob = myLastBlobNo

        # Try to extract the blob to its segments now
        try:
            extractBlobToJpegs( myFileName, mySegmentJpegDir )
        except:
            print "Failed to write lastblob no to \n%s" % myLastBlobFile
            traceback.print_exc(file=sys.stdout)
            myConnection.close()
            sys.exit(0);

        if myCount % 1000 == 0:
            print "%s Blobs extracted" % myCount
            print "%s Pre-existing Blobs skipped" % mySkippedCount

    print "%s Blobs extracted in total" % myCount
    print "%s Pre-existing Blobs skipped in total" % mySkippedCount
    # ---------------------------------------
    # commit transaction and close connection
    # ---------------------------------------
    myConnection.close()

    ################################################################
    # OK so now all the blobs are extracted and converted to jpg segments....
    # Next we update our informix database clone...
    # the informix class lives in the acs django app and has all the logic
    # needed to fetch updates from the acs informix catalogue
    ################################################################
    myInformix = Informix()
    myInformix.runUpdate()

    print "Informix update completed - georeferencing segments and thumbnails now"

    ################################################################
    # Next we get all the auxfile records within the range [mStartBlob,mEndBlob]
    # and georeference the seqments based on their geometry
    # then we clip out the scenes using gdal (so they are also georeferenced)
    ################################################################
    # create the dir to dump the blobs into:
    myRectifiedSegmentsPath = os.path.join( mRectifiedSegmentsPathBase,
                        str( datetime.datetime.now().year ),
                        str( datetime.datetime.now().month ),
                        str( datetime.datetime.now().day ) )
    # make a dir for our georeferenced segments
    if not os.path.isdir( myRectifiedSegmentsPath ):
        try:
            os.makedirs( myRectifiedSegmentsPath )
        except OSError:
            print "Failed to create georeferenced segments directory:\n %s\nCheck permissions and retry..." % myRectifiedSegmentsPath
            myConnection.close()
            sys.exit(0);

    # create a dir to dump the blobs when they are converted into unreffed jpegs
    myScenesPath = os.path.join( mScenesPathBase,
                        str( datetime.datetime.now().year ),
                        str( datetime.datetime.now().month ),
                        str( datetime.datetime.now().day ) )
    # make a dir for our georeferenced segments
    if not os.path.isdir( myScenesPath ):
        try:
            os.makedirs( myScenesPath )
        except OSError:
            print "Failed to create georeferenced segments directory:\n %s\nCheck permissions and retry..." % myScenesPath
            myConnection.close()
            sys.exit(0);

    myAuxFiles = AuxFile.objects.filter(original_id__gte=mStartBlob) #.filter(original_id__lte=mEndBlob)
    print "%s Aux Files to be processed" % len( myAuxFiles )
    for myAuxFile in myAuxFiles:
        print "Processing %s" % myAuxFile.id
        myResult = rectifyImage( mySegmentJpegDir, myRectifiedSegmentsPath , myAuxFile )
        if myResult  == "True":
            mySegment = myAuxFile.segmentCommon
            myFrames = FrameCommon.objects.filter( segment=mySegment )
            for myFrame in myFrames:
                #clipImage is defined in importutils.py
                clipImage( myScenesPath, myRectifiedSegmentsPath, myAuxFile, myFrame )
            ################################################################
            # Ok now we can migrate the metadata record from the acs database clone
            # to the production catalogue database
            ################################################################
            loadFrames( myScenesPath, myAuxFile)

        else:
            print "Error: Failed to rectify segment for auxfile %s" % myAuxFile.id
            print "Returned code was: %s" % myResult



    sys.exit(0);

if __name__ == "__main__":
    run()
