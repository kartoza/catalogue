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
from django.template import RequestContext
#from django.db.models import Count, Min, Max  # for aggregate queries
from django.forms.models import inlineformset_factory

# Models and forms for our app
from catalogue.models import (
    AcquisitionMode,
    Mission,
    MissionSensor,
    SensorType
)


from catalogue.renderDecorator import renderWithContext

# Helper classes

#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

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


# modularized app dependencies
from .searcher import (
    Searcher)

from .models import (
    Search,
    SearchDateRange,
    SearchRecord
)

from .forms import (
    AdvancedSearchForm,
    DateRangeFormSet,
    ProductIdSearchForm,
)


class Http500(Exception):
    pass

DateRangeInlineFormSet = inlineformset_factory(
    Search, SearchDateRange, extra=0, max_num=0, formset=DateRangeFormSet)


def detectAdvancedSearchForm(theSearchForm):
    """
    Based on search form input determine if the form is advanced
    """
    if theSearchForm.data.get('isAdvanced') == 'true':
        return True
    myFormIsAdvancedTest = [
        theSearchForm.data.get('sensor_inclination_angle_start') != '',
        theSearchForm.data.get('sensor_inclination_angle_end') != '',
        theSearchForm.data.get('j_frame_row') != '',
        theSearchForm.data.get('aoi_geometry') != '',
        theSearchForm.data.get('spatial_resolution') != '',
        theSearchForm.data.get('acquisition_mode') != '',
        theSearchForm.data.get('geometry_file') != '',
        theSearchForm.data.get('k_orbit_path') != '',
        theSearchForm.data.get('band_count') != '',
        theSearchForm.data.get('license_type') != '',
        theSearchForm.data.get('geometry') != '',
        theSearchForm.data.get('sensor_type') != '',
        (theSearchForm.data.get('cloud_mean') != '' and
            theSearchForm.data.get('cloud_mean') != '0')
    ]
    return any(myFormIsAdvancedTest)


#@login_required
#theRequest context decorator not used here since we have different return
#paths
def search(theRequest):
    """
    Perform an attribute and spatial search for imagery
    """

    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        theRequest)
    logger.debug(('Post vars:' + str(theRequest.POST)))
    logger.info('search called')
    if theRequest.method == 'POST':
        myForm = AdvancedSearchForm(theRequest.POST, theRequest.FILES)
        if myForm.is_valid():
            mySearch = myForm.save(commit=False)
            # ABP: save_as_new is necessary due to the fact that a new Search
            # object is always
            # created even on Search modify pages
            myFormset = DateRangeInlineFormSet(
                theRequest.POST, theRequest.FILES, instance=mySearch,
                save_as_new=True)
            if myFormset.is_valid():
                logger.info('formset is VALID')
                myLatLong = {'longitude': 0, 'latitude': 0}

                if settings.USE_GEOIP:
                    try:
                        myGeoIpUtils = GeoIpUtils()
                        myIp = myGeoIpUtils.getMyIp(theRequest)
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

                return HttpResponseRedirect(
                    reverse(
                        'searchResultMap', kwargs={'theGuid': mySearch.guid})
                )
            else:
                logger.info('formset is INVALID')
                logger.debug('%s' % myFormset.errors)
        else:
            myFormset = DateRangeInlineFormSet(
                theRequest.POST, theRequest.FILES, save_as_new=True)

        logger.info('form is INVALID after editing')
        logger.debug('%s' % myForm.errors)
        logger.debug('%s' % myFormset.errors)
        #render_to_response is done by the renderWithContext decorator
        return render_to_response(
            'search.html', {
                'myAdvancedFlag': detectAdvancedSearchForm(myForm),
                'mySearchType': theRequest.POST['search_type'],
                'myForm': myForm,
                'myHost': settings.HOST,
                'myFormset': myFormset,
                'myLayerDefinitions': myLayerDefinitions,
                'myLayersList': myLayersList,
                'myActiveBaseMap': myActiveBaseMap},
            context_instance=RequestContext(theRequest))

    else:
        logger.info('initial search form being rendered')
        myForm = AdvancedSearchForm()
        myFormset = DateRangeInlineFormSet()
        #render_to_response is done by the renderWithContext decorator
        return render_to_response(
            'search.html', {
                'myAdvancedFlag': False,
                'mySearchType': None,
                'myForm': myForm,
                'myFormset': myFormset,
                'myHost': settings.HOST,
                'myLayerDefinitions': myLayerDefinitions,
                'myLayersList': myLayersList,
                'myActiveBaseMap': myActiveBaseMap},
            context_instance=RequestContext(theRequest))


