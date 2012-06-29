# Django helpers for forming html pages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.shortcuts import render_to_kml, render_to_kmz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.forms.util import ErrorList

# python logging support to django logging middleware
import logging

# Models and forms for our app
from catalogue.models import *
from catalogue.forms import *
from catalogue.renderDecorator import renderWithContext

# SHP and KML readers
from catalogue.featureReaders import *

# View Helper classes
from geoiputils import *
from searcher import *
from helpers import *

# PIL and os needed for making small thumbs
import os

# For shopping cart and ajax product id search

# for get feature info
import urllib2

# for error logging
import traceback

# for date handling
import datetime

#### VIEW FUNCTIONS ####


def logVisit(theRequest):
    """Silently log a visit and return an empty string. The
    best way to use this method is by adding it as a fake css
    reference at the top of your template e.g.:
    <link rel="stylesheet" href="/visit" type="text/css">
    """
    if settings.USE_GEOIP:
        myGeoIpUtils = GeoIpUtils()
        myIp = myGeoIpUtils.getMyIp(theRequest)
        if myIp:
            myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
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
                myVisit.ip_position = Point(myLatLong['longitude'], myLatLong['latitude'])
                myVisit.ip_address = myIp
                # User is optional - we can see anonymous visits as they will have a null user
                if theRequest.user:
                    myVisit.user = theRequest.user
            except:
                return HttpResponse('/** Error in geoip */',mimetype='text/css')
            myVisit.save()
            # If user is logged in, store their IP lat lon to their profile
            try:
                if theRequest.user:
                    myProfile = theRequest.user.get_profile()
                    myProfile.latitude = str(myLatLong['latitude'])
                    myProfile.longitude = str(myLatLong['longitude'])
                    myProfile.save()
            except:
                    #user has no profile ...
                return HttpResponse('/** No Profile */',mimetype='text/css')
        else:
            logging.info('GEOIP capture failed to retrieve valid position info')
            return HttpResponse('/** No valid position */',mimetype='text/css')
    else:
        logging.info('GEOIP capture disabled in settings')
        return HttpResponse('/** Geoip disabled in settings */',mimetype='text/css')
    return HttpResponse('',mimetype='text/css')

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def whereAmI(theRequest):
    logging.info('whereAmI called...')
    myExtent = '(16,-34, 33, -22)'
    myMessages = []
    myGeoIpUtils = GeoIpUtils()
    myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
    if myLatLong:
        # Above returns something like:
        # {'city': 'Johannesburg', 'region': '06', 'area_code': 0, 'longitude':
        # 28.08329963684082, 'country_code3': 'ZAF', 'latitude': -26.200000762939453,
        # 'postal_code': None, 'dma_code': 0, 'country_code': 'ZA', 'country_name':
        # 'South Africa'}
        myHeading = '<h3><a href="#"><img src="/media/images/wherami_16.png">&nbsp;Your Location</a></h3>'
        myMessages.append('Nearest City: ' + str(myLatLong['city']))
        myMessages.append('Country: ' + str(myLatLong['country_name']))
        myMessages.append('Longitude: ' + str(myLatLong['longitude']))
        myMessages.append('Latitude: ' + str(myLatLong['latitude']))
        myIp = myGeoIpUtils.getMyIp(theRequest)
        myMessages.append('IP Address: ' + myIp)
        # Record the visitor details to our db
        myVisit = Visit()
        if myLatLong['city']:
            myVisit.city = myLatLong['city']
        else:
            myVisit.city = 'Unknown'
        myVisit.country = myLatLong['country_name']
        myVisit.ip_position = Point(myLatLong['longitude'], myLatLong['latitude'])
        myVisit.ip_address = myIp
        myVisit.save()
        myLayerString = """
           /*
           * Layer style
           */
           // we want opaque external graphics and non-opaque internal graphics
           var myLayerStyle = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
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
           var myLayer = new OpenLayers.Layer.Vector("Simple Geometry", {style: myLayerStyle});
           // create a point feature
           var myPoint = new OpenLayers.Geometry.Point(""" + str(myLatLong['longitude']) + "," + str(myLatLong['latitude']) + """);
           myPoint = transformPoint( myPoint );
           var myPointFeature = new OpenLayers.Feature.Vector(myPoint,null,myBlueStyle);
           myLayer.addFeatures([myPointFeature]);
           //map.setCenter(new OpenLayers.LonLat(point.x, point.y), 5);
                        """
        myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2010'],WEB_LAYERS['ZaRoadsBoundaries'], myLayerString ]
        myLayersList = "[zaSpot10mMosaic2010,zaRoadsBoundaries,myLayer]"
        return ( {
          'myGoogleFlag' : 'true',
          'myExtent' : myExtent,
          'myMessagesHeading' : myHeading,
          'myMessages' : myMessages,
          'myLayerDefinitions' : myLayerDefinitions,
          'myLayersList' : myLayersList,
          'myMessagesFlag' : True,
          })

    else:
        myHeading = '<h3><img src="/media/images/wherami_16.png">&nbsp;Your Location</h3>'
        myMessages.append( 'Sorry, we could not resolve your position.' )
        return ( {
          'myGoogleFlag' : None,
          'myExtent' : None,
          'myMessagesHeading' : myHeading,
          'myMessages' : myMessages,
          'myLayerDefinitions' : None,
          'myLayersList' : None,
          'myMessagesFlag' : True,
          })

