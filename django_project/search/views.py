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
# from django.contrib.admin.views.decorators import staff_member_required
# from django.db.models import Count, Min, Max  # for aggregate queries
from django.forms.models import inlineformset_factory

# Helper classes

# Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

from catalogue.render_decorator import RenderWithContext

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

logger = logging.getLogger(__name__)


class Http500(Exception):
    pass


DateRangeInlineFormSet = inlineformset_factory(
    Search, SearchDateRange, fields='__all__', extra=0, max_num=0,
    formset=DateRangeFormSet, form=DateRangeForm)


# @login_required
def downloadSearchResult(request, guid_id):
    """Dispaches request and returns searchresults in desired file format"""
    search = get_object_or_404(Search, guid=guid_id)
    searcher = Searcher(search)
    search_view = SearchView(request, searcher)

    filename = '%s-imagebounds' % guid_id
    if 'shp' in request.GET:
        responder = ShpResponder(SearchRecord)
        responder.file_name = filename
        return responder.write_search_records(search_view.mSearchRecords)
    elif 'kml' in request.GET:
        return render_to_kml(
            'kml/searchRecords.kml', {
                'mySearchRecords': search_view.mSearchRecords,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True},
            filename
        )
    elif 'kmz' in request.GET:
        # next two lines for debugging only since we
        # cant catch exceptions when these methods are called in templates
        # mySearcher.mSearchRecords[0].kmlExtents()
        # mySearcher.mSearchRecords[0].product.georeferencedThumbnail()
        return render_to_kmz(
            'kml/searchRecords.kml', {
                'mySearchRecords': search_view.mSearchRecords,
                'external_site_url': settings.DOMAIN,
                'transparentStyle': True,
                'myThumbsFlag': True},
            filename
        )
    else:
        logger.info(
            'Request cannot be proccesed, unsupported download file type')
        raise Http404


# @login_required
def downloadSearchResultMetadata(request, guid_id):
    """
    Returns ISO 19115 metadata for searchresults. I t defaults to xml format
    unless a ?html is appended to the url
    """

    search = get_object_or_404(Search, guid=guid_id)
    searcher = Searcher(search)
    search_view = SearchView(request, searcher)

    if 'html' in request.GET:
        return downloadHtmlMetadata(
            search_view.mSearchRecords, 'Search-%s' % guid_id)
    else:
        return downloadISOMetadata(
            search_view.mSearchRecords, 'Search-%s' % guid_id)


@login_required
@RenderWithContext('page.html')
def searchguid(request, guid_id):
    """
    Given a search guid, give the user a form prepopulated with
    that search's criteria so they can modify their search easily.
    A new search will be created from the modified one.
    """

    search = get_object_or_404(Search, guid=guid_id)
    form = AdvancedSearchForm(instance=search)
    form_set = DateRangeInlineFormSet(instance=search)

    collections = Collection.objects.all().prefetch_related('satellite_set')

    sel_instrument_types = search.instrument_type.all().values_list(
        'pk', flat=True)
    sel_satellites = search.satellite.all().values_list('pk', flat=True)

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
            if sig.instrument_type.pk in sel_instrument_types)
            for sat in col.satellite_set.all() if sat.pk in sel_satellites)))
    } for col in collections
    ]

    list_tree_options = simplejson.dumps(data)
    list_tree_selected = simplejson.dumps(selected_data)

    return {
        'mysearch': search,
        'searchform': form,
        'dateformset': form_set,
        'listreeoptions': list_tree_options,
        'selected_options': list_tree_selected,
        'searchlistnumber': settings.RESULTS_NUMBER
    }


