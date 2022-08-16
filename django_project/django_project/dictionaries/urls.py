from django.conf.urls import url

from .views import collectionList, satelliteDetails

urlpatterns = [
    url(r'^collectionList/$', collectionList),
    url(r'^satelliteDetails/(?P<theSatelliteId>\d*)/$', satelliteDetails),

]
