import sys
import os
import traceback

import osgeo.gdal

from django_project.catalogue.models import *
from acscatalogue.models import *

from django_project.core.utils import zeroPad

#################################################################
# Helper methods for computing various properties and creating objects
#################################################################

def utmZoneFromLatLon( thePoint ):
    """Return the name of the UTM zone given a latitude and longitude.
       @return a tuple e.g. 32734, UTM34S"""
    myLon = thePoint.x
    myLat = thePoint.y
    mySuffix = None
    myPrefix = "326" #all north utm CRS's begin with 327
    myHemisphere = "N"
    if myLat < 0:
        myPrefix = "327"
        myHemisphere = "S"
    myZoneMin = -180
    myZoneIncrement = 6
    myCurrentZone = 1
    try:
        while myZoneMin < 180:
            if myLon >= myZoneMin and myLon < ( myZoneMin + 6 ):
                mySuffix = zeroPad( str( myCurrentZone ), 2 )
                myResult = myPrefix+mySuffix,"UTM"+mySuffix+myHemisphere
                return myResult
            myZoneMin += myZoneIncrement
            myCurrentZone += 1
        print "Point out of range for UTM zone calculation"
    except Exception, e:
        print "Failed to define a new UTM zone for Lon: %s, Lat: %s" % ( thePoint.x, thePoint.y )
        raise e
    return None

def getOrCreateMission(theAbbreviation, theName):
    # Mission...
    myMissions = Mission.objects.filter(name=theName)
    if len( myMissions ) == 0:
        print "Creating new mission with Abbreviation: %s, Name: %s" % ( theAbbreviation, theName )
        myMission = Mission(abbreviation=theAbbreviation,name=theName)
        myMission.save()
    else:
        myMission = myMissions[0]
    return myMission

def getOrCreateMissionSensor(theAbbreviation, theName):
    mySensors = MissionSensor.objects.filter(name=theName)
    if len( mySensors ) == 0:
        mySensor = MissionSensor(abbreviation=theAbbreviation,name=theName,has_data=True)
        mySensor.save()
    else:
        mySensor = mySensors[0]
    return mySensor

def getOrCreateSensorType(theAbbreviation, theName):
    mySensorTypes = SensorType.objects.filter(abbreviation=theAbbreviation)
    if len( mySensorTypes ) == 0:
        mySensorType = SensorType(abbreviation=theAbbreviation,name=theName)
        mySensorType.save()
    else:
        mySensorType = mySensorTypes[0]
    return mySensorType

def getOrCreateAcquisitionMode(theAbbreviation, theName, theGeometricResolution, theBandCount):
    # Acquisition Mode
    myAcquisitionModes = AcquisitionMode.objects.filter(abbreviation=theAbbreviation)
    if len( myAcquisitionModes ) == 0:
        myAcquisitionMode = AcquisitionMode(abbreviation=theAbbreviation,name=theName,geometric_resolution=theGeometricResolution,band_count=theBandCount)
        myAcquisitionMode.save()
    else:
        myAcquisitionMode = myAcquisitionModes[0]
    return myAcquisitionMode

def getOrCreateProcessingLevel(theAbbreviation, theName):
    # Processing level
    myProcessingLevels = ProcessingLevel.objects.filter(abbreviation=theAbbreviation)
    if len( myProcessingLevels ) == 0:
        myProcessingLevel = ProcessingLevel(abbreviation=theAbbreviation,name=theName)
        myProcessingLevel.save()
    else:
        myProcessingLevel = myProcessingLevels[0]
    return myProcessingLevel

def getOrCreateInstitution(theName, theAddress1, theAddress2, theAddress3, thePostCode):
    myInstitutions = Institution.objects.filter(name=theName)
    if len( myInstitutions ) == 0:
        myInstitution = Institution(name = theName,
                               address1 = theAddress1,
                               address2 = theAddress2,
                               address3 = theAddress3,
                               post_code = thePostCode)
        myInstitution.save()
    else:
        myInstitution = myInstitutions[0]
    return myInstitution



