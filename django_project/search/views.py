"""
SANSA-EO Catalogue - Search related views

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

# python logger support to django logger middleware
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

import traceback
import tempfile

from itertools import chain
from django.conf import settings

# For shopping cart and ajax product id search
import json as simplejson

# Django helpers for forming html pages
from django.shortcuts import get_object_or_404
from django.http import (
    HttpResponse,
    Http404)
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.views.decorators import staff_member_required
#from django.db.models import Count, Min, Max  # for aggregate queries
from django.forms.models import inlineformset_factory

# Helper classes

#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

from catalogue.renderDecorator import renderWithContext

from catalogue.views.helpers import (
    render_to_kml,
    render_to_kmz,
    downloadHtmlMetadata,
    downloadISOMetadata)

# SHP and KML readers
from catalogue.featureReaders import (
    getGeometryFromUploadedFile,
    getFeaturesFromZipFile,
    getFeaturesFromKMLFile,
    processGeometriesType)

from catalogue.views.geoiputils import GeoIpUtils

from dictionaries.models import Collection


# modularized app dependencies
from .searcher import Searcher

from .models import (
    Search,
    SearchDateRange,
    SearchRecord
)

from .forms import (
    AdvancedSearchForm,
    DateRangeFormSet,
    DateRangeForm
)

from .utils import SearchView


class Http500(Exception):
    pass

DateRangeInlineFormSet = inlineformset_factory(
    Search, SearchDateRange, fields='__all__', extra=0, max_num=0,
    formset=DateRangeFormSet,form=DateRangeForm)


#@login_required
def downloadSearchResult(theRequest, theGuid):
    """Dispaches request and returns searchresults in desired file format"""
    mySearch = get_object_or_404(Search, guid=theGuid)
    mySearcher = Searcher(mySearch)
    mySearchView = SearchView(theRequest, mySearcher)

    myFilename = u'%s-imagebounds' % theGuid
    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(SearchRecord)
        myResponder.file_name = myFilename
        return myResponder.write_search_records(mySearchView.mSearchRecords)
    elif 'kml' in theRequest.GET:
        return render_to_kml(
            'kml/searchRecords.kml', {
                'mySearchRecords': mySearchView.mSearchRecords,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True},
            myFilename)
    elif 'kmz' in theRequest.GET:
        #next two lines for debugging only since we
        #cant catch exceptions when these methods are called in templates
        #mySearcher.mSearchRecords[0].kmlExtents()
        #mySearcher.mSearchRecords[0].product.georeferencedThumbnail()
        return render_to_kmz(
            'kml/searchRecords.kml', {
                'mySearchRecords': mySearchView.mSearchRecords,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True,
                'myThumbsFlag': True},
            myFilename)
    else:
        logger.info(
            'Request cannot be proccesed, unsupported download file type')
        raise Http404


#@login_required
def downloadSearchResultMetadata(theRequest, theGuid):
    """
    Returns ISO 19115 metadata for searchresults. I t defaults to xml format
    unless a ?html is appended to the url
    """

    mySearch = get_object_or_404(Search, guid=theGuid)
    mySearcher = Searcher(mySearch)
    mySearchView = SearchView(theRequest, mySearcher)

    if 'html' in theRequest.GET:
        return downloadHtmlMetadata(
            mySearchView.mSearchRecords, 'Search-%s' % theGuid)
    else:
        return downloadISOMetadata(
            mySearchView.mSearchRecords, 'Search-%s' % theGuid)


@login_required
@renderWithContext('page.html')
def searchguid(theRequest, theGuid):
    """
    Given a search guid, give the user a form prepopulated with
    that search's criteria so they can modify their search easily.
    A new search will be created from the modified one.
    """

    mySearch = get_object_or_404(Search, guid=theGuid)
    myForm = AdvancedSearchForm(instance=mySearch)
    myFormset = DateRangeInlineFormSet(instance=mySearch)

    collections = Collection.objects.all().prefetch_related('satellite_set')

    sel_instrumenttypes = mySearch.instrument_type.all().values_list(
        'pk', flat=True)
    sel_satellites = mySearch.satellite.all().values_list('pk', flat=True)

    data = [{
        'key': col.name,
        'val': 'cc{}'.format(col.pk),
        # we need to unnest the lists, and for that purpose we reuse chain
        # from iterable module
        'values': list(chain.from_iterable((({
            'key': '{} {}'.format(sat.name, sig.instrument_type.name),
            'val': '{}|{}'.format(sat.pk, sig.instrument_type.pk)
            } for sig in sat.satelliteinstrumentgroup_set.all()
            # only select instrument_types which are searchable
            if sig.instrument_type.is_searchable)
            for sat in col.satellite_set.all())))
    } for col in collections
    ]

    # prepare the selected data subset
    selected_data = [{
        'key': col.name,
        'val': 'cc{}'.format(col.pk),
        # we need to unnest the lists, and for that purpose we reuse chain
        # from iterable module
        'values': list(chain.from_iterable((({
            'key': '{} {}'.format(sat.name, sig.instrument_type.name),
            'val': '{}|{}'.format(sat.pk, sig.instrument_type.pk)
        } for sig in sat.satelliteinstrumentgroup_set.all()
            if sig.instrument_type.pk in sel_instrumenttypes)
            for sat in col.satellite_set.all() if sat.pk in sel_satellites)))
    } for col in collections
    ]

    myListTreeOptions = simplejson.dumps(data)
    myListTreeSelected = simplejson.dumps(selected_data)

    return {
        'mysearch': mySearch, 'searchform': myForm, 'dateformset': myFormset,
        'listreeoptions': myListTreeOptions,
        'selected_options': myListTreeSelected,
        'searchlistnumber': settings.RESULTS_NUMBER
    }


@renderWithContext('page.html')
def searchView(theRequest):
    """
    Perform an attribute and spatial search for imagery
    """
    col_names = ['ZA South Africa', 'SAC','ERS']
    sat_names = [
        'CBERS-2B',
        'CBERS-04-P10',
        'Landsat 1',
        'Landsat 2',
        'Landsat 3',
        'Landsat 4']
    modified_sat_names = [
        'CBERS-04-MUX',
        'CBERS-04-P5M',
        'CBERS-04-WFI']
    collections = Collection.objects.all().prefetch_related('satellite_set')\
        .exclude(name__in=col_names)
    data = [{
        'key': col.name,
        'val': 'cc{}'.format(col.pk),
        # we need to unnest the lists, and for that purpose we reuse chain
        # from iterable module
        'values': list(chain.from_iterable((({
            'key': '{} {}'.format((
                'CBERS-04' if sat.name in modified_sat_names else sat.name),
                                  sig.instrument_type.name),
            'val': '{}|{}'.format(sat.pk, sig.instrument_type.pk)
            } for sig in sat.satelliteinstrumentgroup_set.all()
            # only select instrument_types which are searchable
            if sig.instrument_type.is_searchable)
            for sat in col.satellite_set.all().exclude(name__in=sat_names))))
            } for col in collections
    ]

    myListTreeOptions = simplejson.dumps(data)

    # add forms
    myForm = AdvancedSearchForm()
    myFormset = DateRangeInlineFormSet()
    return {
        'searchform': myForm, 'dateformset': myFormset,
        'listreeoptions': myListTreeOptions,
        'selected_options': [], 'searchlistnumber': settings.RESULTS_NUMBER
    }


def submitSearch(theRequest):
    """
    Perform an attribute and spatial search for imagery
    """
    myFormErrors = {}
    if theRequest.method == 'POST':
        post_values = theRequest.POST
        # if the request.POST is not 'multipart/form-data' then QueryDict that
        # holds POST values is not mutable, however, we need it to be mutable
        # because 'save_as_new' on inlineformset directly changes values
        #
        # we need to force this behavior
        post_values._mutable = True

        logger.debug('Post vars: %s', str(post_values))
        myForm = AdvancedSearchForm(post_values, theRequest.FILES)
        logger.debug('Uploaded files: %s', theRequest.FILES)

        if myForm.is_valid():
            logger.info('AdvancedForm is VALID')
            mySearch = myForm.save(commit=False)
            # ABP: save_as_new is necessary due to the fact that a new Search
            # object is always
            # created even on Search modify pages
            myFormset = DateRangeInlineFormSet(
                post_values, theRequest.FILES, instance=mySearch,
                save_as_new=True)
            if myFormset.is_valid():
                logger.info('Daterange formset is VALID')
                myLatLong = {'longitude': 0, 'latitude': 0}

                if settings.USE_GEOIP:
                    try:
                        myGeoIpUtils = GeoIpUtils()
                        myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
                    except:
                        # raise forms.ValidationError( "Could not get geoip for
                        # for this request" + traceback.format_exc() )
                        # do nothing - better in a production environment
                        pass
                if myLatLong:
                    mySearch.ip_position = (
                        'SRID=4326;POINT(' + str(myLatLong['longitude']) + ' '
                        + str(myLatLong['latitude']) + ')')
                #if user is anonymous set to None
                if theRequest.user.is_anonymous():
                    mySearch.user = None
                else:
                    mySearch.user = theRequest.user
                mySearch.deleted = False
                try:
                    myGeometry = getGeometryFromUploadedFile(
                        theRequest, myForm, 'geometry_file')
                    if myGeometry:
                        mySearch.geometry = myGeometry
                    else:
                        logger.info(
                            'Failed to set search area from uploaded geometry '
                            'file')
                except:
                    logger.error(
                        'Could not get geometry for this request' +
                        traceback.format_exc())
                    logger.info(
                        'An error occurred trying to set search area from '
                        'uploaded geometry file')
                #check if aoi_geometry exists
                myAOIGeometry = myForm.cleaned_data.get('aoi_geometry')
                if myAOIGeometry:
                    logger.info('Using AOI geometry, specified by user')
                    mySearch.geometry = myAOIGeometry
                # else use the on-the-fly digitised geometry
                mySearch.save()
                """
                Another side effect of using commit=False is seen when your
                model has a many-to-many relation with another model. If your
                model has a many-to-many relation and you specify commit=False
                when you save a form, Django cannot immediately save the form
                data for the many-to-many relation. This is because it isn't
                possible to save many-to-many data for an instance until the
                instance exists in the database.

                To work around this problem, every time you save a form using
                commit=False, Django adds a save_m2m() method to your ModelForm
                subclass. After you've manually saved the instance produced by
                the form, you can invoke save_m2m() to save the many-to-many
                form data.

                ref: http://docs.djangoproject.com/en/dev/topics/forms
                            /modelforms/#the-save-method
                """
                myForm.save_m2m()
                logger.debug('Search: ' + str(mySearch))
                logger.info('form is VALID after editing')
                myFormset.save()

                return HttpResponse(simplejson.dumps({
                    "guid": mySearch.guid
                }), content_type='application/json')

            else:
                myFormErrors.update({
                    'daterange': myFormset._non_form_errors
                })
                myFormErrors.update(myFormset.errors)
                logger.debug('%s' % myFormset.errors)

        # if we got to this point, then the form is invalid
        logger.info('form is INVALID after editing')
        logger.debug('%s' % myForm.errors)

        # form was not valid return 404
        myFormErrors.update(myForm.errors)
        return HttpResponse(
            simplejson.dumps(myFormErrors),
            content_type='application/json', status=404)
    # we can only process POST requests
    return HttpResponse('Not a POST!', status=404)


def upload_geo(theRequest):
    """
    Extract geometry from uploaded geometry
    """
    if theRequest.FILES and theRequest.FILES.get('file_upload'):
        f = theRequest.FILES.get('file_upload')

        myExtension = (f.name.split('.')[-1].lower())
        if not(myExtension == 'zip' or myExtension == 'kml' or
                myExtension == 'kmz'):
            return HttpResponse(
                simplejson.dumps({"error": "File needs to be KML/KMZ/ZIP"}),
                content_type='application/json', status=500)

        destination = tempfile.NamedTemporaryFile(
            delete=False, suffix='.{0}'.format(myExtension))
        # get the filename
        myOutFile = destination.name
        # write the file
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

        myExtension = (f.name.split('.')[-1].lower())

        if myExtension == 'zip':
            extractedGeometries = getFeaturesFromZipFile(
                myOutFile, 'Polygon', 1)
        else:
            extractedGeometries = getFeaturesFromKMLFile(
                myOutFile, 'Polygon', 1)
        if len(extractedGeometries) == 0:
            return HttpResponse(
                simplejson.dumps({"error": "No geometries found..."}),
                content_type='application/json', status=500)
        else:
            return HttpResponse(
                simplejson.dumps({
                    "wkt": processGeometriesType(extractedGeometries).wkt}),
                content_type='application/json', status=200)
