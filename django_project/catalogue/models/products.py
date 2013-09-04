"""
SANSA-EO Catalogue - Product related models

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
__date__ = '16/08/2012'
__copyright__ = 'South African National Space Agency'

import sys
import shutil
import logging
logger = logging.getLogger(__name__)

import os
import re
import datetime
import urllib2
from functools import wraps

from django.contrib.gis.db import models
from django.conf import settings
from django.template.loader import render_to_string
#for translation
from django.core.exceptions import ObjectDoesNotExist
# PIL and os needed for making small thumbs
from PIL import Image, ImageFilter, ImageOps

from catalogue.utmzonecalc import utmZoneFromLatLon
from catalogue.dims_lib import dimsWriter
from catalogue.models import (
    Institution,
    License,
    Projection,
    Quality,
    CreatingSoftware,
    PlaceType,
    Place,
    Topic,
    Unit,)

# for thumb georeferencer
#from osgeo.gdalconst import *

# Read from settings
CATALOGUE_ISO_METADATA_XML_TEMPLATE = getattr(
    settings,
    'CATALOGUE_ISO_METADATA_XML_TEMPLATE'
)


def exceptionToString(e):
    """Convert an exception object into a string,
    complete with stack trace info, suitable for display.
    """
    import traceback
    info = "".join(traceback.format_tb(sys.exc_info()[2]))
    return str(e) + "\n\n" + info


##################################################################
# These first functions are for thumb registration
##################################################################

def coordIsOnBounds(theCoord, theExtents):
    """Helper function to determine if a vertex touches the bounding box"""

    if theCoord[0] == theExtents[0] or theCoord[0] == theExtents[2]:
        return True  # xmin,xmax
    if theCoord[1] == theExtents[1] or theCoord[1] == theExtents[3]:
        return True  # ymin,ymax
    return False

#######################################################


class SortCandidateException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def sortCandidates(theCandidates, theExtents, theCentroid):
    """Return the members of the array in order TL, TR, BR, BL"""
    #for myCoord in theCandidates:
    #  print myCoord
    mySortedCandidates = []
    myTopLeft = None
    #print "Defalt Candidate: %s" %  str(myTopLeft)
    for myCoord in theCandidates:
        #print "Evaluating: %s" % str(myCoord)
        if myCoord[1] < theCentroid[1]:
            continue  # its in the bottom half so ignore
        if not myTopLeft:
            myTopLeft = myCoord
            continue
        if myCoord[0] < myTopLeft[0]:
            myTopLeft = myCoord
            #print "Computed Candidate: %s" %  str(myTopLeft)

    if not myTopLeft:
        raise SortCandidateException(
            'Top left coordinate could not be computed in %s' % theCandidates
        )

    mySortedCandidates.append(myTopLeft)
    theCandidates.remove(myTopLeft)

    myTopRight = None
    #print "Defalt Candidate: %s" %  str(myTopRight)
    for myCoord in theCandidates:
        #print "Evaluating: %s" % str(myCoord)
        if myCoord[1] < theCentroid[1]:
            continue  # its in the bottom half so ignore
        if not myTopRight:
            myTopRight = myCoord
            continue
        if myCoord[0] > myTopRight[0]:
            myTopRight = myCoord
            #print "Computed Candidate: %s" %  str(myTopRight)

    if not myTopRight:
        raise SortCandidateException(
            'Top right coordinate could not be computed in %s' % theCandidates
        )

    mySortedCandidates.append(myTopRight)
    theCandidates.remove(myTopRight)

    myBottomRight = None
    #print "Defalt Candidate: %s" %  str(myBottomRight)
    for myCoord in theCandidates:
        #print "Evaluating: %s" % str(myCoord)
        if myCoord[1] > theCentroid[1]:
            continue  # its in the top half so ignore
        if not myBottomRight:
            myBottomRight = myCoord
            continue
        if myCoord[0] > myBottomRight[0]:
            myBottomRight = myCoord
            #print "Computed Candidate: %s" %  str(myBottomRight)

    if not myBottomRight:
        raise SortCandidateException(
            'Bottom right coordinate could not be computed in %s' % (
                theCandidates,
            )
        )

    mySortedCandidates.append(myBottomRight)
    theCandidates.remove(myBottomRight)

    myBottomLeft = theCandidates[0]
    mySortedCandidates.append(myBottomLeft)  # the only one remaining
    theCandidates.remove(myBottomLeft)

    return mySortedCandidates

#####################################################3
# End of georef helpers
#####################################################3


def runconcrete(func):
    """
    This decorator calls the method in the concrete subclass
    and raise an exception if the method is found only in a base
    abstract class (e.g. GenericProduct or GenericSensorProduct)
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        mySet = (
            set(self.getConcreteInstance().__class__.__mro__)
            .difference([self.__class__])
        )
        myProductClassList = [d for d in mySet if (
            func.__name__ in d.__dict__ and getattr(d, 'concrete', False)
        )]

        #check if there is at least one concrete Product class
        if len(myProductClassList) > 0:
            return getattr(
                self.getConcreteInstance(), func.__name__)(*args, **kwargs)

        raise NotImplementedError()
    return wrapper