def getOrCreateLicense(theName, theDetails):
    # License
    myLicenses = License.objects.filter(name=theName)
    if len( myLicenses ) == 0:
        myLicense = License(name=theName,details=theDetails)
        myLicense.save()
    else:
        myLicense = myLicenses[0]
    return myLicense

def getOrCreateProjection(theEpsgCode, theProjectionName):
    myProjections = Projection.objects.filter( epsg_code=theEpsgCode )
    if len( myProjections ) == 0:
        myProjection = Projection( epsg_code=theEpsgCode,name=theProjectionName )
        myProjection.save()
    else:
        myProjection = myProjections[0]
    return myProjection

def getOrCreateQuality(theName):
    # Quality
    myQualities = Quality.objects.filter(name=theName)
    if len( myQualities ) == 0:
        myQuality = Quality(name=theName)
        myQuality.save()
    else:
        myQuality = myQualities[0]
    return myQuality

def getOrCreateCreatingSoftware(theName, theVersion):
    # CreatingSoftware
    myCreatingSoftwares = CreatingSoftware.objects.filter(name=theName,version=theVersion)
    if len( myCreatingSoftwares ) == 0:
        myCreatingSoftware = CreatingSoftware(name=theName,version=theVersion)
        myCreatingSoftware.save()
    else:
        myCreatingSoftware = myCreatingSoftwares[0]
    return myCreatingSoftware


######################################################################################
# All satellite specific code is refactored down into the following methods
######################################################################################


