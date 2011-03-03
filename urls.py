from django.conf.urls.defaults import *
#from django.views.generic import list_detail
from catalogue.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# These dictionaries are used for our generic views
# see http://docs.djangoproject.com/en/dev/intro/tutorial04/
#myOrdersDict = { 'queryset': Order.objects.all(),
   #  "template_object_name" : "myOrders",
#    }


# Here are our patterns

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    # Usually you would do this using apache but since
    # I have deployed the app to the root of the server
    # we need to do it here
    (r'^admin_media/(.*)$','django.views.static.serve',
      {'document_root': "/usr/share/python-support/python-django/django/contrib/admin/media/"
        , 'show_indexes': True}),
    (r'^media/(.*)$','django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^thumbnails/(.*)$','django.views.static.serve',
      {'document_root': settings.THUMBS_ROOT, 'show_indexes': False}),
    (r'^$', index),
    (r'^about/$', about),
    (r'^contact/$', contact),
    (r'^deletesearch/(?P<theId>[0-9]+)/$', deleteSearch),
    (r'^kml/$', visitorsKml),
    (r'^cartkml/$', cartKml),
    (r'^mapHelp/$', mapHelp),
    (r'^emptyCartHelp/$', emptyCartHelp),
    (r'^positionNotFound/$', positionNotFound),
    (r'^sceneidhelp/$', sceneIdHelp),
    (r'^modifysearch/(?P<theGuid>[a-h0-9\-]{36})/$', modifySearch ),
    # match a product id - its not needed to give teh full id, just enough to be semi unique
    (r'^showProduct/(?P<theProductId>[A-Za-z0-9\_\-]{38,58})/$', showProduct ),
    (r'^clip/$', clip),
    (r'^myclips/$', clipHistory),
    (r'^mysearches/$', searchHistory),
    (r'^recentsearches/$', recentSearches),
    (r'^search/$', 'catalogue.views.search.search'), # clashes with module name catalogue.views.search
    (r'^productIdSearch/(?P<theGuid>[a-h0-9\-]{36})/$', productIdSearch),
    (r'^visit/$', logVisit),
    (r'^visitormap/$', visitorMap),
    (r'^whereami/$', whereAmI),
    (r'^worldmap/$', worldMap),

    #show all searches that were made
    (r'^searchesmap/$', searchesMap),
    (r'^visitorlist/$', visitorList),
    (r'^visitorreport/$', visitorReport),
    (r'^visitormonthlyreport/(?P<theyear>\d{4})/(?P<themonth>\d{1,2})/$', visitorMonthlyReport),
    # Profile application
    (r'^accounts/', include('userprofile.urls')),
    (r'^searchkml/(?P<theGuid>[a-h0-9\-]{36})/$', searchKml), #single search poly as kml
     #show a single search map
    (r'^searchresult/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultMap),
    #show a single search page to insert into search result map
    (r'^searchpage/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultPage),
    # return the results of a search as a shapefile
    (r'^searchresultshapefile/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultShapeFile),
    # show segment thumb for a segment by #
    (r'^thumbnailpage/(?P<theId>[0-9]+)/$', showThumbPage),
    (r'^sensordictionaries/$', getSensorDictionaries),
    # returns image mime type - show segment thumb info for a segment
    (r'^thumbnail/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', showThumb),
    # returns html mime type
    (r'^showpreview/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', showPreview),
    #show info for a scene or segment by #
    (r'^metadata/(?P<theId>[0-9]+)/$', metadata),
    (r'^metadatatext/(?P<theId>[0-9]+)/$', metadataText),
    (r'^addtocart/(?P<theId>[0-9]+)/$', addToCart),
    (r'^removefromcart/(?P<theId>[0-9]+)/$', removeFromCart),
    # cart contents for embedding into other pages
    (r'^cartasshapefile/$', cartAsShapefile),
    (r'^showcartcontents/$', showCartContents),
    (r'^showminicartcontents/$', showMiniCartContents),
    #
    # Order management and related lookup tables
    #
    (r'^addorder/', addOrder),
    (r'^deliverydetailform/(?P<theref_id>\d*)/$', createDeilveryDetailForm),
    (r'^myorders/$', myOrders),
    (r'^listorders/$', listOrders),
    (r'^ordermonthlyreport/(?P<theyear>\d{4})/(?P<themonth>\d{1,2})/$', orderMonthlyReport),
    (r'^vieworder/(?P<theId>[0-9]+)/$', viewOrder),
    (r'^vieworderitems/(?P<theOrderId>[0-9]+)/$', viewOrderItems),
    (r'^updateorderhistory/$', updateOrderHistory),
    (r'^orderssummary/$', ordersSummary),
    # Tasking request managmenet
    (r'^addtaskingrequest/', addTaskingRequest),
    (r'^mytaskingrequests/$', myTaskingRequests),
    (r'^viewtaskingrequest/(?P<theId>[0-9]+)/$', viewTaskingRequest),
    (r'^taskingrequestasshapefile/(?P<theTaskingRequestId>[0-9]+)/$', taskingRequestAsShapefile),

    # upload polygon from zipped shapefile for search/clip
    #( r'^uploadFeature/$', uploadFeature),

    (r'^getFeatureInfo/(?P<theLon>[-]*\d+.\d+)/(?P<theLat>[-]*\d+.\d+)/(?P<theBoundingBox>[0-9\-,.]*)/(?P<thePixelX>\d+)/(?P<thePixelY>\d+)/(?P<theMapWidth>\d+)/(?P<theMapHeight>\d+)/$', getFeatureInfo),

    ( r'^dataSummaryTable/$', dataSummaryTable),
)

