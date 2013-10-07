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
from itertools import chain

# For shopping cart and ajax product id search
from django.utils import simplejson

# Django helpers for forming html pages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    Http404,
    HttpResponseServerError)
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext, loader, Context
#from django.db.models import Count, Min, Max  # for aggregate queries
from django.forms.models import inlineformset_factory

# Helper classes

#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

from catalogue.renderDecorator import renderWithContext

from catalogue.views.helpers import (
    standardLayers,
    render_to_kml,
    render_to_kmz,
    downloadHtmlMetadata,
    downloadISOMetadata)

# SHP and KML readers
from catalogue.featureReaders import (
    getGeometryFromUploadedFile,)

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
    DateRangeFormSet
)

from .utils import prepareSelectQuerysets, SearchView


class Http500(Exception):
    pass

DateRangeInlineFormSet = inlineformset_factory(
    Search, SearchDateRange, extra=0, max_num=0, formset=DateRangeFormSet)


@login_required
def modifySearch(theRequest, theGuid):
    """
    Given a search guid, give the user a form prepopulated with
    that search's criteria so they can modify their search easily.
    A new search will be created from the modified one.
    """
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        theRequest)
    logger.info('initial search form being rendered')
    mySearch = get_object_or_404(Search, guid=theGuid)
    myForm = AdvancedSearchForm(instance=mySearch)
    myFormset = DateRangeInlineFormSet(instance=mySearch)
    return render_to_response(
        'searchv3.html', {
            'myFormset': myFormset,
            'myForm': myForm,
            'myGuid': theGuid,
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
            'myActiveBaseMap': myActiveBaseMap},
        context_instance=RequestContext(theRequest))


#@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def searchResultMap(theRequest, theGuid):
    """
    Renders a search results page including the map and all attendant html
    content
    """
    mySearch = get_object_or_404(Search, guid=theGuid)

    mySearcher = Searcher(mySearch)
    mySearchView = SearchView(theRequest, mySearcher)

    return(mySearchView.templateData())


#@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('page.html')
def searchResultPage(theRequest, theGuid):
    """
    Does the same as searchResultMap but renders only enough html to be
    inserted into a div
    """
    mySearch = get_object_or_404(Search, guid=theGuid)
    mySearcher = Searcher(mySearch)
    mySearchView = SearchView(theRequest, mySearcher)

    return(mySearchView.templateData())


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
    mySearcher = Searcher(theRequest, mySearch)
    mySearchView = SearchView(theRequest, mySearcher)

    if 'html' in theRequest.GET:
        return downloadHtmlMetadata(
            mySearchView.mSearchRecords, 'Search-%s' % theGuid)
    else:
        return downloadISOMetadata(
            mySearchView.mSearchRecords, 'Search-%s' % theGuid)


def renderSearchForm(theRequest):
    """
    Returns Search Form HTML used with AJAX calls
    """
    logger.info('initial search form being rendered')
    myForm = AdvancedSearchForm()
    myFormset = DateRangeInlineFormSet()
    #render_to_response is done by the renderWithContext decorator
    return render_to_response(
        'searchPanelv3.html', {
            'myForm': myForm,
            'myFormset': myFormset},
        context_instance=RequestContext(theRequest))


def renderSearchMap(theRequest):
    """
    Returns Search Map HTML used with AJAX calls
    """
    logger.info('initial search map being rendered')
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        theRequest)
    #render_to_response is done by the renderWithContext decorator
    return render_to_response(
        'map_containerv3.html', {
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
            'myActiveBaseMap': myActiveBaseMap},
        context_instance=RequestContext(theRequest))


#@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('pagev3.html')
def renderSearchResultsPage(theRequest, theGuid):
    """
    Does the same as searchResultMap but renders only enough html to be
    inserted into a div
    """
    mySearch = get_object_or_404(Search, guid=theGuid)

    mySearcher = Searcher(mySearch)
    mySearchView = SearchView(theRequest, mySearcher)
    return(mySearchView.templateData())


def updateSelectOptions(theRequest):
    """
    Returns JSON encoded InstrumentTypes, Satellites and SpectralModes options
    """
    mySelCollections = theRequest.GET.getlist('collections')
    mySelSatellite = theRequest.GET.getlist('satellites')
    mySelInstrumentType = theRequest.GET.getlist('instrumenttypes')
    mySelSpectralGroups = theRequest.GET.getlist('spectralgroups')
    mySelLicenseTypes = theRequest.GET.getlist('licencetypes')

    myQS_data = prepareSelectQuerysets(
        mySelCollections, mySelSatellite, mySelInstrumentType,
        mySelSpectralGroups, mySelLicenseTypes)

    myFinalData = {
        'collections': [(
            option.pk,
            unicode(option)) for option in myQS_data[0]],
        'satellites': [(
            option.pk,
            unicode(option)) for option in myQS_data[1]],
        'instrumenttypes': [(
            option.pk,
            unicode(option)) for option in myQS_data[2]],
        'spectralgroups': [(
            option.pk,
            unicode(option)) for option in myQS_data[3]],
        'licensetypes': [(
            option.pk,
            unicode(option)) for option in myQS_data[4]]
    }
    return HttpResponse(
        simplejson.dumps(myFinalData), mimetype='application/json')


@login_required
def searchguid(theRequest, theGuid):
    """
    Given a search guid, give the user a form prepopulated with
    that search's criteria so they can modify their search easily.
    A new search will be created from the modified one.
    """
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        theRequest)
    logger.info('initial search form being rendered')
    myForm = AdvancedSearchForm()
    myFormset = DateRangeInlineFormSet()
    # render_to_response is done by the renderWithContext decorator
    return render_to_response(
        'searchv3.html', {
            'myAdvancedFlag': False,
            'mySearchType': None,
            'myForm': myForm,
            'myFormset': myFormset,
            'myHost': settings.HOST,
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
            'myActiveBaseMap': myActiveBaseMap,
            'theGuid': theGuid},
        context_instance=RequestContext(theRequest))


@renderWithContext('page.html')
def searchView(theRequest):
    """
    Perform an attribute and spatial search for imagery
    """
    myForm = AdvancedSearchForm()
    myFormset = DateRangeInlineFormSet()

    return {'searchform': myForm, 'dateformset': myFormset}


def getSelectOptions(theRequest):
    """
    """
    collections = Collection.objects.all().prefetch_related('satellite_set')
    data = [{
        'key': col.name,
        'val': 'cc{}'.format(col.pk),
        # we need to unnest the lists, and for that purpose we reuse chain
        # from iterable module
        'values': list(chain.from_iterable((({
            'key': '{} {}'.format(sat.name, sig.instrument_type.name),
            'val': '{}|{}'.format(sat.pk, sig.instrument_type.pk)
            } for sig in sat.satelliteinstrumentgroup_set.all())
            for sat in col.satellite_set.all())))
        } for col in collections
    ]

    return HttpResponse(
        simplejson.dumps(data), mimetype='application/json')


def submitSearch(theRequest):
    """
    Perform an attribute and spatial search for imagery
    """
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
                }), mimetype='application/json')
            else:
                logger.debug('Daterange formset is NOT VALID')
                logger.debug(myFormset.errors)
        else:
            logger.info('form is INVALID after editing')
            logger.debug('%s' % myForm.errors)
            # logger.debug('%s' % myFormset.errors)

            # form was not valid return 404
            return HttpResponse(str(myForm.errors), status=404)
    return HttpResponse('Not a POST!', status=404)
