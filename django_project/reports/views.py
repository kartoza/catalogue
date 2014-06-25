# coding=utf-8
"""
SANSA-EO Catalogue - Report application views

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
__date__ = '17/08/2012'
__copyright__ = 'South African National Space Agency'

# for error logging
import traceback
# for date handling
import datetime
# python logging support to django logging middleware
import logging
logger = logging.getLogger(__name__)

# Django helpers for forming html pages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
# from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
# from django.contrib.gis.shortcuts import render_to_kml, render_to_kmz
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# from django.template import RequestContext
# from django.forms.util import ErrorList
#for sorted, useful when rendering templates
from django.utils.datastructures import SortedDict

# for aggregate queries
from django.db.models import Count  # for aggregate queries

# Models and forms for our app
from catalogue.models import (
    Visit,
    GenericSensorProduct,
    OpticalProduct
)
from catalogue.renderDecorator import renderWithContext

from search.models import (
    Search,
    SearchRecord,
)

from dictionaries.models import SatelliteInstrumentGroup
from reports.tables import (
    table_sort_settings,
    CountryTable,
    SatelliteInstrumentTable, VisitorTable)
from django.conf import settings
from django_tables2 import RequestConfig
from search.tables import SearchesTable


# in case you need to slice ResultSet (paginate) for display
def slice_for_display(the_list, page_size=10):
    """
    Useful when in need to slice large list (ResultSet) into 'pages'
    which can then be handled separately in template

    :param page_size: int
    :param the_list: list to slice
    Example:
    * myL = [1,1,1,1,2,2,2,2]
    * list(slice_for_display(myL, 4))
    * [[1, 1, 1, 1], [2, 2, 2, 2]]
    """
    #calculate number of rows
    num_rows = (len(the_list) / page_size) + 1
    for myX in xrange(num_rows):
        yield the_list[myX * page_size:myX * page_size + page_size]


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitorReport.html')
def visitor_report(request):
    """
    The view to render a visitor report

    Note: Staff member required

    :param request: HttpRequest
    :return: visitorReport.html :rtype: HttpResponse
    """
    sort_col, sort_order, sort_link = table_sort_settings(request)
    country_stats = Visit.helpers.country_stats(
        sort_col=sort_col or 'count',
        sort_order=sort_order or 'DESC'
    )
    if len(country_stats) > 0:
        table = CountryTable(country_stats)
    else:
        table = None
    #render_to_response is done by the renderWithContext decorator
    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myCurrentMonth': datetime.date.today(),
        'table': table,
        'sort_link': sort_link,
        'myScores': country_stats
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitorMonthlyReport.html')
def visitor_monthly_report(request, year, month):
    """
    The view to return a monthly report on visitor activity

    :param request: HttpRequest
    :param year: Requested year
    :param month: Requested month
    :return: visitorMonthlyReport.html :rtype: HttpResponse
    """
    sort_col, sort_order, sort_link = table_sort_settings(request)
    #construct date object
    if not(year and month):
        my_date = datetime.date.today()
    else:
        try:
            my_date = datetime.date(int(year), int(month), 1)
        except (TypeError, Exception):
            my_date = None
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())

    country_stats = Visit.helpers.monthly_report(
        my_date,
        sort_col=sort_col,
        sort_order=sort_order
    )
    if len(country_stats) > 0:
        table = CountryTable(country_stats)
    else:
        table = None

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'table': table,
        'sort_link': sort_link,
        'myCurrentDate': my_date,
        'myPrevDate': my_date - datetime.timedelta(days=1),
        'myNextDate': my_date + datetime.timedelta(days=31),
        'myScores': country_stats
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitors.html')
def visitor_list(request):
    """
    View to render a list of visitors

    :param request: HttpRequest dict
    :return: visitors.html :rtype: HttpResponse
    """
    # Paginate the results
    records = Visit.objects.all().order_by('-visit_date')
    if 'pdf' in request.GET:
        table = None
        page_size = records.count()
        paginator = Paginator(records, page_size)
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        # If page request (9999) is out of range, deliver last page of results.
        try:
            records = paginator.page(page)
        except (EmptyPage, InvalidPage):
            records = paginator.page(paginator.num_pages)
    else:
        table = VisitorTable(records)
        RequestConfig(request, paginate={
            'per_page': settings.PAGE_SIZE
        }).configure(table)

    #render_to_response is done by the renderWithContext decorator
    return ({
        'records': records,
        'table': table
    })


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('mySearches.html')
def search_history(request):
    """
    The view to return the requesting User's search history

    :param request: HttpRequest dict
    :return: mySearches.html :rtype: HttpResponse
    """
    whole_search_history = Search.objects.filter(
        user=request.user.id).filter(deleted=False).order_by('-search_date')
    table = SearchesTable(whole_search_history)
    RequestConfig(request, paginate={
        'per_page': settings.PAGE_SIZE
    }).configure(table)
    return ({
        'table': table
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('recentSearches.html')
def recent_searches(request):
    """
    View to return a list of recent searches. Limited to 50.

    table is deliberately not orderable as this is the RECENT search history

    :param request: HttpRequest dict
    :return: recentSearches.html :rtype: HttpResponse
    """
    search_history_objs = (
        Search.objects.filter(deleted=False).order_by('-search_date'))
    if len(search_history_objs) > 50:
        search_history_objs = search_history_objs[:50]
    table = SearchesTable(search_history_objs)
    table.orderable = False
    return ({
        'mySearches': search_history,
        'myCurrentMonth': datetime.date.today(),
        'table': table
    })


#monthly search report by user ip_position
@staff_member_required
@renderWithContext('searchMonthlyReport.html')
def search_monthly_report(request, year, month):
    """
    The view to return a monthly search report
    :param request: HttpRequest dict
    :param year: Year to render
    :param month: Month to render
    :return: searchMonthlyReport.html :rtype: HttpResponse
    """
    sort_col, sort_order, sort_link = table_sort_settings(request)
    if not(year and month):
        date = datetime.date.today()
    else:
        try:
            date = datetime.date(int(year), int(month), 1)
        except (TypeError, ValueError, Exception):
            date = None
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())
    country_stats = Search.helpers.monthly_report(
        date,
        sort_col=sort_col,
        sort_order=sort_order
    )
    if len(country_stats) > 0:
        table = CountryTable(country_stats)
    else:
        table = None
    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'table': table,
        'sort_link': sort_link,
        'myCurrentDate': date,
        'myPrevDate': date - datetime.timedelta(days=1),
        'myNextDate': date + datetime.timedelta(days=31),
        'myScores': country_stats
    })


#monthly search report by user ip_position
@staff_member_required
@renderWithContext('searchMonthlyReportAOI.html')
def search_monthly_report_aoi(request, year, month):
    """
    The view to return a table of countries searched for by month

    :param request: HttpRequest dict
    :param year: The year requested (int)
    :param month: The month requested (int)
    :return: searchMonthlyReportAOI.html :rtype: HttpResponse
    """
    sort_col, sort_order, sort_link = table_sort_settings(request)
    if not(year and month):
        date = datetime.date.today()
    else:
        try:
            date = datetime.date(int(year), int(month), 1)
        except (TypeError, Exception):
            date = None
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())

    country_stats = Search.helpers.monthly_report_aoi(
        date,
        sort_col=sort_col,
        sort_order=sort_order
    )
    if len(country_stats) > 0:
        table = CountryTable(country_stats)
    else:
        table = None
    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'table': table,
        'sort_link': sort_link,
        'myCurrentDate': date,
        'myPrevDate': date - datetime.timedelta(days=1),
        'myNextDate': date + datetime.timedelta(days=31),
        'myScores': country_stats
    })


#renderWithContext is explained in renderWith.py
@renderWithContext('dataSummaryTable.html')
def data_summary_table(request):
    """
    Summary of available records
    :param request: HttpRequest dict
    """
    result_set = SatelliteInstrumentGroup.objects.annotate(
        id__count=Count(
            'satelliteinstrument__opticalproductprofile__opticalproduct'))\
        .order_by('satellite__name').filter(id__count__gt=0)
    total = 0
    for result in result_set:
        total += result.id__count
    table = SatelliteInstrumentTable(result_set)
    RequestConfig(request, paginate=False).configure(table)
    return {
        'table': table,
        'total': total,
        'myResultSet': result_set
    }


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('sensorSummaryTable.html')
def sensor_summary_table(request, sensor_id):
    """
    Summary of tasking requests,orders etc for a given sensor
    :param sensor_id: The ID of the sensor requested
    :param request: HttpRequest dict
    """
    #
    # Note: don't use len() to count recs - its very inefficient
    #       use count() rather
    #
    sensor = get_object_or_404(SatelliteInstrumentGroup, id=sensor_id)
    search_count = Search.objects.all().count()
    search_for_sensor_count = Search.objects.filter(
        satellite__satelliteinstrumentgroup=sensor).count()

    product_for_sensor_count = OpticalProduct.objects.filter(
        product_profile__satellite_instrument__satellite_instrument_group=
        sensor).count()
    product_total_count = GenericSensorProduct.objects.count()

    records = SearchRecord.objects.filter(
        user__isnull=False).filter(order__isnull=False)
    product_orders_total_count = records.count()
    product_orders_for_sensor_count = (
        SearchRecord.objects.filter(user__isnull=False)
        .filter(order__isnull=False)
        # No idea how we can PEP8 this one!!
        .filter(product__genericimageryproduct__genericsensorproduct__opticalproduct__product_profile__satellite_instrument__satellite_instrument_group__exact=sensor)
        .count())

    results = SortedDict()
    results['Searches for this sensor'] = search_for_sensor_count
    results['Searches for all sensors'] = search_count
    results['Total ordered products for this sensor'] = \
        product_orders_for_sensor_count
    results['Total ordered products for all sensors'] = \
        product_orders_total_count
    results['Total products for this sensor'] = product_for_sensor_count
    results['Total products for all sensors'] = product_total_count

    sensor_yearly_stats = sensor.products_per_year()

    # define beginning year for yearly product summary
    start_year = 1981
    current_year = datetime.date.today().year
    # create a list of 'empty' records
    sensor_yearly_stats_all = [
        {'year': myYear, 'count': 0}
        for myYear in range(start_year, current_year + 1)]

    # update records, replace with actual data
    for myIdx, myTmpYear in enumerate(sensor_yearly_stats_all):
        for myDataYear in sensor_yearly_stats:
            if myDataYear.get('year') == myTmpYear.get('year'):
                sensor_yearly_stats_all[myIdx] = myDataYear

    return ({
        'myResults': results,
        'mySensor': sensor,
        'mySensorYearlyStats': slice_for_display(sensor_yearly_stats_all)
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('dictionaryReport.html')
def dictionary_report(request):
    """
    Summary of mission, sensor, type and mode. Later we could add
        proc level too
    :param request: HttpRequest
    """

    report = (
        SatelliteInstrumentGroup.objects.all().select_related()
        .order_by('satellite__name')
    )

    return ({
        "myResults": report
    })


@renderWithContext('sensor-fact-sheet.html')
def sensor_fact_sheet(request, sat_abbr):
    """
    The view to render a Sensor's fact sheet

    :param sat_abbr: SatelliteInstrumentGroup.satellite.operator_abbreviation
    :param request: HttpRequest
    :return: HttpResponse
    """
    try:
        sat_group = SatelliteInstrumentGroup.objects.get(
            satellite__operator_abbreviation=sat_abbr
        )
    except SatelliteInstrumentGroup.DoesNotExist:
        return HttpResponseNotFound(
            'Sorry! No fact sheet matches the requested sensor.'
        )
    return ({
        'sat_group': sat_group
    })
