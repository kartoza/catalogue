"""
SANSA-EO Catalogue - Search API (TastyPie)

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '27/08/2013'
__copyright__ = 'South African National Space Agency'

from django.conf.urls import url
from django.shortcuts import get_object_or_404

from tastypie.api import Api
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
# from tastypie.authentication import SessionAuthentication
from tastypie.paginator import Paginator
from tastypie.exceptions import BadRequest

from .models import Search
from .searcher import Searcher

from catalogue.models import OpticalProduct


class SearchResultsResource(ModelResource):
    class Meta:
        queryset = OpticalProduct.objects.all()
        resource_name = 'searchresults'
        # authentication = SessionAuthentication()
        authorization = Authorization()
        always_return_data = True
        paginator_class = Paginator
        limit = 10
        include_resource_uri = False
        allowed_methods = ['get']

    def resource_uri_kwargs(self, bundle_or_obj=None):
        # required to build resource uri with proper guid (Search id)
        kwargs = super(
            SearchResultsResource, self).resource_uri_kwargs(bundle_or_obj)
        kwargs.update(self.kwargs)
        return kwargs

    def dispatch_list(self, request, **kwargs):
        # add request kwargs to the object so we can reuse it in
        # resource_uri_kwargs
        self.kwargs = kwargs
        return self.dispatch('list', request, **kwargs)

    def prepend_urls(self):
        # override the default url for retrieving the object list
        # supports guid of the searches
        myUrl = r'^(?P<resource_name>{0})/(?P<guid>[a-h0-9\-]{{36}})/$'.format(
            self._meta.resource_name)
        return [
            url(
                myUrl,
                self.wrap_view('dispatch_list'), name='api_dispatch_list'),
        ]

    def obj_get_list(self, bundle, *args, **kwargs):
        # for the specific guid, retrieve the results
        mySearch = get_object_or_404(Search, guid=kwargs.get('guid'))
        mySearcher = Searcher(bundle.request, mySearch)
        mySearcher.search()

        try:
            objects = mySearcher.mQuerySet
            return self.authorized_read_list(objects, bundle)
        except ValueError:
            raise BadRequest(
                'Invalid resource lookup data provided (mismatched type).')

# register the api
v1_API = Api(api_name='v1')
v1_API.register(SearchResultsResource())