def getSatelliteSpecificMetadata( theSatelliteName, theSegment, theFrame ):
    myString = ""
    if theSatelliteName == "Landsat":
        myLandsatSegment = LandsatSegment.objects.filter( segmentCommon=theSegment )[0]
        myLandsatFrame = LandsatFrame.objects.filter( localization=theFrame.localization )[0]
        # Landsat specific - frame
        myString += "Frame Center Latitude: %s\n" %  myLandsatFrame.centreLat
        myString += "Frame Center Longitude: %s\n" %  myLandsatFrame.centreLon
        myString += "Frame Center Time: %s " % myLandsatFrame.centreTime
        myString += "Frame Sun Azimuth: %s\n" % myLandsatFrame.sunAz
        myString += "Frame Sun Elevation: %s\n" % myLandsatFrame.sunElev
        myString += "Frame fopScene: %s\n" % myLandsatFrame.fopScene
        myString += "Frame Horiziontal data shift: %s\n" % myLandsatFrame.hdShift
        myString += "Frame Quality: %s\n" % myLandsatFrame.sQuality
        myString += "Frame SB Present: %s\n" % myLandsatFrame.sbPresent
        myString += "Frame Band Gain: %s\n" % myLandsatFrame.bGain
        myString += "Frame Band Gain Change: %s\n" % myLandsatFrame.bgChange
        myString += "Frame Band sl Gain Change: %s\n" % myLandsatFrame.bslgainchange
        myString += "Frame Common Begin Time Code: %s\n" % myLandsatSegment.begTimeCode
        myString += "Frame Common Segment End Time Code: %s\n" % myLandsatSegment.endTimeCode
        # Landsat specific - segment
        myString += "Segment Order: %s\n" % myLandsatSegment.segmentOrder
        myString += "Segment Begin Time Code: %s\n" % myLandsatSegment.begTimeCode
        myString += "Segment End Time Code: %s\n" % myLandsatSegment.endTimeCode
        myString += "Segment First Fc: %s\n" % myLandsatSegment.firstFrameFc
        myString += "Segment Last Fc: %s\n" % myLandsatSegment.lastFrameFc
        myString += "Segment Ellipsoid: %s\n" % myLandsatSegment.ellipsoid
        myString += "Segment Ellipsoid Param1: %s\n" % myLandsatSegment.ellipsParam1
        myString += "Segment Ellipsoid Param2: %s\n" % myLandsatSegment.ellipsParam2
        myString += "Segment Ellipsoid Param3: %s\n" % myLandsatSegment.ellipsParam3
        myString += "Segment Ellipsoid Param4: %s\n" % myLandsatSegment.ellipsParam4
        myString += "Segment Channel: %s\n" % myLandsatSegment.channel
        myString += "Segment Meta Version: %s\n" % myLandsatSegment.metaVersionNo
        myString += "Segment Band Present: %s\n" % myLandsatSegment.bandPresent
    elif theSatelliteName in ["E-Ers", "J_Ers"]:
        try:
            myErsSegment = ErsSegment.objects.filter( segmentCommon=theSegment )[0]
            myErsFrame = ErsFrame.objects.filter( localization=theFrame.localization )[0]
        except:
            #print "No ers specific data could be found"
            return myString
        # Ers specific - frame
        myString += "Frame meanI: %s\n" % myErsFrame.meanI
        myString += "Frame meanQ: %s\n" % myErsFrame.meanQ
        myString += "Frame sdevI: %s\n" % myErsFrame.sdevI
        myString += "Frame sdevQ: %s\n" % myErsFrame.sdevQ
        myString += "Frame missLinPerc: %s\n" % myErsFrame.missLinPerc
        myString += "Frame dopplerCentroid: %s\n" % myErsFrame.dopplerCentroid
        myString += "Frame blockNumber: %s\n" % myErsFrame.blockNumber
        myString += "Frame lineNumber: %s\n" % myErsFrame.lineNumber
        myString += "Frame maxI: %s\n" % myErsFrame.maxI
        myString += "Frame MaxQ: %s\n" % myErsFrame.maxQ
        # Ers specific - segement
        myString += "Segment : segmentOrder %s\n" % myErsSegment.segmentOrder
        myString += "Segment : rollAngle %s\n" % myErsSegment.rollAngle
        myString += "Segment : begTimeCode %s\n" % myErsSegment.begTimeCode
        myString += "Segment : endTimeCode %s\n" % myErsSegment.endTimeCode
        myString += "Segment : begFormat %s\n" % myErsSegment.begFormat
        myString += "Segment : endFormat %s\n" % myErsSegment.endFormat
        myString += "Segment : icuOnboardBegTime %s\n" % myErsSegment.icuOnboardBegTime
        myString += "Segment : icuOnboardEndTime %s\n" % myErsSegment.icuOnboardEndTime
        myString += "Segment : compressionMode_id %s\n" % myErsSegment.compressionMode_id
        myString += "Segment : firstFrameNum %s\n" % myErsSegment.firstFrameNum
        myString += "Segment : lastFrameNum %s\n" % myErsSegment.lastFrameNum
        myString += "Segment : pulseRepInt %s\n" % myErsSegment.pulseRepInt
        myString += "Segment : simpleRate %s\n" % myErsSegment.simpleRate
        myString += "Segment : calibSubAtt %s\n" % myErsSegment.calibSubAtt
        myString += "Segment : receivGain %s\n" % myErsSegment.receivGain
        myString += "Segment : ellipsoid_id %s\n" % myErsSegment.ellipsoid_id
        myString += "Segment : ellipsParam1 %s\n" % myErsSegment.ellipsParam1
        myString += "Segment : ellipsParam2 %s\n" % myErsSegment.ellipsParam2
        myString += "Segment : ellipsParam3 %s\n" % myErsSegment.ellipsParam3
        myString += "Segment : ellipsParam4 %s\n" % myErsSegment.ellipsParam4
        myString += "Segment : padFirstFrame %s\n" % myErsSegment.padFirstFrame
        myString += "Segment : padLastFrame %s\n" % myErsSegment.padLastFrame
    elif theSatelliteName == "Noaa":
        try:
            myNoaaSegment = NoaaSegment.objects.filter( segmentCommon=theSegment )[0]
            myNoaaFrame = NoaaFrame.objects.filter( localization=theFrame.localization )[0]
        except:
            #print "No Noaa specific data could be found"
            return myString
        # Ers specific - segement
        myString += "Segment :dataMode_id %s\n" % myNoaaSegment.dataMode_id
        myString += "Segment :eqcrxTime  %s\n" % myNoaaSegment.eqcrxTime
        myString += "Segment :eqLon  %s\n" % myNoaaSegment.eqLon
        myString += "Segment :procLevel  %s\n" % myNoaaSegment.procLevel
        myString += "Segment :bandMode  %s\n" % myNoaaSegment.bandMode
        myString += "Segment :pixFormat  %s\n" % myNoaaSegment.pixFormat
        myString += "Segment :arcCenter  %s\n" % myNoaaSegment.arcCenter
    return myString

