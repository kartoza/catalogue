from django.conf.urls import url

from .api import SearchRecordView, AddSearchRecordView
from .views import (
    downloadSearchResult,
    downloadSearchResultMetadata,
    searchView,
    searchguid,
    submitSearch,
    upload_geo
)

urlpatterns = [
    # return the results of a search as a shapefile
    url(r'^downloadsearchresults/(?P<guid_id>[a-h0-9\-]{36})/$',
        downloadSearchResult, name='downloadSearchResult'),
    url(r'^downloadsearchmetadata/(?P<guid_id>[a-h0-9\-]{36})/$',
        downloadSearchResultMetadata, name='downloadSearchResultMetadata'),
    url(r'^search/$', searchView, name='search'),
    url(r'^search/(?P<guid_id>[a-h0-9\-]{36})/$',
        searchguid, name='searchGuid'),
    url(r'^submitsearch/$', submitSearch,
        name='submitSearch'),
    url(r'^upload_geo/$', upload_geo,
        name='upload_geo'),
    url('api/searchrecords', AddSearchRecordView.as_view()),
    url('api/searchrecords/<int:pk>', SearchRecordView.as_view()),
]