class GenericProduct(models.Model):

    """
    A generic model (following R-5.1-160 of DIMS system architecture document).

    @NOTE: this is not an abstract base class since we are using django
    multi-table inheritance.

    See http://docs.djangoproject.com/en/dev/topics/db/models/#id7

    see: signals, to set defaults product_acquisition_start
    """

    product_date = models.DateTimeField(db_index=True)
    processing_level = models.ForeignKey('dictionaries.ProcessingLevel')
    owner = models.ForeignKey(Institution)
    license = models.ForeignKey(License)
    spatial_coverage = models.PolygonField(
        srid=4326, help_text='Image footprint')
    projection = models.ForeignKey(Projection)
    quality = models.ForeignKey(
        Quality,
        help_text=(
            'A quality assessment describing the amount of dropouts etc.'
            'and how usable the entire scene is.'))
    creating_software = models.ForeignKey(
        CreatingSoftware,
        null=False, blank=False)
    original_product_id = models.CharField(
        help_text='Original id assigned to the product by the vendor/operator',
        max_length=255, null=True, blank=True)
    unique_product_id = models.CharField(
        help_text='SAC Formatted product ID',
        max_length=255, db_index=True, unique=True)
    product_revision = models.CharField(
        max_length=255, null=True, blank=True)
    local_storage_path = models.CharField(
        help_text=(
            'Location on local storage if this product is offered for '
            'immediate download.'),
        max_length=255, null=True, blank=True)
    metadata = models.TextField(
        help_text=(
            'An xml document describing all known metadata for this product.'))
    remote_thumbnail_url = models.TextField(
        max_length=255, null=True, blank=True, help_text=(
            'Location on a remote server where this product\'s thumbnail '
            'resides. The value in this field will be nulled when a local '
            'copy is made of the thumbnail.'))

    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract) this flag is also used in admin back-end to get the list of
    # classes for OrderNotificationRecipients
    concrete = False

    objects = models.GeoManager()

    class Meta:
        """
        This is not an abstract base class although you should avoid dealing
        directly with it.

        See http://docs.djangoproject.com/en/dev/topics/db/models/#id7
        """
        app_label = 'catalogue'
        abstract = False
        ordering = ('product_date',)
        #db_table = 'sample_genericproduct'

    def __unicode__(self):
        return u'{}'.format(self.unique_product_id)

    @runconcrete
    def getAbstract(self):
        """
        Returns a description for this product
        """
        pass

    @runconcrete
    def getMetadataDict(self):
        """
        Returns a dictionary of metadata values to feed getXML
        """
        pass

    def getXML(self, xml_template=CATALOGUE_ISO_METADATA_XML_TEMPLATE):
        """
        Returns ISOMetadata.xml XML as a string
        """
        myDict = self.getMetadataDict()
        return dimsWriter.getXML(myDict, xml_template)

    @runconcrete
    def thumbnailDirectory(self):
        """
        Returns the path (relative to whatever parent dir it is in) for the
        thumb for this file following the scheme <Sensor>/<YYYY>/<MM>/<DD>/
        The thumb itself will exist under this dir as <product_id>.jpg
        """
        pass

    def thumbnail(self, theSize):
        """
        Return a thumbnail for this product of size "small" - 16x16, "medium" -
        200x200 or "large" - 400x400

        If a cached copy of the resampled thumb exists, that will be returned
        directly

        @param a string "small","medium" or "large" - defaults to small

        @return a PIL image object.
        """
        if theSize not in ['medium', 'large']:
            theSize = 'small'

        mySize = 16
        if theSize == 'medium':
            mySize = 200
        elif theSize == 'large':
            mySize = 400

        logger.info('showThumb : id ' + self.product_id)
        myImageFile = os.path.join(
            self.thumbnailDirectory(), self.product_id + '.jpg')
        myFileName = str(settings.THUMBS_ROOT) + '/' + myImageFile

        myThumbDir = os.path.join(
            settings.THUMBS_ROOT, self.thumbnailDirectory())
        # Paths for cache of scaled down thumbs (to reduce processing load)
        myCacheThumbDir = os.path.join(
            settings.THUMBS_ROOT, 'cache', theSize, self.thumbnailDirectory())
        myCacheImage = os.path.join(myCacheThumbDir, self.product_id + '.jpg')
        #
        # Check if there is a scaled down version already cached and just
        # return that if there is
        #
        if os.path.isfile(myCacheImage):
            myImage = Image.open(myCacheImage)
            return (myImage)

        #
        # Cached minified thumb not available so lets make it!
        #

        # Hack to automatically fetch spot or other non local thumbs from their
        # catalogue and store them locally
        if self.remote_thumbnail_url and not os.path.exists(myFileName):
            if not os.path.isdir(myThumbDir):
                logger.debug('Creating dir: %s' % myThumbDir)
                try:
                    os.makedirs(myThumbDir)
                except OSError:
                    logger.debug('Failed to make output directory...quitting')
                    return 'Failed to make output dir.'
            logger.debug('Fetching image: %s' % self.remote_thumbnail_url)
            myOpener = urllib2.build_opener()
            myImagePage = myOpener.open(self.remote_thumbnail_url)
            myImage = myImagePage.read()
            logger.debug('Image fetched, saving as %s' % myImageFile)
            myWriter = open(os.path.join(
                settings.THUMBS_ROOT, myImageFile), 'wb')
            myWriter.write(myImage)
            myWriter.close()
            self.remote_thumbnail_url = ""
            self.save()

        # Specify background colour, should be the same as div background
        myBackgroundColour = (255, 255, 255)
        myAngle = 0
        myShadowFlag = False
        logger.info('Creating thumbnail of : ' + myFileName)
        logger.info('Thumbnail path:   ' + str(settings.THUMBS_ROOT))

        if not os.path.isfile(myFileName):
            #file does not exist so show an error icon
            #return HttpResponse("%s not found" % myFileName)
            myFileName = os.path.join(
                settings.ABS_PATH('core', 'base_static'), 'images',
                'block_16.png')
            myImage = Image.open(myFileName)
            return (myImage)

        try:
            myImage = Image.open(myFileName)
        except:
            #file is not valid for some reason so show an error icon
            myFileName = os.path.join(
                settings.ABS_PATH('core', 'base_static'), 'images',
                'block_16.png')
            myImage = Image.open(myFileName)
            return (myImage)

        if len(myImage.getbands()) < 3:
            myImage = ImageOps.expand(myImage, border=5, fill=(255))
        else:
            myImage = ImageOps.expand(myImage, border=5, fill=(255, 255, 255))
        myBackground = None
        if myShadowFlag:
            myImage = self.dropShadow(
                myImage.convert('RGBA')).rotate(myAngle, expand=1)
            myBackground = Image.new('RGBA', myImage.size, myBackgroundColour)
            myBackground.paste(myImage, (0, 0), myImage)
        else:
            myBackground = Image.new('RGBA', myImage.size, myBackgroundColour)
            myBackground.paste(myImage, (0, 0))
        myBackground.thumbnail((mySize, mySize), Image.ANTIALIAS)

        # Now cache the scaled thumb for faster access next time...
        if not os.path.isdir(myCacheThumbDir):
            logger.debug('Creating dir: %s' % myCacheThumbDir)
            try:
                os.makedirs(myCacheThumbDir)
            except OSError:
                logger.debug('Failed to make output directory...quitting')
                return 'Failed to make output dir'
        logger.debug('Caching image : %s' % myCacheImage)
        myBackground.save(myCacheImage)
        return (myBackground)

    def dropShadow(
            theImage,
            myOffset=(5, 5),
            theBackground=(49, 89, 125),
            theShadow=(0, 0, 0, 100),
            theBorder = 8,
            theIterations = 5
    ):

        # Create the myBackgrounddrop image -- a box in the theBackground
        # colour with a theShadow on it.
        myTotalWidth = theImage.size[0] + abs(myOffset[0]) + 2 * theBorder
        myTotalHeight = theImage.size[1] + abs(myOffset[1]) + 2 * theBorder
        myBackground = Image.new(
            theImage.mode, (myTotalWidth, myTotalHeight), theBackground)

        # Place the theShadow, taking into account the myOffset from the image
        theShadowLeft = theBorder + max(myOffset[0], 0)
        theShadowTop = theBorder + max(myOffset[1], 0)
        myBackground.paste(
            theShadow, [
                theShadowLeft, theShadowTop, theShadowLeft + theImage.size[0],
                theShadowTop + theImage.size[1]])

        # Apply the filter to blur the edges of the theShadow.  Since a small
        # kernel is used, the filter must be applied repeatedly to get a decent
        # blur.
        n = 0
        while n < theIterations:
            myBackground = myBackground.filter(ImageFilter.BLUR)
            n += 1

        # Paste the input image onto the theShadow myBackgrounddrop
        myImageLeft = theBorder - min(myOffset[0], 0)
        myImageTop = theBorder - min(myOffset[1], 0)
        myBackground.paste(theImage, (myImageLeft, myImageTop))

        return myBackground

    def georeferencedThumbnail(self, theForceFlag=False):
        """
        Return the full path to the georeferenced thumb. Will actually do the
        georeferencing of the thumb if needed.

        return thumb full path, e.g.
        myJpg = product.georeferencing()

        To get the world file, simply add a .wld extention to the return var
        We dont return it explicitly as we can only return a single param
        if we want to use this method in template.
        Be careful of using the force flag - some of the thumbs (e.g. newer
        imports from acs) are already georeferenced natively and referencing
        them again will give them an additional rotation.
        """
        myInputImageFile = os.path.join(
            settings.THUMBS_ROOT, self.thumbnailDirectory(),
            self.product_id + '.jpg')
        try:
            myImage = Image.open(myInputImageFile)
            # We need to know the pixel dimensions of the segment so that we
            # can create GCP's
        except:
            logger.info('File not found %s' % myInputImageFile)
            return 'no file'
        myTempTifFile = os.path.join('/tmp/', self.product_id + '.tif')
        myTempReffedTifFile = os.path.join(
            '/tmp/', self.product_id + 'reffed.tif')
        myJpgFile = os.path.join(
            settings.THUMBS_ROOT, self.thumbnailDirectory(),
            self.product_id + '-reffed.jpg')

        myLogFile = file(os.path.join(
            settings.THUMBS_ROOT, self.thumbnailDirectory(),
            self.product_id + '-reffed.log'), 'w')
        if os.path.exists(myJpgFile) and not theForceFlag:
            return myJpgFile
            # Get the minima, maxima - used to test if we are on the edge
        myExtents = self.spatial_coverage.extent
        #print "Envelope: %s %s" % (len(myExtents), str(myExtents))
        # There should only be 4 vertices touching the edges of the
        # bounding box of the shape. If we assume that the top right
        # corner of the poly is on the right edge of the bbox, the
        # bottom right vertex is on the bottom edge and so on
        # we can narrow things down to just the leftside two and rightside
        # two vertices. Thereafter, determining which is 'top' and which is
        # bottom is a simple case of comparing the Y values in each grouping.
        #
        # Note the above logic makes some assumptions about the oreintation of
        # the swath which may not hold true for every sensor.
        #

        myImageXDim = myImage.size[0]
        myImageYDim = myImage.size[1]
        myCandidates = []
        try:
            #should only be a single arc in our case!
            for myArc in self.spatial_coverage.coords:
                for myCoord in myArc[:-1]:
                    if coordIsOnBounds(myCoord, myExtents):
                        myCandidates.append(myCoord)
        except:
            raise
            # print "Candidates Before: %s %s " % (
        #    len(myCandidates), str(myCandidates))
        myCentroid = self.spatial_coverage.centroid
        try:
            myCandidates = sortCandidates(myCandidates, myExtents, myCentroid)
        except:
            raise
            # print "Candidates After: %s %s " % (
        #    len(myCandidates), str(myCandidates))
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
                myInputImageFile,
                myTempTifFile))
        os.system(myString)
        myLogFile.write(myString + "\n")
        # now gdalwarp the file onto itself so that the gcps are used to
        # georeference the file
        myString = 'gdalwarp %s %s' % (myTempTifFile, myTempReffedTifFile)
        myLogFile.write(myString + "\n")
        os.system(myString)
        # TODO : nicer way to call gdal e.g.
        #subprocess.check_call(["gdal_translate", "-q", "-co", "worldfile=on",
        #                       "-of", "JPEG", downloaded_thumb, jpeg_thumb])
        # Now convert the tif to a jpg
        myString = 'gdal_translate -of JPEG -co WORLDFILE=YES %s %s' % (
            myTempReffedTifFile, myJpgFile)
        myLogFile.write(myString + "\n")
        os.system(myString)
        myLogFile.close()
        # Clean away the tiff and copy the referenced jpg over to the thumb dir
        os.remove(myTempTifFile)
        os.remove(myTempReffedTifFile)
        #print "Image X size: %s" % myImageXDim
        #print "Image Y size: %s" % myImageYDim
        #print "Top left X: %s, Y:%s" %(myTL[0],myTL[1])
        #print "Top right X: %s, Y:%s" %(myTR[0],myTR[1])
        #print "Bottom left X: %s, Y:%s" %(myBL[0],myBL[1])
        #print "Bottom right X: %s, Y:%s" %(myBR[0],myBR[1])
        return myJpgFile

    @runconcrete
    def productDirectory(self):
        """
        Returns the path (relative to whatever parent dir it is in) for the
        image itself following the scheme
            <Sensor>/<processinglevel>/<YYYY>/<MM>/<DD>/
        The image itself will exist under this dir as <product_id>.tif.bz2

        @note the filename itself is excluded, only the directory path is
            returned
        """
        # Checks method is in concrete class
        pass

    def productUrl(self):
        """Returns a path to the actual imagery data as a url. You need to have
        apache set up so share this directory. If no file is encountered at the
        computed path,

        None will be returned"""
        myUrl = (
            settings.IMAGERY_URL_ROOT + self.productDirectory() + '/' +
            self.product_id + '.tif.bz2')
        myPath = os.path.join(
            settings.IMAGERY_ROOT, self.productDirectory(),
            self.product_id + '.tif.bz2')
        if os.path.isfile(myPath):
            return myUrl
        else:
            return None

    def rawProductUrl(self):
        """
        Returns a path to the actual RAW imagery data as a url. So if you have
        a level 1Ab product and want to get to its original L1Aa product this
        method will give it to you. You need to have apache set up so share
        this directory. If no file is encountered at the computed path, None
        will be returned.

        @note this method should be deprecated in future since each derivative
        product should have its own record.
        """
        myPath = os.path.join(
            settings.IMAGERY_ROOT, self.productDirectory(),
            self.product_id + '.tar.bz2')
        myLevel = self.processing_level.abbreviation
        myLevel = myLevel.replace('L', '')
        # since we want *RAW* image in this method set processing level to 1Aa
        myPath = myPath.replace(myLevel, '1Aa')
        myUrl = (
            settings.IMAGERY_URL_ROOT + self.productDirectory() + '/' +
            self.product_id + '.tar.bz2')
        myUrl = myUrl.replace(myLevel, '1Aa')
        # In some cases products may not be in bzipped tarballs so check if
        # that is present if the bz2 on its own isn't present
        if not os.path.isfile(myPath):
            myPath = myPath.replace('.tar.bz2', '.bz2')
            myUrl = myUrl.replace('.tar.bz2', '.bz2')
        logger.info('Raw Image Path: %s' % myPath)
        logger.info('Raw Image Url: %s' % myUrl)
        if os.path.isfile(myPath):
            return myUrl
        else:
            return None

    def getConcreteProduct(self):
        """
        Downcast a product to its subtype using technique described here:
        http://docs.djangoproject.com/en/dev/topics/db/models/#id7

        @return Object, String :

            Object : A concrete subtype of GenericProduct e.g an OpticalProduct
                or a RadarProduct etc. None returned if the object could not be
                found.

            String : e.g. "Optical", "Radar" etc representing what type of
                object was found.
        """
        try:
            return (
                self.genericimageryproduct.genericsensorproduct.opticalproduct,
                "Optical")
        except:
            pass
        try:
            return (
                self.genericimageryproduct.genericsensorproduct.radarproduct,
                "Radar")
        except:
            pass
        try:
            return (self.genericimageryproduct, "Imagery")
        except:
            pass
        try:
            return (self.geospatialproduct.ordinalproduct, "Ordinal")
        except:
            pass
        try:
            return (self.geospatialproduct.continuousproduct, "Continuous")
        except:
            pass

        # ABP: raise exception instead of returning None, "Error - product not
        # found"
        raise ObjectDoesNotExist()

    def getConcreteInstance(self):
        """
        Returns the concrete product instance
        """
        return self.getConcreteProduct()[0]

    @runconcrete
    def setSacProductId(self):
        """A sac product id adheres to the following format:

        SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL

        """
        pass

    @runconcrete
    def productIdReverse(self, force=False):
        """
        Parse a product_id and populates instance fields
        If force is set, the procedure will try to create
        missing bits
        """
        pass

    def tidySacId(self):
        """Return a tidy version of the SAC ID for use on web pages etc.

           Normal: S5-_HRG_J--_CAM2_0118-_00_0418-_00_090403_085811_L1A-_ORBIT-

           Tidy:   S5 HRG J CAM2 0118 00 0418  00 090403 085811

           This is so that we can wrap the id nicely in small spaces etc."""
        myTokens = self.product_id.split("_")
        myUsedTokens = myTokens[0:9]
        myNewString = " ".join(myUsedTokens).replace("-", "")
        return myNewString

    def getUTMZones(self, theBuffer=0):
        """ return UTM zones which overlap this product
        theBuffer - specifies how many adjecent zones to return"""

        return set(
            utmZoneFromLatLon(
                *self.spatial_coverage.extent[:2], theBuffer=theBuffer)
            + utmZoneFromLatLon(
                *self.spatial_coverage.extent[2:], theBuffer=theBuffer))

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/genericProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})

    @property
    def product_id(self):
        """
        Simple product_id property, helper with unique_product_id migration
        """
        return self.unique_product_id


