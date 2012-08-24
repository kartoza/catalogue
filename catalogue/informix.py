'''
SANSA-EO Catalogue - Helper class for connecting to legacy informix DB

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

'''

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import os
import sys
import informixdb  # import the InformixDB module
import traceback
import glob
import Image

from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.geos import Polygon
#from django.contrib.gis.geos import Point
import osgeo.gdal
#from osgeo.gdalconst import *
#see notes below before adding any new imports!


class ClipError(Exception):
    pass


class Informix:
    '''
    This class is a helper class to allow you to easily connect to the legacy
    informix database and execute queries there. It is ported from version 1 of
    the catalogue where this logic was contained in acscatalogue.informix.py.

    This class has doctests - to run them just do:

      python catlogue/informix.py

    Note this class is purposely kept free of dependecies to
    any django apps / models etc so it can be used standalone.
    '''

    def __init__(self):
        os.environ['INFORMIXSERVER'] = 'catalog2'
        if not os.environ['INFORMIXSERVER'] == 'catalog2':
            print (
                'We tried to set the INFORMIXSERVER environment variable for '
                'you but failed.')
            print (
                'You can try to set it manually before running this script '
                'from the bash prompt by doing this:')
            print 'export INFORMIXSERVER=catalog2'
            sys.exit(0)
        self.mConnection = informixdb.connect(
            'catalogue@catalog2', user='informix', password='')
        self.mCursor = self.mConnection.cursor(
            rowformat=informixdb.ROW_AS_DICT)
        # this line is needed for blob retrieval to work!
        informixdb.Connection.Sblob(self.mConnection)
        self.mHaltOnError = True
        # set informix output format to 4 (WKT)
        myWktSql = 'update GeoParam set value = 4 where id=3;'
        self.mCursor.execute(myWktSql)
        print ('Informix constructor called: GeoParam set to wkt mode')

        # cache last fetched rows for efficiency
        self.mLastFrameRow = None
        self.mLastLocalizationRow = None
        self.mLastSegmentRow = None
        self.mLastAuxFileRow = None
        self.mLastFileTypeRow = None

        self.mScratchDir = (
            '/mnt/cataloguestorage/thumbnail_processing/0_scratch_dir')
        self.mUnreferencedSegmentDir = (
            '/mnt/cataloguestorage/thumbnail_processing/1_segments_'
            'unreferenced')
        self.mReferencedSegmentDir = (
            '/mnt/cataloguestorage/thumbnail_processing/2_segments_referenced')
        self.mReferencedSceneDir = (
            '/mnt/cataloguestorage/thumbnail_processing/3_scenes_referenced')

        return

    def __del__(self):
        # Dont use logging.* in dtor - it truncates the log file deleting all
        # other messages
        # set informix output format to 0 (Geodetic / Informix native)
        myWktSql = 'update GeoParam set value = 0 where id=3;'
        self.mCursor.execute(myWktSql)
        self.mConnection.close()
        print ('Informix destructor called: GeoParam set to geodetic mode')
        return

    def scratchDir(self):
        try:
            if not os.path.exists(self.mScratchDir):
                os.makedirs(self.mScratchDir)
        except:
            raise
        return self.mScratchDir

    def setScratchDir(self, thePath):
        self.mScratchDir = thePath
        try:
            if not os.path.exists(thePath):
                os.makedirs(thePath)
        except:
            raise

    def unreferencedSegmentDir(self):
        try:
            if not os.path.exists(self.mUnreferencedSegmentDir):
                os.makedirs(self.mUnreferencedSegmentDir)
        except:
            raise
        return self.mUnreferencedSegmentDir

    def setUnreferencedSegmentDir(self, thePath):
        self.mUnreferencedSegmentDir = thePath
        try:
            if not os.path.exists(thePath):
                os.makedirs(thePath)
        except:
            raise

    def referencedSegmentDir(self):
        try:
            if not os.path.exists(self.mReferencedSegmentDir):
                os.makedirs(self.mReferencedSegmentDir)
        except:
            raise
        return self.mReferencedSegmentDir

    def setReferencedSegmentDir(self, thePath):
        self.mReferencedSegmentDir = thePath
        try:
            if not os.path.exists(thePath):
                os.makedirs(thePath)
        except:
            raise

    def referencedSceneDir(self):
        try:
            if not os.path.exists(self.mReferencedSceneDir):
                os.makedirs(self.mReferencedSceneDir)
        except:
            raise
        return self.mReferencedSceneDir

    def setReferencedSceneDir(self, thePath):
        self.mReferencedSceneDir = thePath
        try:
            if not os.path.exists(thePath):
                os.makedirs(thePath)
        except:
            raise

    def cleanupScratchDir(self):
        '''This function removes temporary jpg scratch images'''
        for myFile in glob.glob(os.path.join(self.mScratchDir, '*.jpg')):
            try:
                os.remove(myFile)
            except:
                raise ClipError(
                    'could not delete files - check permissions and retry')
        for myFile in glob.glob(os.path.join(self.mScratchDir, '*.blob')):
            try:
                os.remove(myFile)
            except:
                raise ClipError(
                    'could not delete files - check permissions and retry')

    def cleanupUnreferencedSegmentsDir(self):
        '''This function removes temporary unreferenced segment images'''
        for myFile in glob.glob(os.path.join(
                self.mUnreferencedSegmentDir, '*.jpg')):
            try:
                os.remove(myFile)
            except:
                raise ClipError(
                    'could not delete files - check permissions and retry')

    def cleanupReferencedSegmentsDir(self):
        '''This function removes temporary jpg referenced segment images'''
        for myFile in glob.glob(os.path.join(
                self.mReferencedSegmentDir, '*.jpg')):
            try:
                os.remove(myFile)
            except:
                raise ClipError(
                    'could not delete files - check permissions and retry')

    def cleanup(self):
        '''
        Clear the scratch, unreferenced segment and referenced seqment dirs and
        flush any cached rows. Usually you will only want to call this if
        something went wrong and you want to clean up the working state.
        '''
        self.cleanupReferencedSegmentsDir()
        self.cleanupUnreferencedSegmentsDir()
        self.cleanupScratchDir()
        self.mLastFrameRow = None
        self.mLastLocalizationRow = None
        self.mLastSegmentRow = None
        self.mLastAuxFileRow = None
        self.mLastFileTypeRow = None

    def runQuery(self, theQuery):
        '''
        A helper function that allows you to run any sql statement against the
        informix backend. A collection of objects (one for each row) will be
        returned.
        Note you shouldnt use this for pulling out large recordsets from the
        database (rather write a dedicated procedure that uses a cursor in
        that case.
        '''
        self.mCursor.execute(theQuery)
        myRows = []
        for myRow in self.mCursor:
            myRows.append(myRow)
        return myRows

    def localization(self, theLocalizationId):
        '''
        Fetch a  localization record from the database given its id e.g. of
            what will be returned:
           {'object_supertype': 1,
            'time_stamp': datetime.datetime(2010, 4, 1, 9, 35, 46),
            'id': 1219163,
            'refresh_rate': 0,
            'geo_time_info':
            'POLYGON(
                (21.6 -32.76, 22.04 -31.04, 20.05 -30.75,
                    19.57 -32.46, 21.6 -32.76))'}
        '''
        if self.mLastLocalizationRow:
            if str(self.mLastLocalizationRow['id']) == str(theLocalizationId):
                return self.mLastLocalizationRow

        myQuery = 'select * from t_localization where id=%i;' % (
            int(theLocalizationId),)
        myRows = self.runQuery(myQuery)
        # There should only be one record
        if len(myRows) > 1:
            raise Exception(
                'Localization Rows',
                'Too many localization rows returned for localization '
                '(received %s, expected 1)' % len(myRows))
        if len(myRows) < 1:
            raise Exception(
                'Localization Rows',
                'No rows returned for localization (received %s, expected'
                ' 1)' % len(myRows))

        self.mLastLocalizationRow = myRows[0]
        return self.mLastLocalizationRow

    def frameForLocalization(self, theLocalizationId):
        '''
        Return a frame record given a localization record. Record returned will
        look something like this:
               {'ordinal': 20,
              'ur_lon': 22.040000915527344,
              'lr_lat': -32.759998321533203,
              'ul_lat': -30.75,
              'll_lon': 19.569999694824219,
              'segment_id': 163777,
              'frame': 82,
              'ul_lon': 20.049999237060547,
              'll_lat': -32.459999084472656,
              'lr_lon': 21.600000381469727,
              'begin_time_cod': 21995.346796739504,
              'localization_id': 1219163,
              'processable': True,
              'ur_lat': -31.040000915527344,
              'cloud_mean': 0,
              'track_orbit': 174,
              'end_time_cod': 21995.347094024386,
              'cloud': '0000****'}
        '''
        if self.mLastFrameRow:
            if (str(self.mFrameLastRow['localization_id']) ==
                    str(theLocalizationId)):
                return self.FrameLastRow

        myFrameQuery = (
            'select * from t_frame_common where localization_id=%i;' % (
                int(theLocalizationId),))
        myFrameRows = self.runQuery(myFrameQuery)
        # There should only be one record
        if len(myFrameRows) > 1:
            raise Exception(
                'FrameRows',
                'Too many framerows returned for localization (received %s, '
                'expected 1)' % len(myFrameRows))
        if len(myFrameRows) < 1:
            raise Exception(
                'FrameRows',
                'Too few framerows returned for localization (received 0, '
                'expected 1)')
        self.mFrameLastRow = myFrameRows[0]
        return self.mFrameLastRow

    def segmentForFrame(self, theSegmentId):
        '''
        Return a segment record given a segment id. Return should look
        something liks this:
        {'sensor_id': 2,
          'mission': 5,
          'ascending_flag': False,
          'satellite_id': 1,
          'i_lon_max': 28.443050384521484,
          'displayed_orbit': 138589,
          'id': 163777,
          'start_feet': 0,
          'i_lon_min': 18.360977172851562,
          'start_block': 0,
          'time_stamp': datetime.datetime(2010, 4, 1, 9, 35, 44),
          'end_block': 0,
          'first_address': 20,
          'insertion_date': 22005.361816053242,
          'beg_record_date': 21995.341348495371,
          'station_id': 19,
          'geo_shape': 'POLYGON((26.733053 -2.30708, 26.2 -4.8, 25.89 -6.24,
            25.58 -7.69, 25.26 -9.14, 24.94 -10.58, 24.62 -12.03, 24.3 -13.47,
            23.97 -14.91, 23.64 -16.36, 23.31 -17.8, 22.97 -19.24, 22.63
            -20.68, 22.28 -22.13, 21.92 -23.57, 21.56 -25, 21.2 -26.44, 20.82
            -27.88, 20.44 -29.32, 20.05 -30.75, 19.65 -32.18, 19.24 -33.62,
            18.360977 -36.550076, 20.507157 -36.867314, 21.3 -33.92, 21.68
            -32.48, 22.04 -31.04, 22.41 -29.6, 22.76 -28.16, 23.11 -26.72,
            23.45 -25.28, 23.79 -23.84, 24.13 -22.39, 24.46 -20.95, 24.78
            -19.51, 25.1 -18.06, 25.42 -16.62, 25.74 -15.17, 26.06 -13.73,
            26.37 -12.28, 26.68 -10.83, 26.99 -9.39, 27.3 -7.94, 27.6 -6.49,
            27.91 -5.04, 28.443051 -2.5631083, 26.733053 -2.30708))',
          'end_feet': 0,
          'cycle': 138589,
          'displayed_medium': '1927',
          'medium_id': 163777,
          'end_record_date': 21995.347863935185,
          'i_lat_max': -2.3070800304412842,
          'i_lat_min': -36.867313385009766,
          'npass': 1,
          'orbit': 174,
          'displayed_track': '174',
          'second_address': 22}
        '''

        if self.mLastSegmentRow:
            if str(self.mLastSegmentRow['id']) == str(theSegmentId):
                return self.mLastSegmentRow

        mySegmentQuery = 'select * from t_segment_common where id=%i;' % (
            int(theSegmentId),)
        mySegmentRows = self.runQuery(mySegmentQuery)
        # There should only be one record
        if len(mySegmentRows) > 1:
            raise Exception(
                'SegmentRows',
                'Too many segment rows returned for frame (received %s, '
                'expected 1)' % len(mySegmentRows))
        if len(mySegmentRows) < 1:
            raise Exception(
                'SegmentRows',
                'Too few segment rows returned for frame (received 0, '
                'expected 1)')
        self.mLastSegmentRow = mySegmentRows[0]
        return self.mLastSegmentRow

    def auxfileForSegment(self, theSegmentId):
        '''
        Return an auxfile for a segment. An auxfile is the thing that
        actually contains the quicklook blob in it.
        {'visible': False,
        'file_type': 8,
        'file_name': 'TM5_T174_S19_20100322_Jpeg',
        'insertion_date': 22005.361816469907,
        'file_description': 'Quick look',
        'file': <_informixdb.Sblob object at 0x23716c0>,
        'object_supertype': 1,
        'common_id': 163777,
        'id': 191795}

        The blob will contain the actual segment quicklook.
        '''

        if self.mLastAuxFileRow:
            if str(self.mLastAuxFileRow['common_id']) == str(theSegmentId):
                return self.mLastAuxFileRow
        myAuxFileQuery = 'select * from t_aux_files where common_id=%i;' % (
            int(theSegmentId),)
        myAuxFileRows = self.runQuery(myAuxFileQuery)
        # There should only be one record
        if len(myAuxFileRows) > 1:
            raise Exception(
                'AuxFileRows',
                'Too many auxfile rows returned for segment (received %s, '
                'expected 1)' % len(myAuxFileRows))
        if len(myAuxFileRows) < 1:
            raise Exception(
                'AuxFileRows',
                'Too few auxfile rows returned for segment (received 0, '
                'expected 1)')
        self.mLastAuxFileRow = myAuxFileRows[0]
        return self.mLastAuxFileRow

    def fileTypeForAuxFile(self, theFileTypeId):
        '''Return the file type for a given auxfile
        e.g. {'file_type_name': 'SHOWJPEG', 'id': 8}
        '''
        if self.mLastFileTypeRow:
            if str(self.mLastFileTypeRow['id']) == str(theFileTypeId):
                return self.mLastAuxFileRow
        myFileTypeQuery = 'select * from t_file_types where id=%i;' % (
            theFileTypeId,)
        myFileTypeRows = self.runQuery(myFileTypeQuery)
        # There should only be one record
        if len(myFileTypeRows) > 1:
            raise Exception(
                'FileTypeRows',
                'Too many filetype rows returned for auxfile (received %s, '
                'expected 1)' % len(myFileTypeRows))
        if len(myFileTypeRows) < 1:
            raise Exception(
                'FileTypeRows',
                'Too few filetype rows returned for auxfile (received 0, '
                'expected 1)')
        self.mLastFileTypeRow = myFileTypeRows[0]
        return self.mLastFileTypeRow

    def thumbForLocalization(self, theLocalizationId):
        '''
        Given a localization id, return its georeferenced thumbnail as a jpg
        path which is georeferenced, and a path to its world file.
        Note: You need to hand build PIL - see install notes for details!
        >>> import os
        >>> from informix import Informix
        >>> myI = Informix()
        Informix constructor called: GeoParam set to wkt mode
        >>> myI.setScratchDir('/tmp')
        >>> myI.setReferencedSceneDir('/tmp')
        >>> myI.setUnreferencedSegmentDir('/tmp')
        >>> myI.setReferencedSegmentDir('/tmp')
        >>> if os.path.exists(
        ...    os.path.join(myI.unreferencedSegmentDir(), '136397.jpg' ) ):
        ...   os.remove(
        ...    os.path.join( myI.unreferencedSegmentDir(), '136397.jpg' ) )
        ...
        >>> if os.path.exists(
        ...    os.path.join( myI.referencedSegmentDir(), '136397-rect.tif' ) ):
        ...   os.remove(
        ...    os.path.join( myI.referencedSegmentDir(), '136397-rect.tif' ) )
        ...
        >>> myImage, myWorld = myI.thumbForLocalization( 1000000 )
        Writing segment image with dimensions x: 1004, y: 17496
        Rectifying /tmp/136397.jpg
        >>> myImage, myWorld = myI.thumbForLocalization( 1000000 )
        Using cached segment image
        Using cached rectified image /tmp/136397-rect.tif
        '''

        #print sys.path.append
        myLocalizationRow = self.localization(theLocalizationId)
        myFrameRow = self.frameForLocalization(theLocalizationId)
        mySegmentRow = self.segmentForFrame(myFrameRow['segment_id'])
        myAuxFileRow = self.auxfileForSegment(myFrameRow['segment_id'])
        myFileTypeRow = self.fileTypeForAuxFile(myAuxFileRow['file_type'])
        try:
            return self.referencedThumb(
                myLocalizationRow, myFrameRow, mySegmentRow, myAuxFileRow,
                myFileTypeRow)
        except:
            self.cleanup()
            raise

    def referencedThumb(
            self, theLocalizationRow, theFrameRow, theSegmentRow,
            theAuxFileRow, theFileTypeRow):
        '''
        Given complete rows of loc, frame, segment, auxfile and file type,
        return a path to a jpg thumbnail which is georeferenced, and a path to
        its world file.
        Note: You need to hand build PIL - see install notes for details!
        >>> from informix import Informix
        >>> import os
        >>> myI = Informix()
        Informix constructor called: GeoParam set to wkt mode
        >>> myI.setScratchDir('/tmp')
        >>> myI.setReferencedSceneDir('/tmp')
        >>> myI.setUnreferencedSegmentDir('/tmp')
        >>> myI.setReferencedSegmentDir('/tmp')
        >>> if os.path.exists(
        ...    os.path.join( myI.unreferencedSegmentDir(), '136397.jpg' ) ):
        ...   os.remove(
        ...    os.path.join( myI.unreferencedSegmentDir(), '136397.jpg' ) )
        ...
        >>> if os.path.exists(
        ...    os.path.join( myI.referencedSegmentDir(), '136397-rect.tif' ) ):
        ...   os.remove(
        ...    os.path.join( myI.referencedSegmentDir(), '136397-rect.tif' ) )
        ...
        >>> myLocalizationRow = myI.localization( 1000000 )
        >>> myFrameRow = myI.frameForLocalization( myLocalizationRow['id'] )
        >>> mySegmentRow = myI.segmentForFrame( myFrameRow['segment_id'] )
        >>> myAuxFileRow = myI.auxfileForSegment( myFrameRow['segment_id'] )
        >>> myFileTypeRow = myI.fileTypeForAuxFile( myAuxFileRow['file_type'] )
        >>> myImage, myWorld = myI.referencedThumb(
        ...    myLocalizationRow, myFrameRow, mySegmentRow, myAuxFileRow,
        ...    myFileTypeRow )
        Writing segment image with dimensions x: 1004, y: 17496
        Rectifying /tmp/136397.jpg
        '''
        mySegmentId = theFrameRow['segment_id']
        myBlob = theAuxFileRow['file']
        try:
            mySegmentJpeg = self.extractBlobToJpeg(mySegmentId, myBlob)
            mySegmentWkt = 'SRID=4326;' + theSegmentRow['geo_shape']
            #print mySegmentWkt
            mySegmentGeometry = GEOSGeometry(mySegmentWkt)
            mySegmentFile = self.rectifyImage(mySegmentJpeg, mySegmentGeometry)

            myLocalizationWkt = 'SRID=4326; %s' % (
                theLocalizationRow['geo_time_info'],)
            #print myLocalizationWkt
            myLocalizationGeometry = GEOSGeometry(myLocalizationWkt)
            myDestinationImage = str(theLocalizationRow['id']) + '.jpg'
            return self.clipImage(
                mySegmentFile, myDestinationImage, mySegmentGeometry,
                myLocalizationGeometry)
        except:
            self.cleanup()
            raise

    ########################################################
    # Helper functions for blob extraction to jpgs
    ########################################################

    def getBlockPositionsForBlob(self, theBlob):
        '''
        In each blob is a series of embedded jpg images. This function
        computes the offset of the start of each jpg image by looking for the
        initial JFIF tag. It returns a list of these block offsets
        '''
        myLength = len(theBlob)
        #print 'File Length: %s' % myLength
        myPosition = 0
        myLastPosition = 0
        theFileNo = 0
        myList = []
        while not myPosition < 0:
            theFileNo = theFileNo + 1
            myLastPosition = myPosition
            #print 'Searching from : %s' % ( myPosition + 10 )
            myPosition = theBlob.find('JFIF', myPosition + 10) - 6
            #print 'JFIF at %s' % (myPosition )
            if myLastPosition > 0 and myPosition > 0:
                myList.append(myPosition)
            elif len(myList) == 0:
                myList.append(myPosition)
            else:
                myList.append(myLength)
            #print 'myPosition: %s ' % myPosition
            #print 'myLastPosition: %s ' % myLastPosition

        return myList

    def blockToData(self, theStart, theEnd, theBlob):
        '''Extracts a block of binary date from a blob'''
        theBlob.seek(theStart)
        myBlockValue = theBlob.read(theEnd - theStart)
        return myBlockValue

    def dataToImage(self, theData, theFile):
        '''Saves a block of binary data as file'''
        #print 'Saving %s' % theFile
        myJpg = open(theFile, mode='wb')
        myJpg.write(theData)
        myJpg.close()

    def createGroupFile(self, theFileList, theOutputFile):
        '''
        This function will merge 1 or more images into a single file. The
        images will be pasted into incremental positions down the file.
        Note: You need to hand build PIL - see install notes for details!
        '''
        #print theFileList

        if len(theFileList) < 1:
            return
        if os.path.exists(theOutputFile):
            os.remove(theOutputFile)

        # Open the first image to get its dims
        myWidth = 0
        myHeight = 0
        for myFile in theFileList:
            myImage = Image.open(myFile)
            # Get the image metrics nicely so we can paste it into the quad
            # image
            mySize = myImage.size
            myX = mySize[0]
            myY = mySize[1]
            myHeight += myY
            if myX > myWidth:
                myWidth = myX

        print 'Writing segment image with dimensions x: %i, y: %i' % (
            int(myWidth), int(myHeight))
        mySize = (myWidth, myHeight)
        myOutImage = Image.new('RGB', mySize)

        myLastY = 0
        for myFile in theFileList:
            myImage = Image.open(myFile)
            mySize = myImage.size
            myX = mySize[0]
            myY = mySize[1]
            #determine the position to paste the block into
            myBox = (0, myLastY, myX, myLastY + myY)
            # now paste the blocks in
            try:
                myOutImage.paste(myImage, myBox)
                myLastY += myY
            except IOError as e:
                traceback.print_exc(file=sys.stdout)
                raise
            except ValueError:
                print 'Image %s,%s can\'t go into %s,%s at position 0,%s' % (
                    myX, myY, myWidth, myHeight, myLastY - myY)
                myLastY += myY
                continue
        # save up
        myOutImage.save(theOutputFile)

    def removeBlocks(self, theArray):
        '''
        This function removes temporary files containing blocks (individual
            jpg sub images).
        '''
        for myBlockFile in theArray:
            try:
                os.remove(myBlockFile)
            except:
                pass

    def extractBlobToJpeg(self, theSegmentId, theBlob):
        myBlobFileName = os.path.join(
            self.scratchDir(), str(theSegmentId) + '.blob')
        # use cached image if possible
        myJpegFileName = os.path.join(
            self.unreferencedSegmentDir(), str(theSegmentId) + '.jpg')
        if os.path.exists(myJpegFileName):
            print 'Using cached segment image'
            return myJpegFileName

        myFile = file(myBlobFileName, 'wb')
        try:
            theBlob.open()
            myStats = theBlob.stat()
            #print 'Blob stats: size = %s' % str(myStats['size'])
        except Exception, myException:
            print 'Sblob open failed (%s)' % str(myException)
            raise
        try:
            # First write the whole blob out to a file
            myData = theBlob.read(theBlob.stat()['size'])
            myFile.write(myData)
            myFile.close()
            #print 'Wrote ' + myFileName

        except Exception, myException:
            print 'Sblob read failed (%s)' % str(myException)
            raise

        myBlob = open(myBlobFileName, mode='rb')
        myValue = myBlob.read()
        myArray = self.getBlockPositionsForBlob(myValue)
        #print myArray
        # used to hold filenames that will be combined into a single file
        myGroupFileArray = []
        myBlockTally = 0
        myErrorTally = 0
        #print '%s block(s) in this file' % ( len( myArray ) - 1 )
        for myPosition in range(0, len(myArray)):
            if myPosition == 0:
                continue  # skip the first position marker
            myBlockTally += 1
            myStart = myArray[myPosition - 1]
            myEnd = myArray[myPosition]
            myData = self.blockToData(myStart, myEnd, myBlob)
            myJpgFile = os.path.join(self.scratchDir(), '%sblock%s.jpg' % (
                theSegmentId, myBlockTally))
            self.dataToImage(myData, myJpgFile)
            myGroupFileArray.append(myJpgFile)
        # We are accummulating files in blocks of myBlocksInGroup
        # or any remaining at the end of the segment
        # write this group of myBlocksInGroup files into a single file
        # print 'Block Tally: %s' % myBlockTally
        #print 'Writing %s' % myJpegFileName
        try:
            self.createGroupFile(myGroupFileArray, myJpegFileName)
            self.removeBlocks(myGroupFileArray)
            os.remove(myBlobFileName)
        except IOError as e:
            if e.errno == 28:  # out of space exception
                print 'Fatal Error - out of disk space!'
                print 'Last file processed was: %s' % myFile
                print e
                traceback.print_exc(file=sys.stdout)
                raise
        except Exception as e:
            self.removeBlocks(myGroupFileArray)
            os.remove(myBlobFileName)
            raise

        return myJpegFileName

    def coordIsOnBounds(self, theCoord, theExtents):
        '''
        Helper function to determine if a vertex touches the bounding box
        '''
        if theCoord[0] == theExtents[0] or theCoord[0] == theExtents[2]:
            return True  # xmin,xmax
        if theCoord[1] == theExtents[1] or theCoord[1] == theExtents[3]:
            return True  # ymin,ymax
        return False

    def sortCandidates(self, theCandidates, theExtents, theCentroid):
        '''Return the members of the array in order TL, TR, BR, BL'''
        #for myCoord in theCandidates:
        #  print myCoord
        mySortedCandidates = []
        myTopLeft = None
        #print 'Defalt Candidate: %s' %  str( myTopLeft )
        for myCoord in theCandidates:
            #print 'Evaluating: %s' % str( myCoord )
            if myCoord[1] < theCentroid[1]:
                continue  # its in the bottom half so ignore
            if not myTopLeft:
                myTopLeft = myCoord
                continue
            if myCoord[0] < myTopLeft[0]:
                myTopLeft = myCoord
                #print 'Computed Candidate: %s' %  str( myTopLeft )

        mySortedCandidates.append(myTopLeft)
        theCandidates.remove(myTopLeft)

        myTopRight = None
        #print 'Defalt Candidate: %s' %  str( myTopRight )
        for myCoord in theCandidates:
            #print 'Evaluating: %s' % str( myCoord )
            if myCoord[1] < theCentroid[1]:
                continue  # its in the bottom half so ignore
            if not myTopRight:
                myTopRight = myCoord
                continue
            if myCoord[0] > myTopRight[0]:
                myTopRight = myCoord
                #print 'Computed Candidate: %s' %  str( myTopRight )

        mySortedCandidates.append(myTopRight)
        theCandidates.remove(myTopRight)

        myBottomRight = None
        #print 'Defalt Candidate: %s' %  str( myBottomRight )
        for myCoord in theCandidates:
            #print 'Evaluating: %s' % str( myCoord )
            if myCoord[1] > theCentroid[1]:
                continue  # its in the top half so ignore
            if not myBottomRight:
                myBottomRight = myCoord
                continue
            if myCoord[0] > myBottomRight[0]:
                myBottomRight = myCoord
                #print 'Computed Candidate: %s' %  str( myBottomRight )

        mySortedCandidates.append(myBottomRight)
        theCandidates.remove(myBottomRight)

        myBottomLeft = theCandidates[0]
        mySortedCandidates.append(myBottomLeft)  # the only one remaining
        theCandidates.remove(myBottomLeft)

        return mySortedCandidates

    def rectifyImage(self, theSegmentJpeg, theGeometry):
        '''
        Given a path to an image, and a geometry, register the image such that
        its corners correspond to the corners of the geometry.

        Note it does not use simply the bounding box but rather the
        TL, TR, BL and BR extremes of the supplied geometry.

        The rectified image base name will be suffixed with '-rect.tif' and
        returned as a string on success. Failure will raise an exception.
        '''
        myFileBase = os.path.split(theSegmentJpeg)[1]
        myFileBase = os.path.splitext(myFileBase)[0]
        myOutputPath = os.path.join(
            self.referencedSegmentDir(), myFileBase + '-rect.tif')
        if os.path.exists(myOutputPath):
            print 'Using cached rectified image %s ' % myOutputPath
            return myOutputPath
        print 'Rectifying %s' % theSegmentJpeg
        myImage = None
        try:
            myImage = Image.open(theSegmentJpeg)
            # We need to know the pixel dimensions of the segment so that we
            # can create GCP's
        except:
            print 'File not found %s' % theSegmentJpeg
            raise

        myImageXDim = myImage.size[0]
        myImageYDim = myImage.size[1]
        # Get the minima, maxima - used to test if we are on the edge
        myExtents = theGeometry.extent
        #print 'Envelope: %s %s' % ( len( myExtents), str( myExtents ) )
        # There should only be 4 vertices touching the edges of the
        # bounding box of the shape. If we assume that the top right
        # corner of the poly is on the right edge of the bbox, the
        # bottom right vertex is on the bottom edge and so on
        # we can narrow things down to just the leftside two and rightside
        # two vertices. Thereafter, determining which is 'top' and which
        # is bottom is a simple case of comparing the Y values in each
        # grouping.
        #
        # Note the above logic makes some assumptions about the oreintation of
        # the swath which may not hold true for every sensor.
        #
        myCandidates = []
        try:
            # should only be a single arc in our case!
            for myArc in theGeometry.coords:
                for myCoord in myArc[:-1]:
                    if self.coordIsOnBounds(myCoord, myExtents):
                        myCandidates.append(myCoord)
        except:
            raise
        #print 'Candidates Before: %s %s ' % (
        #    len(myCandidates), str(myCandidates))
        myCentroid = theGeometry.centroid
        try:
            myCandidates = self.sortCandidates(
                myCandidates, myExtents, myCentroid)
        except:
            raise
        #print 'Candidates After: %s %s ' % (len(myCandidates),
        #    str( myCandidates ) )
        myTL = myCandidates[0]
        myTR = myCandidates[1]
        myBR = myCandidates[2]
        myBL = myCandidates[3]

        myString = (
            'gdal_translate -a_srs "EPSG:4326" -gcp 0 0 %s %s -gcp %s 0 %s %s '
            '-gcp %s %s %s %s -gcp 0 %s %s %s -of GTIFF -co COMPRESS=DEFLATE '
            '-co TILED=YES %s %s' % (
                myTL[0], myTL[1],
                myImageXDim, myTR[0], myTR[1],
                myImageXDim, myImageYDim, myBR[0], myBR[1],
                myImageYDim, myBL[0], myBL[1],
                theSegmentJpeg,
                myOutputPath))
        #print myString
        os.system(myString)
        return myOutputPath

    def clipImage(
            self, theSourceImage, theDestinationImage, theSourceGeometry,
            theDestinationGeometry):
        '''
        Clip a georeferenced image from a georeferenced source image using the
        provided polygon. The source geometry should match the footprint of the
        georeferenced source image.

        return Full path to georeferenced clip, full path to world file
        '''
        if not os.path.exists(theSourceImage):
            raise ClipError('Source dataset does not exist')
        myDirectory = self.referencedSceneDir()
        myFile = os.path.split(theDestinationImage)[1]
        myFileBase = os.path.splitext(myFile)[0]
        myFileExt = os.path.splitext(myFile)[1]
        if not os.path.isdir(myDirectory):
            try:
                os.makedirs(myDirectory)
            except OSError:
                raise ClipError('Failed to make output directory...quitting')
        myTiffThumbnail = os.path.join(self.scratchDir(), myFileBase + '.tif')
        myWktFile = os.path.join(self.scratchDir(), myFileBase + '.wkt')
        # Note: Initially I used PIL to do this (simpler, less deps), but it
        # cant open all tiffs it seems
        try:
            myImage = osgeo.gdal.Open(theSourceImage)
        except:
            raise ClipError(
                'ClipImage : File could not be opened %s' % theSourceImage)

        myImageXDim = myImage.RasterXSize
        myImageYDim = myImage.RasterYSize
        #using convex hull will reduce the number of points we need to iterate
        myIntersectedGeometry = theDestinationGeometry.intersection(
            theSourceGeometry)
        # Get the minima, maxima - used to test if we are on the edge
        myExtents = None
        try:
            myExtents = myIntersectedGeometry.extent
        except:
            raise ClipError(
                'Intersected geometry extents could not be obtained')
        myWktString = myIntersectedGeometry.wkt
        file(myWktFile, 'wt').write(myWktString)
        # clip to bbox (for image size)
        # TODO: reinstate mask everything but the scene contents(using cutline)
        myString = (
            'gdalwarp -of GTiff -co COMPRESS=DEFLATE -co TILED=YES -te %s %s '
            '%s %s %s %s' % (
                myExtents[0], myExtents[1], myExtents[2], myExtents[3],
                theSourceImage, myTiffThumbnail))
        #print myString
        os.system(myString)
        # Now convert the tiff to a jpg with world file
        # We do this as a second step as gdal does not support direct creation
        # of a jpg from gdalwarp
        myOutJpg = os.path.join(self.referencedSceneDir(), theDestinationImage)
        myOutWld = os.path.join(self.referencedSceneDir(), myFileBase + '.wld')
        myString = 'gdal_translate -of JPEG -co WORLDFILE=YES %s %s' % (
            myTiffThumbnail, myOutJpg)
        os.system(myString)
        # Clean away the tiff
        os.remove(myTiffThumbnail)
        os.remove(myWktFile)
        return myOutJpg, myOutWld


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