def getSensorAndMode( theSatelliteName, theSegment, theFrame ):
    mySensorType = None
    myAcquisitionMode = None
    if theSatelliteName == "Landsat":
        mySensorType = getOrCreateSensorType("MST","Multispectral + Thermal")
        myAcquisitionMode = getOrCreateAcquisitionMode( "HRT","Multispectral and Thermal", 0, 0 )
    elif theSatelliteName in ["E-Ers", "J_Ers"]:
        mySensorType = getOrCreateSensorType("AMI","AMI")
        myAcquisitionMode = getOrCreateAcquisitionMode( "VV","Vertical / Vertical Polarisation", 0, 0 )
    elif theSatelliteName == "Noaa":
        mySensorType = getOrCreateSensorType("AVHR","Advanced Very High Resolution Radiometer")
        myAcquisitionMode = getOrCreateAcquisitionMode( "MS","Multispectral", 0, 0 )
    elif theSatelliteName == "Spot":
        mySpotSegment = SpotSegment.objects.filter( segmentCommon=theSegment )[0]
        mySensorName = theSegment.sensor.name
        myCamera = str( mySpotSegment.channel )
        mySensorType = getOrCreateSensorType("CAM" + myCamera,"Spot Camera " + myCamera)
        myAcquisitionMode = getOrCreateAcquisitionMode( mySpotSegment.mode , mySpotSegment.mode, 0, 0 )
        #if mySensorName == "Spot 1,2,3 HRV Pan":
        #  mySensorType = getOrCreateSensorType("CAM1","Spot Camera 1")
        #  myAcquisitionMode = getOrCreateAcquisitionMode( "M","Monochromatic", 0, 0 )
        #elif mySensorName == "Spot 1,2,3 HRV Xs":
        #  mySensorType = getOrCreateSensorType("CAM1","Spot Camera 1")
        #  myAcquisitionMode = getOrCreateAcquisitionMode( "Xs","Multispectral", 0, 0 )
        #elif mySensorName == "Spot 4 G,R,NIR,SWIR":
        #  mySensorType = getOrCreateSensorType("CAM1","Spot Camera 1")
        #  myAcquisitionMode = getOrCreateAcquisitionMode( "Xi","Multispectral", 0, 0 )
        #elif mySensorName == "Spot 4 Pan":
        #  mySensorType = getOrCreateSensorType("CAM1","Spot Camera 1")
        #  myAcquisitionMode = getOrCreateAcquisitionMode( "AB","Multispectral", 0, 0 )
        #else:
            #print "Error unknown spot sensor type"
    return mySensorType, myAcquisitionMode