def worldMap(theRequest):
    """Show a world"""
    myMessages = []
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )

    return render_to_response('simpleMap.html', {
      'myMessages' : myMessages,
      'myLayerDefinitions' : myLayerDefinitions,
      'myLayersList' : myLayersList,
      'myActiveBaseMap' : myActiveBaseMap,
      'myExtents' : "-90, -70, 90, 70"
      })

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('addPage.html')
def clip(theRequest):
    """Show a spot map of South Africa"""
    myTitle = 'Clip Request'
    myExtent = '(15.256693,-35.325000,33.743307,-21.675000)'
    myHeading = '<h3><a href="#"><img src="/media/images/globe_16.png">&nbsp;2008 SPOT5 Mosaic</a></h3>'
    myMessages = []
    myMessages.append('<h3>SPOT5 Mosaic, South Africa</h3>')
    myMessages.append('Initial view is NASA Blue Marble Data, zoom in and the SPOT Mosaic will appear... ')
    myLayerDefinitions = None
    myLayersList = None
    myActiveBaseMap = None
    myProfile = None
    myForm = None

    try:
        myProfile = theRequest.user.get_profile()
    except:
        logging.debug('Profile does not exist')
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
    if theRequest.method == 'POST':
        myForm = ClipForm(theRequest.POST, theRequest.FILES)
        if myForm.is_valid():
            myObject = myForm.save(commit=False)
            myObject.owner = theRequest.user
            myGeometry = None
            try:
                myGeometry = getGeometryFromUploadedFile( theRequest, myForm, 'geometry_file' )
                if myGeometry:
                    myObject.geometry = myGeometry
                else:
                    logging.info("Failed to set clip area from uploaded geometry file")
                    logging.info("Or no shapefile uploaded")
            except:
                logging.info("An error occurred try to set clip area from geometry file")
                logging.info(traceback.format_exc() )
            if not myObject.geometry:
                myErrors = myForm._errors.setdefault("geometry", ErrorList())
                myErrors.append(u"No valid geometry provided")
                logging.info('Form is NOT valid - at least a file or digitised geom is needed')
                return render_to_response("addPage.html",
                    myOptions,
                    context_instance=RequestContext(theRequest))

                myObject.save()


            logging.debug("Clip: " + str( myClip ))
            logging.info('form is VALID after editing')
            #test of registered user messaging system
            theRequest.user.message_set.create(message="Your clip request has been submitted successfully. Please wait for email notification of result availability.")
            return HttpResponseRedirect(myRedirectPath + str(myObject.id))
        else:
            logging.info('form is INVALID after editing')
            #render_to_response is done by the renderWithContext decorator
            return ({
              'myTitle': myTitle,
              'mySubmitLabel' : "Submit Clip Request",
              'myTaskingRequestFlag' : True,
              'myForm': myForm,
              'myMessages' : myMessages,
              'myMessagesHeading' : myHeading,
              'myMessagesFlag' : True,
              'myLayerDefinitions' : myLayerDefinitions,
              'myLayersList' : myLayersList,
              'myLegendFlag' : True, #used to show the legend in the accordion
              'myActiveBaseMap' : myActiveBaseMap
              })
    else:
        myForm = ClipForm()
        #render_to_response is done by the renderWithContext decorator
        return  ( {
          'myTitle': myTitle,
          'mySubmitLabel' : "Submit Clip Request",
          'myTaskingRequestFlag' : True,
          'myForm': myForm,
          'myMessages' : myMessages,
          'myMessagesHeading' : myHeading,
          'myMessagesFlag' : True,
          'myExtent' : myExtent,
          'myLayerDefinitions' : myLayerDefinitions,
          'myLegendFlag' : True, #used to show the legend in the accordion
          'myLayersList' : myLayersList
          })

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('simpleMap.html')
def visitorMap(theRequest):
    """Show a map of all visitors"""
    myGeoIpUtils = GeoIpUtils()
    myCount = Visit.objects.count()
    myMessages = []
    myLayerDefinitions = None
    myExtent = None
    myLayersList = None
    myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
    # Above returns something like:
    # {'city': 'Johannesburg', 'region': '06', 'area_code': 0, 'longitude':
    # 28.08329963684082, 'country_code3': 'ZAF', 'latitude': -26.200000762939453,
    # 'postal_code': None, 'dma_code': 0, 'country_code': 'ZA', 'country_name':
    # 'South Africa'}
    myMessages.append('<h3 class="centered">Your details</h3><br/>')
    if not myLatLong:
        myMessages.append("Could not calculate your location")
    else:
        if myLatLong['city']:
            myMessages.append('Nearest City: ' + myLatLong['city'])
        else:
            myMessages.append('Nearest City: Unknown')
        myMessages.append('Country: ' + myLatLong['country_name'])
        myMessages.append('Longitude: ' + str(myLatLong['longitude']))
        myMessages.append('Latitude: ' + str(myLatLong['latitude']))
        myIp = myGeoIpUtils.getMyIp(theRequest)
        myMessages.append('IP Address: ' + myIp)
        myMessages.append('<h3>All visitors</h3>')
        myMessages.append('Total Site Visits: ' + str(myCount))
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
    myLayerDefinitions.append(WEB_LAYERS['Visitors'])
    myLayersList = myLayersList.replace("]",",visitors]")

    #render_to_response is done by the renderWithContext decorator
    return ( {
      'myMessages' : myMessages,
      'myExtents' : "-90, -70, 90, 70",
      'myLayerDefinitions' : myLayerDefinitions,
      'myLayersList' : myLayersList,
      'myActiveBaseMap' : myActiveBaseMap,
      })