@RenderWithContext('page.html')
def searchView(request):
    """
    Perform an attribute and spatial search for imagery
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
        } for sig in sat.satelliteinstrumentgroup_set.all()
            # only select instrument_types which are searchable
            if sig.instrument_type.is_searchable)
            for sat in col.satellite_set.all())))
    } for col in collections
    ]

    list_tree_options = simplejson.dumps(data)

    # add forms
    form = AdvancedSearchForm()
    form_set = DateRangeInlineFormSet()
    return {
        'searchform': form,
        'dateformset': form_set,
        'listreeoptions': list_tree_options,
        'selected_options': [],
        'searchlistnumber': settings.RESULTS_NUMBER
    }


def submitSearch(request):
    """
    Perform an attribute and spatial search for imagery
    """
    form_errors = {}
    if request.method == 'POST':
        post_values = request.POST
        # if the request.POST is not 'multipart/form-data' then QueryDict that
        # holds POST values is not mutable, however, we need it to be mutable
        # because 'save_as_new' on inlineformset directly changes values
        #
        # we need to force this behavior
        post_values._mutable = True

        logger.debug('Post vars: %s', str(post_values))
        form = AdvancedSearchForm(post_values, request.FILES)
        logger.debug('Uploaded files: %s', request.FILES)

        if form.is_valid():
            logger.info('AdvancedForm is VALID')
            search = form.save(commit=False)
            # ABP: save_as_new is necessary due to the fact that a new Search
            # object is always
            # created even on Search modify pages
            form_set = DateRangeInlineFormSet(
                post_values,
                request.FILES,
                instance=search,
                save_as_new=True)
            if form_set.is_valid():
                logger.info('Daterange formset is VALID')
                lat_long = {'longitude': 0, 'latitude': 0}

                if settings.USE_GEOIP:
                    try:
                        lat_long = GeoIpUtils().getMyLatLong(request)
                    except:
                        # raise forms.ValidationError( "Could not get geoip for
                        # for this request" + traceback.format_exc() )
                        # do nothing - better in a production environment
                        pass
                if lat_long:
                    search.ip_position = (
                            'SRID=4326;POINT(' + str(lat_long['longitude']) + ' '
                            + str(lat_long['latitude']) + ')')
                # if user is anonymous set to None
                if request.user.is_anonymous:
                    search.user = None
                else:
                    search.user = request.user
                search.deleted = False
                try:
                    geometry = getGeometryFromUploadedFile(
                        request, form, 'geometry_file')
                    if geometry:
                        search.geometry = geometry
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
                # check if aoi_geometry exists
                aoi_geometry = form.cleaned_data.get('aoi_geometry')
                if aoi_geometry:
                    logger.info('Using AOI geometry, specified by user')
                    search.geometry = aoi_geometry
                # else use the on-the-fly digitised geometry
                search.save()
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
                form.save_m2m()
                logger.debug('Search: ' + str(search))
                logger.info('form is VALID after editing')
                form_set.save()

                return HttpResponse(simplejson.dumps({
                    "guid": search.guid
                }), content_type='application/json')

            else:
                form_errors.update({
                    'daterange': form_set._non_form_errors
                })
                form_errors.update(form_set.errors)
                logger.debug('%s' % form_set.errors)

        # if we got to this point, then the form is invalid
        logger.info('form is INVALID after editing')
        logger.debug('%s' % form.errors)

        # form was not valid return 404
        form_errors.update(form.errors)
        return HttpResponse(
            simplejson.dumps(form_errors),
            content_type='application/json', status=404)
    # we can only process POST requests
    return HttpResponse('Not a POST!', status=404)


def upload_geo(request):
    """
    Extract geometry from uploaded geometry
    """
    if request.FILES and request.FILES.get('file_upload'):
        f = request.FILES.get('file_upload')

        extension = (f.name.split('.')[-1].lower())
        if not (extension == 'zip' or extension == 'kml' or
                extension == 'kmz'):
            return HttpResponse(
                simplejson.dumps({"error": "File needs to be KML/KMZ/ZIP"}),
                content_type='application/json', status=500)

        destination = tempfile.NamedTemporaryFile(
            delete=False, suffix='.{0}'.format(extension))
        # get the filename
        out_file = destination.name
        # write the file
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

        extension = (f.name.split('.')[-1].lower())

        if extension == 'zip':
            extracted_geometries = getFeaturesFromZipFile(
                out_file, 'Polygon', 1)
        else:
            extracted_geometries = getFeaturesFromKMLFile(
                out_file, 'Polygon', 1)
        if len(extracted_geometries) == 0:
            return HttpResponse(
                simplejson.dumps({"error": "No geometries found..."}),
                content_type='application/json', status=500)
        else:
            return HttpResponse(
                simplejson.dumps({
                    "wkt": processGeometriesType(extracted_geometries).wkt}),
                content_type='application/json', status=200)