def applySensorSpecificProperties( theSatelliteName, theProduct, theSegment, theFrame ):
    if theSatelliteName == "Landsat":
        myLandsatSegment = LandsatSegment.objects.filter( segmentCommon=theSegment )[0]
        myLandsatFrame = LandsatFrame.objects.filter( localization=theFrame.localization )[0]
        theProduct.solar_zenith_angle = myLandsatFrame.sunElev
        theProduct.solar_azimuth_angle = myLandsatFrame.sunAz
        return
    elif theSatelliteName in ["E-Ers", "J_Ers"]:
        try:
            myErsSegment = ErsSegment.objects.filter( segmentCommon=theSegment )[0]
            myErsFrame = ErsFrame.objects.filter( localization=theFrame.localization )[0]
            #Wolfgang to determine which properties are useful
        except:
            pass
        return
    elif theSatelliteName == "Noaa":
        try:
            myNoaaSegment = NoaaSegment.objects.filter( segmentCommon=theSegment )[0]
            myNoaaFrame = NoaaFrame.objects.filter( localization=theFrame.localization )[0]
            #Wolfgang to determine which properties are useful
        except:
            pass
    elif theSatelliteName == "Spot":
        try:
            mySpotSegment = SpotSegment.objects.filter( segmentCommon=theSegment )[0]
            mySpotFrame = SpotFrame.objects.filter( localization=theFrame.localization )[0]
            #determine which properties are useful
        except:
            pass
        return

def getProductTypeForSatellite( theSatelliteName ):
    myOpticalList = ["Landsat","Mos","Spot","Irs","Noaa","Orbview"]
    myRadarList = ["J_Ers","E-Ers","Irs","Radarsat"]
    if theSatelliteName in myOpticalList:
        return "Optical"
    elif theSatelliteName in myRadarList:
        return "Radar"
    else:
        return "Atmospheric" #no support for this yet

def refreshSacIds():
    print "Refreshing all SAC product id's"
    mySuccessCount = 0
    for myProduct in GenericProduct.objects.all():
        myProduct.setSacProductId()
        myProduct.save()
        mySuccessCount += 1
        # Show progress occasionaly
        if mySuccessCount % 10000 == 0:
            print "Records successfully processed: %s" % mySuccessCount

##################################################################
# These next functions are for acs informix segment registration
##################################################################

def coordIsOnBounds( theCoord, theExtents ):
    """Helper function to determine if a vertex touches the bounding box"""
    if theCoord[0] == theExtents[0] or theCoord[0] == theExtents[2]: return True #xmin,xmax
    if theCoord[1] == theExtents[1] or theCoord[1] == theExtents[3]: return True #ymin,ymax
    return False

#######################################################

def sortCandidates( theCandidates, theExtents, theCentroid ):
    """Return the members of the array in order TL, TR, BR, BL"""
    #for myCoord in theCandidates:
    #  print myCoord
    mySortedCandidates = []
    myTopLeft = None
    #print "Defalt Candidate: %s" %  str( myTopLeft )
    for myCoord in theCandidates:
        #print "Evaluating: %s" % str( myCoord )
        if myCoord[1] < theCentroid[1]:
            continue # its in the bottom half so ignore
        if not myTopLeft:
            myTopLeft = myCoord
            continue
        if myCoord[0] < myTopLeft[0]:
            myTopLeft = myCoord
            #print "Computed Candidate: %s" %  str( myTopLeft )

    mySortedCandidates.append( myTopLeft )
    theCandidates.remove( myTopLeft )

    myTopRight = None
    #print "Defalt Candidate: %s" %  str( myTopRight )
    for myCoord in theCandidates:
        #print "Evaluating: %s" % str( myCoord )
        if myCoord[1] < theCentroid[1]:
            continue # its in the bottom half so ignore
        if not myTopRight:
            myTopRight = myCoord
            continue
        if myCoord[0] > myTopRight[0]:
            myTopRight = myCoord
            #print "Computed Candidate: %s" %  str( myTopRight )

    mySortedCandidates.append( myTopRight )
    theCandidates.remove( myTopRight )

    myBottomRight = None
    #print "Defalt Candidate: %s" %  str( myBottomRight )
    for myCoord in theCandidates:
        #print "Evaluating: %s" % str( myCoord )
        if myCoord[1] > theCentroid[1]:
            continue # its in the top half so ignore
        if not myBottomRight:
            myBottomRight = myCoord
            continue
        if myCoord[0] > myBottomRight[0]:
            myBottomRight = myCoord
            #print "Computed Candidate: %s" %  str( myBottomRight )

    mySortedCandidates.append( myBottomRight )
    theCandidates.remove( myBottomRight )

    myBottomLeft = theCandidates[0]
    mySortedCandidates.append( myBottomLeft ) #the only one remaining
    theCandidates.remove( myBottomLeft  )

    return mySortedCandidates

