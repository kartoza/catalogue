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
    #url(r'^sentry/', include('sentry.web.urls')),
    (r'^media/(.*)$','django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^thumbnails/(.*)$','django.views.static.serve',
      {'document_root': settings.THUMBS_ROOT, 'show_indexes': False}),
    (r'^$', index),
    (r'^video/$', video),
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
    (r'^showProductByOriginalId/(?P<theOriginalProductId>[A-Za-z0-9\_\-]{0,58})/$', showProductByOriginalId ),
    (r'^clip/$', clip),
    (r'^myclips/$', clipHistory),
    (r'^mysearches/$', searchHistory),
    (r'^recentsearches/$', recentSearches),
    (r'^searchmonthlyreport/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$', searchMonthlyReport),
    (r'^searchmonthlyreportaoi/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$', searchMonthlyReportAOI),
    (r'^search/$', 'catalogue.views.search.search'), # clashes with module name catalogue.views.search
    (r'^productIdSearchClone/(?P<theGuid>[a-h0-9\-]{36})/$', productIdSearchClone),
    (r'^productIdSearch/(?P<theGuid>[a-h0-9\-]{36})/$', productIdSearch),
    (r'^visit/$', logVisit),
    (r'^visitormap/$', visitorMap),
    (r'^whereami/$', whereAmI),
    (r'^worldmap/$', worldMap),

    #show all searches that were made
    (r'^searchesmap/$', searchesMap),
    (r'^visitorlist/$', visitorList),
    (r'^visitorfrequency/$', visitorFrequency),
    (r'^visitorreport/$', visitorReport),
    (r'^visitormonthlyreport/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$', visitorMonthlyReport),
    # Profile application
    (r'^accounts/', include('userprofile.urls')),
    (r'^searchkml/(?P<theGuid>[a-h0-9\-]{36})/$', searchKml), #single search poly as kml
     #show a single search map
    (r'^searchresult/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultMap),
    #show a single search page to insert into search result map
    (r'^searchpage/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultPage),
    # return the results of a search as a shapefile
    (r'^downloadsearchresults/(?P<theGuid>[a-h0-9\-]{36})/$', downloadSearchResult),
    (r'^downloadsearchmetadata/(?P<theGuid>[a-h0-9\-]{36})/$', downloadSearchResultMetadata),
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
    url(r'^addtocart/(?P<theId>[0-9]+)/$', addToCart, name='addToCart'),
    (r'^removefromcart/(?P<theId>[0-9]+)/$', removeFromCart),
    # cart contents for embedding into other pages
    url(r'^downloadcart/$', downloadCart, name='downloadCart'),
    url(r'^downloadcartmetadata/$', downloadCartMetadata, name='downloadCartMetadata'),
    (r'^myCart/$', showCartContents),
    (r'^showcartcontents/$', showCartContents), #used by xhr requests
    (r'^showminicartcontents/$', showMiniCartContents),
    #
    # Order management and related lookup tables
    #
    (r'^addorder/', addOrder),
    (r'^deliverydetailform/(?P<theReferenceId>\d*)/$', createDeliveryDetailForm),
    (r'^showdeliverydetail/(?P<theReferenceId>\d*)/$', showDeliveryDetail),
    (r'^downloadclipgeometry/(?P<theId>\d*)/$', downloadClipGeometry),
    (r'^downloadordermetadata/(?P<theId>\d*)/$', downloadOrderMetadata),
    (r'^downloadorder/(?P<theId>\d*)/$', downloadOrder),
    (r'^myorders/$', myOrders),
    (r'^listorders/$', listOrders),
    (r'^ordermonthlyreport/(?P<theyear>\d{4})/(?P<themonth>\d{1,2})/$', orderMonthlyReport),
    (r'^vieworder/(?P<theId>[0-9]+)/$', viewOrder),
    (r'^vieworderitems/(?P<theOrderId>[0-9]+)/$', viewOrderItems),
    (r'^updateorderhistory/$', updateOrderHistory),
    (r'^orderssummary/$', ordersSummary),
    # Tasking request managmenet
    url(r'^listtaskingrequests/$', listTaskingRequests, name='listTaskingRequests'),
    url(r'^addtaskingrequest/', addTaskingRequest, name='addTaskingRequest'),
    url(r'^mytaskingrequests/$', myTaskingRequests, name='myTaskingRequests'),
    url(r'^viewtaskingrequest/(?P<theId>[0-9]+)/$', viewTaskingRequest, name='viewTaskingRequest'),
    url(r'^taskingrequest/(?P<theId>\d*)/$', downloadTaskingRequest, name='downloadTaskingRequest'),

    # upload polygon from zipped shapefile for search/clip
    #( r'^uploadFeature/$', uploadFeature),

    (r'^getFeatureInfo/(?P<theLon>[-]*\d+.\d+)/(?P<theLat>[-]*\d+.\d+)/(?P<theBoundingBox>[0-9\-,.]*)/(?P<thePixelX>\d+)/(?P<thePixelY>\d+)/(?P<theMapWidth>\d+)/(?P<theMapHeight>\d+)/$', getFeatureInfo),

    ( r'^dataSummaryTable/$', dataSummaryTable),
    ( r'^dictionaryReport/$', dictionaryReport),
    ( r'^sensorSummaryTable/(?P<theSensorId>[0-9]+)/$', sensorSummaryTable),
    (r'^getUserMessages/$', messaging.userMessages),
    #need to be staff to use this
    (r'^sendMessageToUser/$', messaging.sendMessageToUser),
    #need to be staff to use this
    (r'^sendMessageToAllUsers/$', messaging.sendMessageToAllUsers),

)
