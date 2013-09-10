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

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.paginator import Paginator
from tastypie.exceptions import BadRequest

from .models import Search, SearchRecord
from .searcher import Searcher

from catalogue.models import OpticalProduct


class SearchResultsResource(ModelResource):
    class Meta:
        queryset = OpticalProduct.objects.all()
        resource_name = 'searchresults'
        authentication = SessionAuthentication()
        authorization = Authorization()
        always_return_data = True
        paginator_class = Paginator
        limit = 15
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
        mySearcher = Searcher(mySearch)

        try:
            objects = mySearcher.mQuerySet
            return self.authorized_read_list(objects, bundle)
        except ValueError:
            raise BadRequest(
                'Invalid resource lookup data provided (mismatched type).')


class SearchRecordResource(ModelResource):
    user = fields.ToOneField('useraccounts.api.UserResource', 'user')
    product = fields.ToOneField(
        'catalogue.api.GenericProductResource', 'product', full=True)

    class Meta:
        queryset = SearchRecord.objects.filter(order=None).all()
        resource_name = 'searchrecords'
        authentication = SessionAuthentication()
        authorization = Authorization()
        # always_return_data = True
        paginator_class = Paginator
        limit = 15
        include_resource_uri = False
        # allowed_methods = ['get']

    def obj_create(self, bundle, **kwargs):
        return super(SearchRecordResource, self).obj_create(
            bundle, user=bundle.request.user)

    def get_object_list(self, request):
        import pdb; pdb.set_trace()
        return super(SearchRecordResource, self).get_object_list(
            request).filter(user=request.user.id)
