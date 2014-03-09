#from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
#from django.views.generic import list_detail
from catalogue.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# These are used for our generic views
# see http://docs.djangoproject.com/en/dev/intro/tutorial04/
#myOrdersDict = { 'queryset': Order.objects.all(),
   #  "template_object_name" : "myOrders",
#    }

from api import v1_API

# Here are our patterns
urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^eo-catalogue-backend/', include(admin.site.urls)),
    # Usually you would do this using apache but since
    # I have deployed the app to the root of the server
    # we need to do it here
    url(r'^admin_media/(.*)$','django.views.static.serve',
      {'document_root': "/usr/share/python-support/python-django/django/contrib/admin/media/"
        , 'show_indexes': True}),
    #(r'^sentry/', include('sentry.web.urls')),
    url(r'^media/(.*)$','django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^thumbnails/(.*)$','django.views.static.serve',
      {'document_root': settings.THUMBS_ROOT, 'show_indexes': False}),
    url(r'^$', index, name='index'),
    url(r'^video/$', video, name='video'),
    url(r'^about/$', about, name='about'),
    url(r'^searchformhelp/$', searchFormHelp, name='searchformhelp'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^deletesearch/(?P<theId>[0-9]+)/$', deleteSearch, name='deleteSearch'),
    url(r'^kml/$', visitorsKml, name='visitorsKml'),
    url(r'^mapHelp/$', mapHelp, name='mapHelp'),
    url(r'^emptyCartHelp/$', emptyCartHelp, name='emptyCartHelp'),
    url(r'^sceneidhelp/$', sceneIdHelp, name='sceneIdHelp'),

    # match a product id - its not needed to give teh full id, just enough to be semi unique
    url(r'^showProduct/(?P<theProductId>[A-Za-z0-9]+)/$', showProduct, name='showProduct'),
    url(r'^clip/$', clip),
    # is this used?
    url(r'^myclips/$', clipHistory),
    url(r'^visit/$', logVisit, name='logVisit'),
    url(r'^visitormap/$', visitorMap, name='visitorMap'),
    url(r'^whereami/$', whereAmI, name='whereAmI'),

    #show all searches that were made
    url(r'^searchesmap/$', searchesMap, name='searchesMap'),

    # show segment thumb for a segment by #
    # thumbnailpage is called only by itself?
    url(r'^thumbnailpage/(?P<theId>[0-9]+)/$', showThumbPage, name='showThumbPage'),

    # returns image mime type - show segment thumb info for a segment
    url(r'^thumbnail/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', showThumb, name='showThumb'),
    # returns html mime type
    url(r'^showpreview/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', showPreview, name='showPreview'),
    #show info for a scene or segment by #
    url(r'^metadata/(?P<theId>[0-9]+)/$', metadata, name="metadata"),
    url(r'^addtocart/(?P<theId>[0-9]+)/$', addToCart, name='addToCart'),
    url(r'^removefromcart/(?P<theId>[0-9]+)/$', removeFromCart, name='removeFromCart'),
    # cart contents for embedding into other pages
    url(r'^downloadcart/$', downloadCart, name='downloadCart'),
    url(r'^downloadcartmetadata/$', downloadCartMetadata, name='downloadCartMetadata'),
    url(r'^showcartcontents/$', showCartContents, name='showCartContents'), #used by xhr requests
    url(r'^showminicartcontents/$', showMiniCartContents, name='showMiniCartContents'),


    # upload polygon from zipped shapefile for search/clip
    #( r'^uploadFeature/$', uploadFeature),

    url(r'^getFeatureInfo/(?P<theLon>[-]*\d+.\d+)/(?P<theLat>[-]*\d+.\d+)/(?P<theBoundingBox>[0-9\-,.]*)/(?P<thePixelX>\d+)/(?P<thePixelY>\d+)/(?P<theMapWidth>\d+)/(?P<theMapHeight>\d+)/$', getFeatureInfo),

    url(r'^getUserMessages/$', messaging.userMessages),
    #need to be staff to use this
    url(r'^sendMessageToUser/$', messaging.sendMessageToUser),
    #need to be staff to use this
    url(r'^sendMessageToAllUsers/$', messaging.sendMessageToAllUsers),

    # New dictionaries
    url(r'', include('dictionaries.urls')),
    # New user profile management
    url(r'', include('useraccounts.urls')),
    # New search app
    url(r'', include('search.urls')),
    # pycsw integration
    url(r'', include('pycsw_integration.urls')),
    # new reports app
    url(r'', include('reports.urls')),
    # new orders app
    url(r'', include('orders.urls')),


    # api urls
    url(r'^api/', include(v1_API.urls)),
)