@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('productView.html')
def showProduct(theRequest, theProductId):
    """Renders a search results page including the map
    and all attendant html content - for a single product only
    identified by its sac product ID"""
    myProduct = None
    myMessages = []
    myProducts = GenericProduct.objects.filter(product_id=theProductId)
    if len( myProducts ) > 0:
        myProduct = myProducts[0]
        myObject, myType = myProduct.getConcreteProduct()
        myMessages.append("Product found")
    else:
        myMessages.append("No matching product found")
    return ({
          'messages' : myMessages,
          'myProduct' : myObject,
          })

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('productView.html')
def showProductByOriginalId(theRequest, theOriginalProductId):
    """Renders a search results page including the map
    and all attendant html content - for a single product only
    identified by its sac product ID"""
    myProduct = None
    myMessages = []
    myProducts = GenericProduct.objects.filter(original_product_id=theOriginalProductId)
    if len( myProducts ) > 0:
        myProduct = myProducts[0]
        myProduct.checkForAcsThumb()
        myObject, myType = myProduct.getConcreteProduct()
        myMessages.append("Product found")
    else:
        myMessages.append("No matching product found")
    return ({
          'messages' : myMessages,
          'myProduct' : myObject,
          })


@login_required
def showPreview(theRequest, theId, theSize):
    """Show a segment or scene thumbnail details,
      returning the result as a scaled down image.

      This is basically just a wrapper for the showThumb
      method but it returns a html document instead of an image
      mime type. And adds a link to the larger image.
      """
    return HttpResponse("""
          <center><img src="/thumbnail/"""
          + str(theId)
          + "/"
          + str(theSize)
          + """/"><center>"""
          + """<img src="/media/images/info_32.png" onclick='showMetadata(""" +  str(theId) + """);'  alt="Click to view metadata for this image" title="Click to view metadata for this image" />&nbsp;"""
          + """<img src="/media/images/buy_32.png" onclick='addToCart(""" +  str(theId) + """);'  alt="Click to add to your cart" title="Click to add this image to your cart" />&nbsp;"""
          + """<a id="large_preview" href="/thumbnailpage/"""
          + str(theId)
          + """/"><img src="/media/images/search_32.png" alt="Click for larger view" title="Click for larger preview"/></a>"""
          +"""</center>"""
          , mimetype="text/html")

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('thumbnail.html')
def showThumbPage(theRequest, theId):
    """Show a segment or scene thumbnail details in a popup dialog"""
    logging.info("showThumbPage : id " + theId)
    myDetails=[]
    myProduct = get_object_or_404( GenericProduct, id=theId )
    #ABP: ugly hack
    try:
        myDetails.append("<tr><th>Sensor: " + myProduct.mission_sensor.name + "</th></tr>")
    except AttributeError:
        pass
    myImageFile = os.path.join( myProduct.thumbnailDirectory(), myProduct.product_id + ".jpg" )
    myDetails.append("<tr><td><center><img src=\"/thumbnails/" + myImageFile + "\"></center></td></tr>")
    #render_to_response is done by the renderWithContext decorator
    logging.info('Thumbnail path:   ' + str(settings.THUMBS_ROOT))
    logging.info('Media path    :   ' + str(settings.MEDIA_ROOT))
    logging.info('Project root path:' + str(settings.ROOT_PROJECT_FOLDER))
    return ( { 'myDetails' : myDetails } )

