"""
SANSA-EO Catalogue - Other application views

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
__date__ = '17/08/2012'
__copyright__ = 'South African National Space Agency'

# PIL and os needed for making small thumbs
import os

# python logging support to django logging middleware
import logging

# for get feature info
import urllib.request, urllib.error, urllib.parse

# for error logging
import traceback

# Django helpers for forming html pages
from django.contrib.gis.db.models.functions import AsKML
from django.contrib.gis.gdal import OGRGeometry
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.forms.utils import ErrorList
from django.contrib.gis.geos import Point

# Models and forms for our app
from catalogue.models.others import Visit, VisitorReport
from catalogue.models.products import GenericProduct
from catalogue.models.website import Contact, Slider

from catalogue.forms import (
    ClipForm)
from catalogue.render_decorator import RenderWithContext

# SHP and KML readers
from catalogue.featureReaders import (
    getGeometryFromUploadedFile, )

# View Helper classes
from catalogue.views.geoiputils import GeoIpUtils
from catalogue.views.helpers import (
    WEB_LAYERS,
    standardLayers,
    isStrategicPartner)
from catalogue.views.helpers import render_to_kml

from search.models import (
    Search,
    # SearchRecord,
    Clip,
)

logger = logging.getLogger(__name__)


#### VIEW FUNCTIONS ####


def log_visit(request):
    """
    Silently log a visit and return an empty string. The best way to use this
    method is by adding it as a fake css reference at the top of your template
    e.g.: <link rel="stylesheet" href="/visit" type="text/css">
    """
    if settings.USE_GEOIP:
        myGeoIpUtils = GeoIpUtils()
        myIp = myGeoIpUtils.getMyIp(request)
        if myIp:
            myLatLong = myGeoIpUtils.getMyLatLong(request)
            myVisit = Visit()
            try:
                if myLatLong['city']:
                    myVisit.city = myLatLong['city']
                else:
                    myVisit.city = 'Unknown'
            except:
                myVisit.city = 'Unknown'
            try:
                myVisit.country = myLatLong['country_name']
                myVisit.ip_position = Point(
                    myLatLong['longitude'], myLatLong['latitude'])
                myVisit.ip_address = myIp
                # User is optional - we can see anonymous visits as they will
                # have a null user
                if request.user:
                    myVisit.user = request.user
            except:
                return HttpResponse(
                    '/** Error in geoip */', content_type='text/css')
            myVisit.save()
            # If user is logged in, store their IP lat lon to their profile
            try:
                if request.user:
                    myProfile = request.user.get_profile()
                    myProfile.latitude = str(myLatLong['latitude'])
                    myProfile.longitude = str(myLatLong['longitude'])
                    myProfile.save()
            except:
                # user has no profile ...
                return HttpResponse('/** No Profile */', content_type='text/css')
        else:
            logger.info(
                'GEOIP capture failed to retrieve valid position info')
            return HttpResponse(
                '/** No valid position */', content_type='text/css')
    else:
        logger.info('GEOIP capture disabled in settings')
        return HttpResponse(
            '/** Geoip disabled in settings */', content_type='text/css')
    return HttpResponse('', content_type='text/css')


@login_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('map.html')
def whereAmI(request):
    logger.info('whereAmI called...')
    myExtent = '(16,-34, 33, -22)'
    myMessages = []
    myGeoIpUtils = GeoIpUtils()
    myLatLong = myGeoIpUtils.getMyLatLong(request)
    if myLatLong:
        # Above returns something like:
        # {'city': 'Johannesburg', 'region': '06', 'area_code': 0, 'longitude':
        # 28.08329963684082, 'country_code3': 'ZAF',
        # 'latitude': -26.200000762939453,
        # 'postal_code': None, 'dma_code': 0, 'country_code': 'ZA',
        # 'country_name':'South Africa'}
        myHeading = (
            '<h3><a href="#"><i class="icon-globe"></i>&nbsp;'
            'Your Location</a></h3>')
        myMessages.append('Nearest City: ' + str(myLatLong['city']))
        myMessages.append('Country: ' + str(myLatLong['country_name']))
        myMessages.append('Longitude: ' + str(myLatLong['longitude']))
        myMessages.append('Latitude: ' + str(myLatLong['latitude']))
        myIp = myGeoIpUtils.getMyIp(request)
        myMessages.append('IP Address: ' + myIp)
        # Record the visitor details to our db
        myVisit = Visit()
        if myLatLong['city']:
            myVisit.city = myLatLong['city']
        else:
            myVisit.city = 'Unknown'
        myVisit.country = myLatLong['country_name']
        myVisit.ip_position = Point(
            myLatLong['longitude'], myLatLong['latitude'])
        myVisit.ip_address = myIp
        myVisit.save()
        myLayerString = (
                """
           /*
           * Layer style
           */
           // we want opaque external graphics and non-opaque internal graphics
           var myLayerStyle = OpenLayers.Util.extend({},
               OpenLayers.Feature.Vector.style['default']);
           myLayerStyle.fillOpacity = 0.2;
           myLayerStyle.graphicOpacity = 1;
           /*
           * Blue style
           */
           var myBlueStyle = OpenLayers.Util.extend({}, myLayerStyle);
           myBlueStyle.strokeColor = "blue";
           myBlueStyle.fillColor = "blue";
           myBlueStyle.graphicName = "star";
           myBlueStyle.pointRadius = 10;
           myBlueStyle.strokeWidth = 3;
           myBlueStyle.rotation = 45;
           myBlueStyle.strokeLinecap = "butt";
           var myLayer = new OpenLayers.Layer.Vector("Simple Geometry",
               {style: myLayerStyle});
           // create a point feature
           var myPoint = new OpenLayers.Geometry.Point(""" +
                str(myLatLong['longitude']) + "," +
                str(myLatLong['latitude']) + """);
           myPoint = transformPoint( myPoint );
           var myPointFeature = new OpenLayers.Feature.Vector(myPoint,null,
                myBlueStyle);
           myLayer.addFeatures([myPointFeature]);
           //map.setCenter(new OpenLayers.LonLat(point.x, point.y), 5);
                        """)
        myLayerDefinitions = [
            WEB_LAYERS['TMSOverlay'],
            myLayerString]
        myLayersList = "[TMSOverlay,myLayer]"
        return ({
            'myGoogleFlag': 'true',
            'myExtent': myExtent,
            'myMessagesHeading': myHeading,
            'myMessages': myMessages,
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
            'myMessagesFlag': True,
        })

    else:
        myHeading = (
            '<h3><i class="icon-globe"></i>&nbsp;'
            'Your Location</h3>')
        myMessages.append('Sorry, we could not resolve your position.')
        return ({
            'myGoogleFlag': None,
            'myExtent': None,
            'myMessagesHeading': myHeading,
            'myMessages': myMessages,
            'myLayerDefinitions': None,
            'myLayersList': None,
            'myMessagesFlag': True,
        })


@login_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('addPage.html')
def clip(request):
    """Show a spot map of South Africa"""
    myTitle = 'Clip Request'
    myExtent = '(15.256693,-35.325000,33.743307,-21.675000)'
    myHeading = (
        '<h3><a href="#"><img src="/static/images/globe_16.png">&nbsp;'
        '2008 SPOT5 Mosaic</a></h3>')
    myMessages = []
    myMessages.append('<h3>SPOT5 Mosaic, South Africa</h3>')
    myMessages.append(
        'Initial view is NASA Blue Marble Data, zoom in and the SPOT Mosaic '
        'will appear... ')
    myLayerDefinitions = None
    myLayersList = None
    myActiveBaseMap = None
    myProfile = None
    myForm = None

    try:
        myProfile = request.user.get_profile()
    except:
        logger.debug('Profile does not exist')
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        request)
    if request.method == 'POST':
        myForm = ClipForm(request.POST, request.FILES)
        if myForm.is_valid():
            myObject = myForm.save(commit=False)
            myObject.owner = request.user
            myGeometry = None
            try:
                myGeometry = getGeometryFromUploadedFile(
                    request, myForm, 'geometry_file')
                if myGeometry:
                    myObject.geometry = myGeometry
                else:
                    logger.info(
                        'Failed to set clip area from uploaded geometry file')
                    logger.info('Or no shapefile uploaded')
            except:
                logger.info(
                    'An error occurred trying to set clip area from geometry '
                    'file')
                logger.info(traceback.format_exc())
            if not myObject.geometry:
                myErrors = myForm._errors.setdefault('geometry', ErrorList())
                myErrors.append('No valid geometry provided')
                logger.info(
                    'Form is NOT valid - at least a file or digitised geom is '
                    'needed')
                return render(
                    request,
                    'addPage.html',
                    myOptions,
                    )

                # BUG: this code is unreachable, will never execute
                myObject.save()

            logger.debug('Clip: ' + str(myClip))
            logger.info('form is VALID after editing')
            # test of registered user messaging system
            return HttpResponseRedirect(myRedirectPath + str(myObject.id))
        else:
            logger.info('form is INVALID after editing')
            # render_to_response is done by the RenderWithContext decorator
            return ({
                'myTitle': myTitle,
                'mySubmitLabel': 'Submit Clip Request',
                'myTaskingRequestFlag': True,
                'myForm': myForm,
                'myMessages': myMessages,
                'myMessagesHeading': myHeading,
                'myMessagesFlag': True,
                'myLayerDefinitions': myLayerDefinitions,
                'myLayersList': myLayersList,
                # used to show the legend in the accordion
                'myLegendFlag': True,
                'myActiveBaseMap': myActiveBaseMap
            })
    else:
        myForm = ClipForm()
        # render_to_response is done by the RenderWithContext decorator
        return ({
            'myTitle': myTitle,
            'mySubmitLabel': 'Submit Clip Request',
            'myTaskingRequestFlag': True,
            'myForm': myForm,
            'myMessages': myMessages,
            'myMessagesHeading': myHeading,
            'myMessagesFlag': True,
            'myExtent': myExtent,
            'myLayerDefinitions': myLayerDefinitions,
            # used to show the legend in the accordion
            'myLegendFlag': True,
            'myLayersList': myLayersList
        })


@staff_member_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('simpleMap.html')
def visitor_map(request):
    """Show a map of all visitors"""
    myGeoIpUtils = GeoIpUtils()
    myCount = Visit.objects.all()
    myMessages = []
    myLayerDefinitions = None
    myExtent = None
    myLayersList = None
    myLatLong = myGeoIpUtils.getMyLatLong(request)
    # Above returns something like:
    # {'city': 'Johannesburg', 'region': '06', 'area_code': 0, 'longitude':
    # 28.08329963684082, 'country_code3': 'ZAF',
    # 'latitude': -26.200000762939453, 'postal_code': None, 'dma_code': 0,
    # 'country_code': 'ZA', 'country_name': 'South Africa'}
    myMessages.append('<h3>Your details</h3>')
    if not myLatLong:
        myMessages.append('Could not calculate your location')
    else:
        if myLatLong['city']:
            myMessages.append('Nearest City: ' + myLatLong['city'])
        else:
            myMessages.append('Nearest City: Unknown')
        myMessages.append('Country: ' + myLatLong['country_name'])
        myMessages.append('Longitude: ' + str(myLatLong['longitude']))
        myMessages.append('Latitude: ' + str(myLatLong['latitude']))
        myIp = myGeoIpUtils.getMyIp(request)
        myMessages.append('IP Address: ' + myIp)
        myMessages.append('<h3>All visitors</h3>')
        myMessages.append('Total Site Visits: ' + str(myCount))
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        request)
    myLayerDefinitions.append(WEB_LAYERS['Visitors'])
    myLayersList = myLayersList.replace(']', ',visitors]')

    # render_to_response is done by the RenderWithContext decorator
    return ({
        'myMessages': myMessages,
        'myExtents': '-90, -70, 90, 70',
        'myLayerDefinitions': myLayerDefinitions,
        'myLayersList': myLayersList,
        'myActiveBaseMap': myActiveBaseMap,
    })


# RenderWithContext is explained in renderWith.py
@RenderWithContext('productView.html')
def show_product(request, theProductId):
    """
    Renders a search results page including the map and all attendant html
    content - for a single product only identified by its sac product ID
    """
    myProduct = None
    myMessages = []
    myObject = None
    myProducts = GenericProduct.objects.filter(
        original_product_id=theProductId)
    if len(myProducts) > 0:
        myProduct = myProducts[0]
        myObject, myType = myProduct.getConcreteProduct()
        myMessages.append('Product found')
    else:
        myMessages.append('No matching product found')
    return ({
        'messages': myMessages,
        'myProduct': myObject,
    })


# @login_required
@RenderWithContext('productPreview.html')
def show_preview(request, theId, theSize):
    """Show a segment or scene thumbnail details,
      returning the result as a scaled down image.

      This is basically just a wrapper for the showThumb
      method but it returns a html document instead of an image
      mime type. And adds a link to the larger image.
      """
    return {'theId': theId, 'theSize': theSize}


# @login_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('thumbnail.html')
def show_thumb_page(request, theId):
    """Show a segment or scene thumbnail details in a popup dialog"""
    logger.info('showThumbPage : id ' + theId)
    myDetails = []
    myProduct = get_object_or_404(GenericProduct, id=theId)
    myProduct = myProduct.getConcreteProduct()[0]
    # ABP: ugly hack
    try:
        myDetails.append(
            '<tr><th>Sensor:{}</th></tr>'.format(
                myProduct.product_profile.spectral_mode.name)
        )
    except AttributeError:
        pass
    myDetails.append(
        '<tr><td><center><img src=\"/thumbnail/'
        + theId + '/large/"></center></td></tr>')
    # render_to_response is done by the RenderWithContext decorator
    logger.info('Thumbnail path:   ' + str(settings.THUMBS_ROOT))
    logger.info('Static path    :   ' + str(settings.STATIC_ROOT))
    logger.info('Project root path:' + str(settings.PROJECT_ROOT))
    return ({'myDetails': myDetails})


# @login_required
def show_thumb(request, theId, theSize):
    """
    Show a scene thumbnail details,
    returning the result as a scaled down image.
    """
    logger.info('showThumb : id ' + theId)
    myProduct = get_object_or_404(GenericProduct, id=theId)
    myImage = myProduct.thumbnail(theSize)
    if isinstance(myImage, str):
        return HttpResponse('Thumbnail for %s could not be found' % theId)
    else:
        myResponse = HttpResponse(content_type='image/png')
        myImage.save(myResponse, 'PNG')
        return myResponse


# @login_required
def metadata(request, theId):
    """Get the metadata for a product."""
    myGenericProduct = get_object_or_404(GenericProduct, id=theId)
    myObject, myType = myGenericProduct.getConcreteProduct()
    return HttpResponse(myObject.toHtml())


@staff_member_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('searchesmap.html')
def searches_map(request):
    """Show a map of all searches"""


#
# Visitor related views. Visits are recordings of site hits by
# IP and LatLong
#
@login_required()
def visitors_kml(request):
    my_visits = VisitorReport.objects.kml
    return render_to_kml(
        "kml/visitorreport.kml",
        {
            'Visits': my_visits
        },
        'visitors')


@login_required
def delete_search(request, pk):
    """
    We don't ever actually delete a search since we need to see them all for
    site statistics. Rather we mark them as deleted so the user only sees his
    valid ones
    """
    mySearch = None
    try:
        mySearch = Search.objects.get(pk=pk)
        if mySearch.user == request.user:
            mySearch.deleted = True
            mySearch.save()
        else:
            raise ('Search not owned by you!')
    except Exception as myError:
        return HttpResponse(
            '{"success" : False,"reason" : "' + myError + '"}',
            content_type='text/plain')

    # return a simple json object
    return HttpResponse("{'success' : True}", content_type="text/plain")


@login_required
# RenderWithContext is explained in renderWith.py
@RenderWithContext('myClips.html')
def clip_history(request):
    myClipHistory = Clip.objects.filter(
        owner=request.user).order_by('-date')
    return {'myClips': myClipHistory}


###########################################################
#
# Map Query related views
#
###########################################################


@login_required
def get_feature_info(request,
                   theLon,
                   theLat,
                   theBoundingBox,
                   thePixelX,
                   thePixelY,
                   theMapWidth,
                   theMapHeight):
    """
    This is a blind proxy that we use to get around browser restrictions that
    prevent the Javascript from loading pages not on the same server as the
    Javascript.  This has several problems: it's less efficient, it might
    break some sites, and it's a security risk because people can use this
    proxy to browse the web and possibly do bad stuff with it. It only loads
    pages via http and https, but it can load any content type. It supports
    GET and POST requests.
    """

    logger.debug(
        'getFeatureInfo called \n Lon: %s Lat: %s BBox: %s X: %s Y: %s '
        'Height: %s Width: %s' % (
            theLon,
            theLat,
            theBoundingBox,
            thePixelX,
            thePixelY,
            theMapWidth,
            theMapHeight))

    myUrl = "http://" + settings.WMS_SERVER

    myHeaders = {'Content-Type': 'text/plain'}
    myBody = 'foo body'
    try:
        myRequest = urllib.request.Request(myUrl, myBody, myHeaders)
        myResponse = urllib.request.urlopen(myRequest)

        # logger.debug(content type header)
        myInfo = myResponse.info()
        if 'Content-Type' in myInfo:
            logger.debug('Content-Type: %s' % (myInfo['Content-Type']))
        else:
            logger.debug("Content-Type: text/plain")

        logger.debug(myResponse.read())

        myResponse.close()

    except Exception as e:
        logger.debug('Status: 500 Unexpected Error')
        logger.debug('Content-Type: text/plain')
        logger.debug()
        logger.debug('Some unexpected error occurred. Error text was:', e)

    return HttpResponse('Hello world')


###########################################################
#
# Mostly "static" views
#
###########################################################


# RenderWithContext is explained in renderWith.py
@RenderWithContext('index.html')
def index(request):
    # render_to_response is done by the RenderWithContext decorator
    return ({
        'myPartnerFlag': isStrategicPartner(request),
        'slider': Slider.objects.all()
    })


# RenderWithContext is explained in renderWith.py
@RenderWithContext('video.html')
def video(request):
    # render_to_response is done by the RenderWithContext decorator
    return ()


# RenderWithContext is explained in renderWith.py
@RenderWithContext('about.html')
def about(request):
    # render_to_response is done by the RenderWithContext decorator
    return ()


# RenderWithContext is explained in renderWith.py
@RenderWithContext('contact.html')
def contact(request):
    # render_to_response is done by the RenderWithContext decorator
    return (
        {
            'data': Contact.objects.all()
        }
    )


# RenderWithContext is explained in renderWith.py
@RenderWithContext('mapHelp.html')
def map_help(request):
    # render_to_response is done by the RenderWithContext decorator
    if request.is_ajax():
        return ({'myTemplate': 'emptytemplate.html'})
    else:
        return ({'myTemplate': 'base.html'})


# RenderWithContext is explained in renderWith.py
@RenderWithContext('emptyCartHelp.html')
def empty_cart_help(request):
    # render_to_response is done by the RenderWithContext decorator
    return ()


# Note: Dont use the login required decorator here -
# it causes the page to continually try to reload and cpu
# for firefix goes ballistic
# RenderWithContext is explained in renderWith.py
@RenderWithContext('sceneIdHelp.html')
def scene_id_help(request):
    return


# RenderWithContext is explained in renderWith.py
@RenderWithContext('searchFormHelp.html')
def search_form_help(request):
    # render_to_response is done by the RenderWithContext decorator
    return ()