#######################################################

def rectifyImage( theInputPath, theOutputPath, theAuxFile ):
    myId = str( theAuxFile.original_id )
    myPath = os.path.join(theInputPath,myId + "segment.jpg")
    myOutputPath = os.path.join(theOutputPath,myId + "segment-proj.tif")
    try:
        myImage = Image.open( myPath )
        # We need to know the pixel dimensions of the segment so that we can create GCP's
    except:
        print "File not found %s" % myPath
        return "False"

    myImageXDim = myImage.size[0]
    myImageYDim = myImage.size[1]
    mySegment = theAuxFile.segmentCommon
    #using convex hull will reduce the number of points we need to iterate
    myGeometry = mySegment.geometry
    myString = file("scripts/segmenttemplate.kml","rt").read()
    myKmlString = myString.replace("[POLYGON]",myGeometry.kml)
    file(os.path.join(theOutputPath,myId + "segment.kml"),"wt").write(myKmlString)
    # Get the minima, maxima - used to test if we are on the edge
    myExtents = myGeometry.extent
    #print "Envelope: %s %s" % ( len( myExtents), str( myExtents ) )
    # There should only be 4 vertices touching the edges of the
    # bounding box of the shape. If we assume that the top right
    # corner of the poly is on the right edge of the bbox, the
    # bottom right vertex is on the bottom edge and so on
    # we can narrow things down to just the leftside two and rightside
    # two vertices. Thereafter, determining which is 'top' and which
    # is bottom is a simple case of comparing the Y values in each grouping.
    #
    # Note the above logic makes some assumptions about the oreintation of
    # the swath which may not hold true for every sensor.
    #
    myCandidates = []
    try:
        for myArc in myGeometry.coords: #should only be a single arc in our case!
            for myCoord in myArc[:-1]:
                if coordIsOnBounds( myCoord, myExtents ):
                    myCandidates.append( myCoord )
    except:
        return "False"
    #print "Candidates Before: %s %s " % (len(myCandidates), str( myCandidates ) )
    myCentroid = myGeometry.centroid
    try:
        myCandidates = sortCandidates( myCandidates, myExtents, myCentroid )
    except:
        return "False"
    #print "Candidates After: %s %s " % (len(myCandidates), str( myCandidates ) )
    myTL = myCandidates[0]
    myTR = myCandidates[1]
    myBR = myCandidates[2]
    myBL = myCandidates[3]
    myKmlString = "<Polygon><outerBoundaryIs><LinearRing><coordinates>%s,%s,0 %s,%s,0 %s,%s,0 %s,%s,0 %s,%s,0</coordinates></LinearRing></outerBoundaryIs></Polygon>" % ( \
          myTL[0], myTL[1], \
          myTR[0],myTR[1], \
          myBR[0],myBR[1], \
          myBL[0],myBL[1], \
          myTL[0], myTL[1] \
          )
    myKmlString = myString.replace("[POLYGON]",myKmlString)
    file(os.path.join(theOutputPath,myId + "segment-proj.kml"),"wt").write(myKmlString)

    myString = "gdal_translate -a_srs 'EPSG:4326' -gcp 0 0 %s %s -gcp %s 0 %s %s -gcp %s %s %s %s -gcp 0 %s %s %s -of GTIFF -co COMPRESS=DEFLATE -co TILED=YES %s %s" % ( \
          myTL[0], myTL[1], \
          myImageXDim, myTR[0],myTR[1], \
          myImageXDim, myImageYDim, myBR[0],myBR[1], \
          myImageYDim, myBL[0],myBL[1], \
          myPath, \
          myOutputPath )
    print myString
    os.system( myString )
    #print "Image X size: %s" % myImageXDim
    #print "Image Y size: %s" % myImageYDim
    #print "Top left X: %s, Y:%s" %(myTL[0],myTL[1])
    #print "Top right X: %s, Y:%s" %(myTR[0],myTR[1])
    #print "Bottom left X: %s, Y:%s" %(myBL[0],myBL[1])
    #print "Bottom right X: %s, Y:%s" %(myBR[0],myBR[1])
    return "True"