@login_required
def showThumb(theRequest, theId, theSize):
    """Show a scene thumbnail details,
      returning the result as a scaled down image."""
    logging.info("showThumb : id " + theId)
    myProduct = get_object_or_404( GenericProduct, id=theId )
    myImage = myProduct.thumbnail( theSize )
    if (isinstance(myImage, str)):
        return HttpResponse("Thumbnail for %s could not be found" % theId )
    else:
        myResponse = HttpResponse(mimetype="image/png")
        myImage.save(myResponse, "PNG")
        return ( myResponse )


@login_required
def metadataText(theRequest, theId):
    myGenericProduct = get_object_or_404( GenericProduct, id=theId )
    myString = "<pre>%s</pre>" % myGenericProduct.metadata
    return HttpResponse( myString )

@login_required
def metadata(theRequest, theId):
    """Get the metadata for a product."""
    myGenericProduct = get_object_or_404( GenericProduct, id=theId )
    myObject, myType = myGenericProduct.getConcreteProduct()
    return ( HttpResponse( myObject.toHtml() ) )

def searchKml(theRequest, theGuid):
    """Show a kml of a single search"""
    mySearch = get_object_or_404(Search, guid=theGuid)
    return render_to_kml("kml/search.kml", {'search' : mySearch}, 'search')

def cartKml(theRequest):
    """Show a kml of a single search"""
    myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
    return render_to_kmz("kml/cart.kml", {'myRecords' : myRecords})

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def searchesMap(theRequest):
    """Show a map of all searches"""
    myMessages = []
    myLayerDefinitions = None
    myLayersList = None
    myExtent = '(-90.0,-45.0, 90.0, 45.0)'
    myMessages.append('<h3>All searches</h3>')
    myCount = Search.objects.count()
    myMessages.append('Total Searches: ' + str(myCount))
    myLayerDefinitions = [ WEB_LAYERS['BlueMarble'],WEB_LAYERS['Heatmap-total'],WEB_LAYERS['Heatmap-last3month'],WEB_LAYERS['Heatmap-lastmonth'],WEB_LAYERS['Heatmap-lastweek'],WEB_LAYERS['Searches'] ]
    myLayersList = "[BlueMarble, heatmap_total, heatmap_last3month, heatmap_lastmonth, heatmap_lastweek,searches]"
    #myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaRoadsBoundaries'], WEB_LAYERS['Searches'] ]
    #myLayersList = "[zaSpot10mMosaic2009,zaRoadsBoundaries,searches]"

    #render_to_response is done by the renderWithContext decorator
    return ( {
      'myMessages' : myMessages,
      'myExtent' : myExtent,
      'myLayerDefinitions' : myLayerDefinitions,
      'myLayersList' : myLayersList,
      'myPartnerFlag' : isStrategicPartner(theRequest),
      'myShowSearchFeatureInfoFlag' : 'true',
      'myLegendFlag':'true',
      'mySearchAreasToggle' : 'true',
      })

#
# Visitor related views. Visits are recordings of site hits by
# IP and LatLong
#
def visitorsKml(theRequest):
    myVisits = VisitorReport.objects.kml()
    return render_to_kml("kml/visitorreport.kml", {'Visits' : myVisits}, 'visitors')