###############################################################################

class GenericImageryProduct(GenericProduct):
    """
    Generic Imagery product, it is always a composite aggregated products
    see: signals, to set spatial_resolution defaults and average
    """
    spatial_resolution = models.FloatField(
        help_text='Spatial resolution in m')
    spatial_resolution_x = models.FloatField(
        help_text='Spatial resolution in m (x direction)')
    spatial_resolution_y = models.FloatField(
        help_text='Spatial resolution in m (y direction)')
    radiometric_resolution = models.IntegerField(
        help_text=(
            'Bit depth of image e.g. 16bit Note that this is for the '
            'delivered image and not necessarily the same as bit depth at '
            'acquisition.'))
    band_count = models.IntegerField(
        help_text='Number of spectral bands in product')

    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract)
    concrete = True
    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'
        #db_table = 'sample_genericimageryproduct'

    def getAbstract(self):
        """
        Returns the abstract for this product
        TODO: implement
        """
        return ''

    def getMetadataDict(self):
        """
        Returns metadata dictionary
        """
        metadata = dict(
            product_date=self.product_date.isoformat(),
            file_identifier=self.product_id,
            vertical_cs=self.projection.name,
            processing_level_code=self.processing_level.abbreviation,
            md_data_identification=unicode(self.product_profile),
            md_product_date=self.product_date.isoformat(),
            md_abstract=self.getAbstract(),
            bbox_west=self.spatial_coverage.extent[0],
            bbox_east=self.spatial_coverage.extent[2],
            bbox_north=self.spatial_coverage.extent[3],
            bbox_south=self.spatial_coverage.extent[1],
            image_quality_code=self.quality.name,
            spatial_coverage=' '.join(
                ["%s,%s" % _p for _p in self.spatial_coverage.tuple[0]]),
            institution_name=self.owner.name,
            institution_address=self.owner.address1,
            institution_city=self.owner.address2,
            institution_region='',
            institution_postcode=self.owner.post_code,
            institution_country=self.owner.address3,)
        return metadata

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/genericImageryProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})