@login_required
def getSensorDictionaries(theRequest):
    """
    Given a set of search sensor-releated criteria, returns
    valid options for the selects.
    """
    values = {}
    if theRequest.is_ajax():
        # ABP: Returns a json object with the dictionary possible values
        qs = AcquisitionMode.objects.order_by()
        if (int(theRequest.POST.get('search_type')) in
                (Search.PRODUCT_SEARCH_RADAR, Search.PRODUCT_SEARCH_OPTICAL)):
            is_radar = (
                (int(theRequest.POST.get('search_type'))
                    == Search.PRODUCT_SEARCH_RADAR))
            qs = qs.filter(sensor_type__mission_sensor__is_radar=is_radar)
        values['mission'] = list(qs.distinct().values_list(
            'sensor_type__mission_sensor__mission', flat=True))
        if theRequest.POST.get('mission'):
            try:
                qs = qs.filter(
                    sensor_type__mission_sensor__mission=
                    Mission.objects.get(pk=theRequest.POST.get('mission')))
            except ObjectDoesNotExist:
                raise Http500('Mission does not exists')
        # m2m
        values['sensors'] = list(qs.distinct().values_list(
            'sensor_type__mission_sensor', flat=True))
        if theRequest.POST.get('sensors'):
            try:
                qs = qs.filter(
                    sensor_type__mission_sensor__in=MissionSensor.objects
                    .filter(pk__in=theRequest.POST.getlist('sensors')))
            except ObjectDoesNotExist:
                raise Http500('SensorType does not exists')
        values['sensor_type'] = list(qs.distinct().values_list(
            'sensor_type', flat=True))
        if theRequest.POST.get('sensor_type'):
            try:
                qs = qs.filter(
                    sensor_type=SensorType.objects.get(
                        pk=theRequest.POST.get('sensor_type')))
            except ObjectDoesNotExist:
                raise Http500('SensorType does not exists')
        values['acquisition_mode'] = list(qs.distinct().values_list(
            'pk', flat=True))
        if  theRequest.POST.get('acquisition_mode'):
            qs = qs.filter(pk=theRequest.POST.get('acquisition_mode'))
        return HttpResponse(
            simplejson.dumps(values), mimetype='application/json')
    raise Http500('This view must be called by XHR')


#@login_required
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
        'search.html', {
            'myAdvancedFlag': mySearch.isAdvanced,
            'mySearchType': mySearch.search_type,
            'myFormset': myFormset,
            'myForm': myForm,
            'myGuid': theGuid,
            'myHost': settings.HOST,
            'myLayerDefinitions': myLayerDefinitions,
            'myLayersList': myLayersList,
            'myActiveBaseMap': myActiveBaseMap},
        context_instance=RequestContext(theRequest))


