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

import logging

from django.conf.urls import url
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.paginator import Paginator
from tastypie.exceptions import BadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.api_fields import ProductRelField

from search.models import Search, SearchRecord
from search.searcher import Searcher
from search.serializers import SearchRecordSerializer

from catalogue.models import OpticalProduct
from catalogue.serializers.product_serializer import OpticalProductSerializer

from catalogue.limitoffset_pagination import LimitOffsetPagination

logger = logging.getLogger(__name__)


class SearchResultsResource(ModelResource):
    product_name = fields.CharField(attribute='product_name')

    class Meta:
        queryset = OpticalProduct.objects.all()
        resource_name = 'searchresults'
        # authentication = SessionAuthentication()
        # authorization = Authorization()
        always_return_data = True
        paginator_class = Paginator
        limit = settings.RESULTS_NUMBER
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

    def dehydrate_product_date(self, bundle):
        return bundle.data['product_date'].strftime('%d/%m/%Y')

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
    product = ProductRelField(
        'catalogue.api.OpticalProductResource', 'product', full=True)

    class Meta:
        queryset = SearchRecord.objects.filter(order=None).all()
        resource_name = 'searchrecords'
        authentication = SessionAuthentication()
        authorization = Authorization()
        # always_return_data = True
        paginator_class = Paginator
        limit = 100
        include_resource_uri = False
        # allowed_methods = ['get']

    def obj_create(self, bundle, **kwargs):
        return super(SearchRecordResource, self).obj_create(
            bundle, user=bundle.request.user)

    def get_object_list(self, request):
        return super(SearchRecordResource, self).get_object_list(
            request).filter(user=request.user.id)


class SearchRecordView(APIView):
    """
    Retrieve, update or delete a search record.
    """

    def get_object(self, pk):
        try:
            return SearchRecord.objects.get(pk=pk)
        except SearchRecord.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = SearchRecordSerializer(record)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = SearchRecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        record = self.get_object(pk)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddSearchRecordView(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        context = {
            "request": self.request,
        }
        serializer = SearchRecordSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchResultsResourceView(ListAPIView):
    serializer_class = OpticalProductSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        search = get_object_or_404(Search, guid=self.kwargs.get('guid'))
        result = Searcher(search)

        try:
            query_list = result.mQuerySet
            return query_list

        except OpticalProduct.DoesNotExist:
            return HttpResponse(
                'Object Does Not Exist',
                status=status.HTTP_400_BAD_REQUEST
            )