###############################################################################

class GenericSensorProduct(GenericImageryProduct):
    """
    Multitable inheritance class to hold common fields for satellite imagery
    """
    # e.g. CAM1, BUMP, etc - this must die!
    product_acquisition_start = models.DateTimeField(db_index=True)
    product_acquisition_end = models.DateTimeField(
        null=True, blank=True, db_index=True)
    geometric_accuracy_mean = models.FloatField(
        null=True, blank=True, db_index=True)
    geometric_accuracy_1sigma = models.FloatField(null=True, blank=True)
    geometric_accuracy_2sigma = models.FloatField(null=True, blank=True)
    radiometric_signal_to_noise_ratio = models.FloatField(
        null=True, blank=True)
    radiometric_percentage_error = models.FloatField(null=True, blank=True)
    spectral_accuracy = models.FloatField(
        help_text='Wavelength Deviation', null=True, blank=True)
    orbit_number = models.IntegerField(null=True, blank=True)
    # K Path Orbit
    path = models.IntegerField(null=True, blank=True, db_index=True)
    path_offset = models.IntegerField(null=True, blank=True, db_index=True)
    # J Frame Row
    row = models.IntegerField(null=True, blank=True)
    row_offset = models.IntegerField(null=True, blank=True)
    offline_storage_medium_id = models.CharField(
        max_length=12, null=True, blank=True,
        help_text=(
            'Identifier for the offline tape or other medium on which this '
            'scene is stored'))
    online_storage_medium_id = models.CharField(
        max_length=36, null=True, blank=True, help_text=(
            'DIMS Product Id as defined by Werum e.g. S5_G2_J_MX_200902160841'
            '252_FG_001822'))

    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract)
    concrete = False
    objects = models.GeoManager()

    class Meta:
        """
        This is not an abstract base class although you should avoid dealing
        directly with it

        see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
        """
        app_label = 'catalogue'
        abstract = False
        #db_table = 'sample_genericsensorproduct'

    def _productDirectory(self):
        """
        Returns the path (relative to whatever parent dir it is in) for the
        product / image itself following the scheme
            <Satellite>/<processinglevel>/<YYYY>/<MM>/<DD>/
        The image itself will exist under this dir as <product_id>.tif.bz2

        @note the filename itself is excluded, only the directory path is
            returned
        """
        myPath = os.path.join(
            self.product_profile.satellite_instrument
            .satellite_instrument_group.satellite.abbreviation,
            str(self.processing_level.abbreviation),
            str(self.product_acquisition_start.year),
            str(self.product_acquisition_start.month),
            str(self.product_acquisition_start.day))
        logger.debug('Product directory path: %s', myPath)
        return myPath

    def _thumbnailDirectory(self):
        """
        Returns the path (relative to whatever parent dir it is in defined by
        THUMBS_ROOT) for the thumb for this file following the scheme
            <Satellite>/<YYYY>/<MM>/<DD>/
        The thumb itself will exist under this dir as <product_id>.jpg

        @note the filename itself is excluded, only the directory path is
        returned
        """
        myPath = os.path.join(
            self.product_profile.satellite_instrument.
            satellite_instrument_group.satellite.abbreviation,
            str(self.product_acquisition_start.year),
            str(self.product_acquisition_start.month),
            str(self.product_acquisition_start.day))
        logger.debug('Thumbnail directory path: %s', myPath)
        return myPath

    def refileProductAssets(
            self, theOldId, theOldImageryPath, theOldThumbPath):

        """
        A helper for when a product id changes so that its assets (thumbs,
        product data etc) can be moved to the correct place on the storage
        system to match the new product's designation. There are a few things
        we need to move:
            - the raw imagery (which may be a bz2 or tar.bz2 archive) if it
                exists
            - the processed imagery (bz2 archive) currently assumed to be a
                tiff
            - the thumbnail if present
            - the georeferenced thumb if present
            - cached thumbnail minatures if present
            """
        #
        # Rename the thumb from the old name to the new name (if present):
        #
        if theOldId is None or theOldId == '':
            # This is a new record
            return
        if theOldId == self.product_id:
            #it already has the correct name
            return

        myNewImageryPath = os.path.join(
            # /opt/sac_catalogue/sac_live/imagery_master_copy
            settings.IMAGERY_ROOT,
            # ZA2/1Aa/2009/12/11
            self.productDirectory(),
            # ZA2_MSS_R3B_FMC4_098W_56_020N_01_091211_154127_L1Aa_ORBIT-
            self.product_id + '.tif.bz2')

        myOldImageryPath = os.path.join(
            # /opt/sac_catalogue/sac_live/imagery_master_copy
            settings.IMAGERY_ROOT,
            # ZA2/1Ab/2009/12/11
            theOldImageryPath,
            # ZA2_MSS_R3B_FMC4_098W_56_020N_01_091211_154127_L1Ab_ORBIT-
            theOldId + '.tif.bz2')
        # In some cases the imagery may be in a tar archive (for multiple
        # files) rather than a simple bz2 so we also try to find a tar file.
        if not os.path.isfile(myOldImageryPath):
            myNewImageryPath = myNewImageryPath.replace('.tar.bz2', '.bz2')
            myOldImageryPath = myOldImageryPath.replace('.tar.bz2', '.bz2')

        myImageryOutputPath = os.path.join(
            settings.IMAGERY_ROOT, self.productDirectory())
        myThumbOutputPath = os.path.join(
            settings.THUMBS_ROOT, self.thumbnailDirectory())

        # Create the imagery destination dir if it does not exist.
        if not os.path.isdir(myImageryOutputPath):
            try:
                os.makedirs(myImageryOutputPath)
            except OSError:
                logger.debug(
                    'Failed to make output directory (%s) ...quitting' % (
                        myImageryOutputPath,))
                return 'False'

        # Create the thumbnails destination dir if it does not exist.
        if not os.path.isdir(myThumbOutputPath):
            try:
                os.makedirs(myThumbOutputPath)
            except OSError:
                logger.debug(
                    'Failed to make output directory (%s) ...quitting' % (
                        myThumbOutputPath,))
                return 'False'

        # now everything is ready do the actual renaming
        try:
            myNewReffedPath = os.path.join(
                myThumbOutputPath,
                self.product_id + '-reffed.jpg')
            myOldReffedPath = os.path.join(
                theOldThumbPath,
                theOldId + '-reffed.jpg')

            myNewJpgPath = os.path.join(myThumbOutputPath,
                                        self.product_id + '.jpg')
            myOldJpgPath = os.path.join(theOldThumbPath,
                                        theOldId + '.jpg')

            myNewWorldPath = os.path.join(myThumbOutputPath,
                                          self.product_id + '.wld')
            myOldWorldPath = os.path.join(theOldThumbPath,
                                          theOldId + '.wld')

            if os.path.exists(myOldJpgPath):
                shutil.move(myOldJpgPath, myNewJpgPath)

            if os.path.exists(myOldReffedPath):
                # If the reffed jpg is a symlink, replace it with a new one
                if os.path.islink(myOldReffedPath):
                    os.remove(myOldReffedPath)
                    os.symlink(myNewJpgPath, myNewReffedPath)
                else:
                    # Otherwise move the file.
                    shutil.move(myOldReffedPath, myNewReffedPath)

            if os.path.exists(myOldWorldPath):
                shutil.move(myOldWorldPath, myNewWorldPath)

            # Now move the imagery if it exists
            if os.path.exists(myOldImageryPath):
                shutil.move(myOldImageryPath, myNewImageryPath)

        except:
            logger.debug("Failed to move some or all of the assets")

        return

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/genericSensorProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})