@login_required
def deleteSearch(theRequest, theId):
    """We don't ever actually delete a search since we need to see them
    all for site statistics. Rather we mark them as deleted so the
    user only sees his valid ones"""
    mySearch = None
    try:
        mySearch = Search.objects.get(id=theId)
        if mySearch.user == theRequest.user:
            mySearch.deleted=True
            mySearch.save()
        else:
            rasise ("Search not owned by you!")
    except Exception, myError:
        return HttpResponse("{'success' : False,'reason' : '" + myError + "'}", mimetype="text/plain")

    #return a simple json object
    return HttpResponse("{'success' : True}", mimetype="text/plain")


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('myClips.html')
def clipHistory(theRequest):
    clipHistory = Clip.objects.filter(owner=theRequest.user).order_by('-date')
    return ({'myClips' : clipHistory})

###########################################################
#
# Map Query related views
#
###########################################################


@login_required
def getFeatureInfo(theRequest,
                   theLon,
                   theLat,
                   theBoundingBox,
                   thePixelX,
                   thePixelY,
                   theMapWidth,
                   theMapHeight):
    """This is a blind proxy that we use to get around browser
    restrictions that prevent the Javascript from loading pages not on the
    same server as the Javascript.  This has several problems: it's less
    efficient, it might break some sites, and it's a security risk because
    people can use this proxy to browse the web and possibly do bad stuff
    with it.  It only loads pages via http and https, but it can load any
    content type. It supports GET and POST requests."""

    logging.debug("getFeatureInfo called \n Lon: %s Lat: %s BBox: %s X: %s Y: %s Height: %s Width: %s" % (
                     theLon,
                     theLat,
                     theBoundingBox,
                     thePixelX,
                     thePixelY,
                     theMapWidth,
                     theMapHeight))

    myGeometryQuery = Q(frame_geometry__intersects=(self.mSearch.geometry))
    myUrl = "http://" + settings.WMS_SERVER

    myHeaders = {"Content-Type": "text/plain"}
    myBody = "foo body"
    try:
        myRequest = urllib2.Request( myUrl, myBody, myHeaders )
        myResponse = urllib2.urlopen( myRequest )

        # logging.debug(content type header)
        myInfo = myResponse.info()
        if myInfo.has_key( "Content-Type" ):
            logging.debug("Content-Type: %s" % ( myInfo["Content-Type"] ))
        else:
            logging.debug("Content-Type: text/plain")

        logging.debug(myResponse.read())

        myResponse.close()

    except Exception, E:
        logging.debug("Status: 500 Unexpected Error")
        logging.debug("Content-Type: text/plain")
        logging.debug( )
        logging.debug("Some unexpected error occurred. Error text was:", E)

    return HttpResponse("Hello world")

###########################################################
#
# Mostly "static" views
#
###########################################################


#renderWithContext is explained in renderWith.py
@renderWithContext('index.html')
def index(theRequest):
    myMissions = Mission.objects.all()
    #render_to_response is done by the renderWithContext decorator
    return ({
          'myPartnerFlag': isStrategicPartner(theRequest),
          'myMissions': myMissions,
        }
      )


#renderWithContext is explained in renderWith.py
@renderWithContext('video.html')
def video(theRequest):
    #render_to_response is done by the renderWithContext decorator
    return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('about.html')
def about(theRequest):
    #render_to_response is done by the renderWithContext decorator
    return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('contact.html')
def contact(theRequest):
    #render_to_response is done by the renderWithContext decorator
    return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('mapHelp.html')
def mapHelp(theRequest):
    #render_to_response is done by the renderWithContext decorator
    if theRequest.is_ajax():
        return ( {"myTemplate" : "emptytemplate.html"})
    else:
        return ( {"myTemplate" : "base.html"})

#renderWithContext is explained in renderWith.py
@renderWithContext('emptyCartHelp.html')
def emptyCartHelp(theRequest):
    #render_to_response is done by the renderWithContext decorator
    return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('positionNotFound.html')
def positionNotFound(theRequest):
    #render_to_response is done by the renderWithContext decorator
    return ()

#Note: Dont use the login required decorator here -
# it causes the page to continually try to reload and cpu
# for firefix goes ballistic
#renderWithContext is explained in renderWith.py
@renderWithContext('sceneIdHelp.html')
def sceneIdHelp(theRequest):
    return