##################################################################
# This next function is for acs informix scene registration
##################################################################

def clipImage( theScenesPath, theSegmentsPath, theAuxFile, theFrame ):
    if not os.path.isdir( theScenesPath ):
        try:
            os.makedirs( theScenesPath )
        except OSError:
            print "Failed to make output directory...quitting"
            return "False"
    myId = str( theAuxFile.original_id )
    mySegmentFilePath = os.path.join(theSegmentsPath,myId + "segment-proj.tif")
    myTiffThumbnail = os.path.join(theScenesPath, str( theFrame.id ) + "-rectified-clipped.tiff")
    myJpegThumbnail = os.path.join(theScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
    myImage = None
    if not os.path.isfile( mySegmentFilePath ):
        print "ClipImage : File not found %s" % mySegmentFilePath
        return "False"
    # Note: Initially I used PIL to do this (simpler, less deps), but it cant open all tiffs it seems
    try:
        myImage = osgeo.gdal.Open( mySegmentFilePath )
    except:
        traceback.print_exc(file=sys.stdout)
        print "ClipImage : File could not be opened %s" % mySegmentFilePath
        return "False"

    myImageXDim = myImage.RasterXSize
    myImageYDim = myImage.RasterYSize
    mySegment = theAuxFile.segmentCommon
    mySegmentGeometry = mySegment.geometry
    #using convex hull will reduce the number of points we need to iterate
    mySceneGeometry = theFrame.localization.geometry
    myIntersectedGeometry = mySceneGeometry.intersection( mySegmentGeometry )
    # Get the minima, maxima - used to test if we are on the edge
    myExtents = None
    try:
        myExtents = myIntersectedGeometry.extent
    except:
        traceback.print_exc(file=sys.stdout)
        print "Intersected geometry extents could not be obtained %s" % mySegmentFilePath
        return "False"
    # Write geometry of intersection between segment and scene to kml
    # (mainly for testing)
    myString = file("scripts/scenetemplate.kml","rt").read()
    myKmlString = myString.replace("[POLYGON]",myIntersectedGeometry.kml)
    myIntersectedKmlFilePath = os.path.join( theScenesPath , str( theFrame.id ) + "scene-intersection.kml" )
    file( myIntersectedKmlFilePath, "wt" ).write( myKmlString )
    # write actual scene footprint to kml
    myKmlString = myString.replace("[POLYGON]",mySceneGeometry.kml)
    myKmlFilePath = os.path.join( theScenesPath , str( theFrame.id ) + "scene.kml" )
    file( myKmlFilePath, "wt" ).write( myKmlString )
    # clip to bbox (for image size) and mask everything but the scene contents (using cutline)
    myString = "gdalwarp -of GTiff -co COMPRESS=DEFLATE -co TILED=YES -cutline %s %s %s -te %s %s %s %s" % \
             ( myIntersectedKmlFilePath, mySegmentFilePath, myTiffThumbnail, \
               myExtents[0], myExtents[1], myExtents[2], myExtents[3] )
             #( myIntersectedKmlFilePath, myTmpOutputPath, myTiffThumbnail )
    print myString
    os.system( myString )
    # Now convert the tiff to a jpg with world file
    # We do this as a second step as gdal does not support direct creation of a jpg from gdalwarp
    myString = "gdal_translate -of JPEG -co WORLDFILE=YES %s %s" % \
        ( myTiffThumbnail, myJpegThumbnail )
    os.system( myString )
    # Clean away the tiff
    os.remove( myTiffThumbnail )

    return "True"