###############################################################################


class OpticalProduct(GenericSensorProduct):
    """
    We are using multitable inheritance so you can do this to get this class
    instance from an GenericProduct :

    myOpticalProduct = GenericProduct.objects.get(id=1).opticalproduct

    See http://docs.djangoproject.com/en/dev/topics/db/models/#id7 for more
    info.
    """
    ##Descriptors for optical products
    # new dicts
    product_profile = models.ForeignKey(
        'dictionaries.OpticalProductProfile'
    )
    #TODO: all cloud cover values should be normalized to percentages
    # see http://tracker.sansa.org.za/issues/475
    cloud_cover = models.IntegerField(
        null=True, blank=True, max_length=3,
        help_text=(
            'The maximum cloud cover when searching for images. Note that not '
            'all sensors support cloud cover filtering. Range 0-100%'))
    sensor_inclination_angle = models.FloatField(
        null=True, blank=True,
        help_text='Orientation of the vehicle on which the sensor is mounted')
    sensor_viewing_angle = models.FloatField(
        null=True, blank=True,
        help_text='Angle of acquisition for the image')
    gain_name = models.CharField(max_length=200, null=True, blank=True)
    gain_value_per_channel = models.CharField(
        max_length=200, null=True, blank=True,
        help_text='Comma separated list of gain values')
    gain_change_per_channel = models.CharField(
        max_length=200, null=True, blank=True,
        help_text='Comma separated list of gain change values')
    bias_per_channel = models.CharField(
        max_length=200, null=True, blank=True,
        help_text='Comma separated list of bias values')
    solar_zenith_angle = models.FloatField(null=True, blank=True)
    solar_azimuth_angle = models.FloatField(null=True, blank=True)
    earth_sun_distance = models.FloatField(null=True, blank=True)

    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract)
    concrete = True
    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'
        #db_table = 'sample_opticalproduct'

    def getMetadataDict(self):
        """
        Returns metadata dictionary
        """
        metadata = dict(
            product_date=self.product_date.isoformat(),
            file_identifier=self.product_id,
            vertical_cs=self.projection.name,
            processing_level_code=self.processing_level.abbreviation,
            cloud_cover_percentage=self.cloud_cover,  # OpticalProduct only
            md_data_identification=unicode(self.product_profile),
            md_product_date=self.product_date.isoformat(),
            md_abstract=self.getAbstract(),
            bbox_west=self.spatial_coverage.extent[0],
            bbox_east=self.spatial_coverage.extent[2],
            bbox_north=self.spatial_coverage.extent[3],
            bbox_south=self.spatial_coverage.extent[1],
            image_quality_code=self.quality.name,
            spatial_coverage=' '.join(
                ['%s,%s' % _p for _p in self.spatial_coverage.tuple[0]]),
            institution_name=self.owner.name,
            institution_address=self.owner.address1,
            institution_city=self.owner.address2,
            institution_region='',
            institution_postcode=self.owner.post_code,
            institution_country=self.owner.address3,)
        return metadata

    def productDirectory(self):
        """
        A wrapper to run concrete from GenericSensorProduct
        @note the filename itself is excluded, only the directory path is
            returned
        """
        return self._productDirectory()

    def thumbnailDirectory(self):
        """
        A wrapper to run concrete from GenericSensorProduct
        """
        return self._thumbnailDirectory()

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">"""

        return render_to_string(
            'productTypes/opticalProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})


###############################################################################

#TODO use lookup tables rather?

class RadarProduct(GenericSensorProduct):
    """
    We are using multi-table inheritance so you can do this to get this class
    instance from an GenericProduct :
    myRadarProduct = GenericProduct.objects.get(id=1).radarproduct

    See http://docs.djangoproject.com/en/dev/topics/db/models/#id7 for more
    info.
    """
    # Note for radar products row and path will be computed as
    # the Degrees (2 digits) Minutes (2 Digits) and the offset will be used to
    # store seconds (2 digits)

    LOOK_DIRECTION_CHOICES = (('L', 'Left'), ('R', 'Right'))
    RECEIVE_CONFIGURATION_CHOICES = (('V', 'Vertical'), ('H', 'Horizontal'))
    POLARISING_MODE_CHOICES = (
        ('S', 'Single Pole'), ('D', 'Dual Pole'), ('Q', 'Quad Pole'))
    ORBIT_DIRECTION_CHOICES = (('A', 'Ascending'), ('D', 'Descending'))

    # new dicts
    product_profile = models.ForeignKey(
        'dictionaries.RadarProductProfile'
    )
    imaging_mode = models.CharField(max_length=200, null=True, blank=True)
    look_direction = models.CharField(
        max_length=1, choices=LOOK_DIRECTION_CHOICES, null=True, blank=True)
    antenna_receive_configuration = models.CharField(
        max_length=1, choices=RECEIVE_CONFIGURATION_CHOICES,
        null=True, blank=True)
    polarising_mode = models.CharField(
        max_length=1, choices=POLARISING_MODE_CHOICES, null=True, blank=True)
    polarising_list = models.CharField(
        max_length=200, null=True, blank=True,
        help_text=(
            'Comma separated list of V/H/VV/VH/HV/HH (vertical and horizontal '
            'polarisation.)'))
    slant_range_resolution = models.FloatField(null=True, blank=True)
    azimuth_range_resolution = models.FloatField(null=True, blank=True)
    orbit_direction = models.CharField(
        max_length=1, choices=ORBIT_DIRECTION_CHOICES, null=True, blank=True)
    calibration = models.CharField(max_length=255, null=True, blank=True)
    incidence_angle = models.FloatField(null=True, blank=True)

    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract)
    concrete = True
    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'
        #db_table = 'sample_radarproduct'

    def productDirectory(self):
        """
        A wrapper to run concrete from GenericSensorProduct
        @note the filename itself is excluded, only the directory path is
            returned
        """
        return self._productDirectory()

    def thumbnailDirectory(self):
        """
        A wrapper to run concrete from GenericSensorProduct
        """
        return self._thumbnailDirectory()

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/radarProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})
    ###########################################################################