@login_required
# theRequest context decorator not used here since we have different return
# paths
def productIdSearch(theRequest, theGuid):
    """
    Display the product id builder, based on initial existing Search values,
    the following interaction is ajax based.
    This kind of search is only available when search_type is
    PRODUCT_SEARCH_OPTICAL
    """
    myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers(
        theRequest)
    mySearch = get_object_or_404(Search, guid=theGuid)

    if mySearch.search_type != Search.PRODUCT_SEARCH_OPTICAL:
        raise Http500(
            'productIdSearch is only available for products of type '
            'PRODUCT_SEARCH_OPTICAL')

    logger.info(
        'productIdSearch initializing values from existing search %s' % (
            theGuid,))
    mySearcher = Searcher(theRequest, theGuid)
    mySearcher.search()
    myTemplateData = mySearcher.templateData()

    if theRequest.method == 'POST':
        myForm = ProductIdSearchForm(
            theRequest.POST, theRequest.FILES, instance=mySearch)
        if myForm.is_valid():
            logger.info('productIdSearch form is VALID after editing')
            logger.info(
                'productIdSearch cleaned_data: %s' % myForm.cleaned_data)
            myForm.save()
            # Save new date ranges
            if myForm.cleaned_data.get('date_range'):
                mySearch.searchdaterange_set.all().delete()
                # http://stackoverflow.com/
                # questions/400739/what-does-mean-in-python
                # for ** explanation below
                mySearch.searchdaterange_set.add(
                    SearchDateRange(**myForm.cleaned_data.get('date_range')))
            # Save new sensors
            if myForm.cleaned_data.get('sensors'):
                for sensor in myForm.cleaned_data.get('sensors'):
                    mySearch.sensors.add(sensor)
            if theRequest.is_ajax():
                # ABP: Returns a json object with query description.
                # We need to instantiate the Searcher since search logic
                # is not in the Search class :(
                mySearcher = Searcher(theRequest, theGuid)
                return HttpResponse(simplejson.dumps(
                    mySearcher.describeQuery()), mimetype='application/json')
            else:
                return HttpResponseRedirect(
                    reverse(
                        'searchResultMap', kwargs={'theGuid': mySearch.guid})
                )

        else:
            logger.info('form is INVALID after editing')
            if theRequest.is_ajax():
                # Sends a 500
                return HttpResponseServerError(
                    simplejson.dumps(myForm.errors),
                    mimetype='application/json')
            return render_to_response(
                'productIdSearch.html', {
                    'mySearch': mySearch,
                    'myForm': myForm,
                    'theGuid': theGuid},
                context_instance=RequestContext(theRequest))
    else:
        myForm = ProductIdSearchForm(instance=mySearch)
        logger.info('initial search form being rendered')
        myTemplateData['mySearch'] = mySearch
        myTemplateData['myForm'] = myForm
        myTemplateData['theGuid'] = theGuid
        myTemplateData['filterValues'] = simplejson.dumps(
            mySearcher.describeQuery()['values'])
        return render_to_response(
            'productIdSearch.html', myTemplateData,
            context_instance=RequestContext(theRequest))


#@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def searchResultMap(theRequest, theGuid):
    """
    Renders a search results page including the map and all attendant html
    content
    """
    mySearcher = Searcher(theRequest, theGuid)
    mySearcher.search()
    return(mySearcher.templateData())


#@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('page.html')
def searchResultPage(theRequest, theGuid):
    """
    Does the same as searchResultMap but renders only enough html to be
    inserted into a div
    """
    mySearcher = Searcher(theRequest, theGuid)
    mySearcher.search()
    return(mySearcher.templateData())


#@login_required
def downloadSearchResult(theRequest, theGuid):
    """Dispaches request and returns searchresults in desired file format"""
    mySearcher = Searcher(theRequest, theGuid)
    mySearcher.search(False)  # dont paginate

    myFilename = u'%s-imagebounds' % theGuid
    if 'shp' in theRequest.GET:
        myResponder = ShpResponder(SearchRecord)
        myResponder.file_name = myFilename
        return myResponder.write_search_records(mySearcher.mSearchRecords)
    elif 'kml' in theRequest.GET:
        return render_to_kml(
            'kml/searchRecords.kml', {
                'mySearchRecords': mySearcher.mSearchRecords,
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
                'mySearchRecords': mySearcher.mSearchRecords,
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

    mySearcher = Searcher(theRequest, theGuid)
    mySearcher.search(False)  # dont paginate
    if 'html' in theRequest.GET:
        return downloadHtmlMetadata(
            mySearcher.mSearchRecords, 'Search-%s' % theGuid)
    else:
        return downloadISOMetadata(
            mySearcher.mSearchRecords, 'Search-%s' % theGuid)