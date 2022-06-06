# from django.conf.urls.defaults import *
from django.conf.urls import include, url
# from django.views.generic import list_detail
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from catalogue.views.others import (
    index,
    video,
    about,
    search_form_help,
    contact,
    delete_search,
    visitors_kml,
    map_help,
    empty_cart_help,
    scene_id_help,
    show_product,
    clip,
    clip_history,
    log_visit,
    visitor_map,
    whereAmI,
    searches_map,
    show_thumb_page,
    show_thumb,
    show_preview,
    metadata,
    get_feature_info
)
from catalogue.views.shopping_cart import (
    addToCart,
    removeFromCart,
    download_cart,
    downloadCartMetadata,
    show_cart_contents,
    showMiniCartContents,
)
from catalogue.views.messaging import (
    userMessages,
    sendMessageToUser,
    sendMessageToAllUsers
)

# These are used for our generic views
# see http://docs.djangoproject.com/en/dev/intro/tutorial04/
# myOrdersDict = { 'queryset': Order.objects.all(),
#  "template_object_name" : "myOrders",
#    }

from .api import v1_API
from catalogue.api import VisitorGeojson

admin.autodiscover()

# Here are our patterns
urlpatterns = [
    # Uncomment the next line to enable the admin:
    url(r'^eo-catalogue-backend/', admin.site.urls),
    # Usually you would do this using apache but since
    # I have deployed the app to the root of the server
    # we need to do it here
    # url(r'^admin_media/(.*)$','django.views.static.serve',
    #   {'document_root': "/usr/share/python-support/python-django/django/contrib/admin/media/"
    #     , 'show_indexes': True}),
    # (r'^sentry/', include('sentry.web.urls')),
    # url(r'^media/(.*)$','django.views.static.serve',
    #   {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    # url(r'^thumbnails/(.*)$','django.views.static.serve',
    #   {'document_root': settings.THUMBS_ROOT, 'show_indexes': False}),
    url(r'^$', index, name='index'),
    url(r'^video/$', video, name='video'),
    url(r'^about/$', about, name='about'),
    url(r'^searchformhelp/$', search_form_help, name='searchformhelp'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^deletesearch/(?P<pk>[0-9]+)/$', delete_search, name='deleteSearch'),
    url(r'^kml/$', visitors_kml, name='visitorsKml'),
    url(r'^mapHelp/$', map_help, name='mapHelp'),
    url(r'^emptyCartHelp/$', empty_cart_help, name='emptyCartHelp'),
    url(r'^sceneidhelp/$', scene_id_help, name='sceneIdHelp'),

    # match a product id - its not needed to give teh full id, just enough to be semi unique
    url(r'^showProduct/(?P<theProductId>.*)/$', show_product, name='showProduct'),
    url(r'^clip/$', clip),
    # is this used?
    url(r'^myclips/$', clip_history),
    url(r'^visit/$', log_visit, name='logVisit'),
    url(r'^visitor-map/$', visitor_map, name='visitor-map'),
    url(r'^whereami/$', whereAmI, name='whereAmI'),

    # show all searches that were made
    url(r'^searches-map/$', searches_map, name='searches-map'),

    # show segment thumb for a segment by #
    # thumbnailpage is called only by itself?
    url(r'^thumbnailpage/(?P<theId>[0-9]+)/$', show_thumb_page, name='showThumbPage'),

    # returns image mime type - show segment thumb info for a segment
    url(r'^thumbnail/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', show_thumb, name='showThumb'),
    # returns html mime type
    url(r'^showpreview/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', show_preview, name='showPreview'),
    # show info for a scene or segment by #
    url(r'^metadata/(?P<pk>[0-9]+)/$', metadata, name="metadata"),
    url(r'^addtocart/(?P<pk>[0-9]+)/$', addToCart, name='addToCart'),
    url(r'^removefromcart/(?P<theId>[0-9]+)/$', removeFromCart, name='removeFromCart'),
    # cart contents for embedding into other pages
    url(r'^downloadcart/$', download_cart, name='downloadCart'),
    url(r'^downloadcartmetadata/$', downloadCartMetadata, name='downloadCartMetadata'),
    url(r'^show-cart-contents/$', show_cart_contents, name='show-cart-contents'),  # used by xhr requests
    url(r'^showminicartcontents/$', showMiniCartContents, name='showMiniCartContents'),

    # upload polygon from zipped shapefile for search/clip
    # ( r'^uploadFeature/$', uploadFeature),

    url(r'^getFeatureInfo/(?P<theLon>[-]*\d+.\d+)/(?P<theLat>[-]*\d+.\d+)/(?P<theBoundingBox>[0-9\-,.]*)/(?P<thePixelX>\d+)/(?P<thePixelY>\d+)/(?P<theMapWidth>\d+)/(?P<theMapHeight>\d+)/$',
        get_feature_info),

    url(r'^getUserMessages/$', userMessages),
    # need to be staff to use this
    url(r'^sendMessageToUser/$', sendMessageToUser),
    # need to be staff to use this
    url(r'^sendMessageToAllUsers/$', sendMessageToAllUsers),

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
    url(r'^visitors/geojson$',
        VisitorGeojson.as_view(), name='visitor-geojson'),

    # api urls
    url(r'^api/', include(v1_API.urls)),
]