class GeospatialProduct(GenericProduct):
    """
    Geospatial product, does not have sensors information. Geospatial products
    may be rasters (that were derived from one or more satellite or other
    rasters) or vectors.
    """
    GEOSPATIAL_GEOMETRY_TYPE_CHOICES = (
        ('RA', 'Raster'), ('VP', 'Vector - Points'), ('VL', 'Vector - Lines'),
        ('VA', 'Vector - Areas / Polygons'))
    name = models.CharField(
        max_length=255, null=False, blank=False,
        help_text='A descriptive name for this dataset')
    description = models.TextField(
        null=True, blank=True, help_text='Description of the product')
    processing_notes = models.TextField(
        null=True, blank=True,
        help_text='Description of how the product was created.')
    equivalent_scale = models.IntegerField(
        null=True, blank=True, default=1000000,
        help_text=(
            'The fractional part at the ideal maximum scale for this dataset. '
            'For example enter "50000" if it should not be used at scales '
            'larger that 1:50 000'),)
    data_type = models.CharField(
        max_length=2, choices=GEOSPATIAL_GEOMETRY_TYPE_CHOICES, null=True,
        blank=True, help_text='Is this a vector or raster dataset?')
    temporal_extent_start = models.DateTimeField(
        db_index=True,
        help_text=(
            'The start of the timespan covered by this dataset. If left blank '
            'will default to time of accession.'))
    temporal_extent_end = models.DateTimeField(
        null=True, blank=True, db_index=True,
        help_text=(
            'The start of the timespan covered by this dataset. If left blank'
            'will default to start date.'))
    place_type = models.ForeignKey(
        PlaceType,
        help_text=(
            'Select the type of geographic region covered by this dataset'))
    place = models.ForeignKey(
        Place,
        help_text='Nearest place, town, country region etc. to this product')
    primary_topic = models.ForeignKey(
        Topic,
        help_text=(
            'Select the most appopriate topic for this dataset. You can add '
            'additional keywords in the tags box.'))  # e.g. Landuse etc
    #
    # elpaso to implement tagging support please....
    #
    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract)
    concrete = False
    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/geospatialProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})
    ###########################################################################


class OrdinalProduct(GenericProduct):
    """
    Ordinal product, does not have sensors information. Ordinal products are
    class based products e.g. roads, landuse, etc.
    Products may be rasters (that were derived from one or more satellite or
    other rasters) or vectors.
    """
    class_count = models.IntegerField(
        help_text='Number of spectral bands in product')
    confusion_matrix = models.CommaSeparatedIntegerField(
        max_length=80, null=True, unique=False, blank=True,
        help_text=(
            'Confusion matrix in the format: true positive, false negative, '
            'false positive,true negative'))
    kappa_score = models.FloatField(
        null=True, blank=True,
        help_text=(
            'Enter a value between 0 and 1 representing the kappa score.'))

    # We need a flag to tell if this Product class can have instances
    # (if it is not abstract)
    concrete = True
    objects = models.GeoManager()

    class Meta:
        # Specifies which database this model ORM goes to
        app_label = 'catalogue'

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/ordinalProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})
    ###########################################################################


class ContinuousProduct(GenericProduct):
    """
    Continuousproduct, does not have sensors information. These products
    represent continuous data e.g. elevation, rainfall etc.

    Products may be rasters (that were derived from measurements, one or more
    satellite or other rasters) or vectors.
    """
    range_min = models.FloatField(
        null=False, blank=False,
        help_text=(
            'The minimum value in the range of values represented in this '
            'dataset.'))
    range_max = models.FloatField(
        null=False, blank=False,
        help_text=(
            'The maximum value in the range of values represented in this'
            'dataset.'))
    unit = models.ForeignKey(
        Unit,
        help_text='Units for the values represented in this dataset.')
    # We need a flag to tell if this Product class can have instances (if it is
    # not abstract)
    concrete = True
    objects = models.GeoManager()

    class Meta:
        app_label = 'catalogue'

    def toHtml(self, theImageIsLocal=False):
        """
        Return an html snippet that describes the properties of this product.
        If theImageIsLocal flag is true, not url path will be used (i.e. it
        will be rendered as <img src="foo.jpg">
        """
        return render_to_string(
            'productTypes/continuousProduct.html', {
                'myObject': self, 'myImageIsLocalFlag': theImageIsLocal})
