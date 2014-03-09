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


# in case you need to slice ResultSet (paginate) for display
def sliceForDisplay(theList, thePageSize=10):
    """
    Useful when in need to slice large list (ResultSet) into 'pages'
    which can then be handled separately in template

    Example:
    * myL = [1,1,1,1,2,2,2,2]
    * list(sliceForDisplay(myL, 4))
    * [[1, 1, 1, 1], [2, 2, 2, 2]]
    """
    #calculate number of rows
    myNumRows = (len(theList) / thePageSize) + 1
    for myX in xrange(myNumRows):
        yield theList[myX * thePageSize:myX * thePageSize + thePageSize]


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitorReport.html')
def visitorReport(theRequest):
    myCountryStats = Visit.helpers.countryStats()

    #render_to_response is done by the renderWithContext decorator
    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myScores': myCountryStats,
        'myCurrentMonth': datetime.date.today()
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitorMonthlyReport.html')
def visitorMonthlyReport(theRequest, theYear, theMonth):
    #construct date object
    if not(theYear and theMonth):
        myDate = datetime.date.today()
    else:
        try:
            myDate = datetime.date(int(theYear), int(theMonth), 1)
        except:
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())

    myCountryStats = Visit.helpers.monthlyReport(myDate)

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myScores': myCountryStats,
        'myCurrentDate': myDate,
        'myPrevDate': myDate - datetime.timedelta(days=1),
        'myNextDate': myDate + datetime.timedelta(days=31),
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitors.html')
def visitorList(theRequest):
    myRecords = Visit.objects.all().order_by('-visit_date')
    # Paginate the results
    if 'pdf' in theRequest.GET:
        myPageSize = myRecords.count()
    else:
        myPageSize = 100
    myPaginator = Paginator(myRecords, myPageSize)
    # Make sure page request is an int. If not, deliver first page.
    try:
        myPage = int(theRequest.GET.get('page', '1'))
    except ValueError:
        myPage = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        myRecords = myPaginator.page(myPage)
    except (EmptyPage, InvalidPage):
        myRecords = myPaginator.page(myPaginator.num_pages)

    #render_to_response is done by the renderWithContext decorator
    return ({'myRecords': myRecords})


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('mySearches.html')
def searchHistory(theRequest):
    mySearchHistory = (
        Search.objects.filter(user=theRequest.user.id)
        .filter(deleted=False)
        .order_by('-search_date'))
    return ({'mySearches': mySearchHistory})


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('recentSearches.html')
def recentSearches(theRequest):
    mySearchHistory = (
        Search.objects.filter(deleted=False).order_by('-search_date'))
    if len(mySearchHistory) > 50:
        mySearchHistory = mySearchHistory[0:50]
    return ({
        'mySearches': mySearchHistory,
        'myCurrentMonth': datetime.date.today()})


#monthly search report by user ip_position
@staff_member_required
@renderWithContext('searchMonthlyReport.html')
def searchMonthlyReport(theRequest, theYear, theMonth):
    #construct date object
    if not(theYear and theMonth):
        myDate = datetime.date.today()
    else:
        try:
            myDate = datetime.date(int(theYear), int(theMonth), 1)
        except:
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())

    myCountryStats = Search.helpers.monthlyReport(theDate=myDate)

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myScores': myCountryStats,
        'myCurrentDate': myDate,
        'myPrevDate': myDate - datetime.timedelta(days=1),
        'myNextDate': myDate + datetime.timedelta(days=31),
    })


#monthly search report by user ip_position
@staff_member_required
@renderWithContext('searchMonthlyReportAOI.html')
def searchMonthlyReportAOI(theRequest, theYear, theMonth):
    #construct date object
    if not(theYear and theMonth):
        myDate = datetime.date.today()
    else:
        try:
            myDate = datetime.date(int(theYear), int(theMonth), 1)
        except:
            logger.error('Date arguments cannot be parsed')
            logger.info(traceback.format_exc())

    myCountryStats = Search.helpers.monthlyReportAOI(theDate=myDate)

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myScores': myCountryStats,
        'myCurrentDate': myDate,
        'myPrevDate': myDate - datetime.timedelta(days=1),
        'myNextDate': myDate + datetime.timedelta(days=31),
    })


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('dataSummaryTable.html')
def dataSummaryTable(theRequest):
    """
    Summary of available records
    """
    myResultSet = (
        SatelliteInstrumentGroup.objects
        .annotate(id__count=Count(
            'satelliteinstrument__opticalproductprofile__opticalproduct'))
        .order_by('satellite__name'))

    myTotal = 0
    for myResult in myResultSet:
        myTotal += myResult.id__count
    return ({'myResultSet': myResultSet, 'myTotal': myTotal})


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('sensorSummaryTable.html')
def sensorSummaryTable(theRequest, theSensorId):
    """
    Summary of tasking requests,orders etc for a given sensor
    """
    #
    # Note: don't use len() to count recs - its very inefficient
    #       use count() rather
    #
    mySensor = get_object_or_404(SatelliteInstrumentGroup, id=theSensorId)
    mySearchCount = Search.objects.all().count()
    mySearchForSensorCount = Search.objects.filter(
        satellite__satelliteinstrumentgroup=mySensor).count()
    myProductForSensorCount = None

    myProductForSensorCount = OpticalProduct.objects.filter(
        product_profile__satellite_instrument__satellite_instrument_group=mySensor).count()
    myProductTotalCount = GenericSensorProduct.objects.count()

    myRecords = SearchRecord.objects.filter(
        user__isnull=False).filter(order__isnull=False)
    myProductOrdersTotalCount = myRecords.count()
    myProductOrdersForSensorCount = (
        SearchRecord.objects.filter(user__isnull=False)
        .filter(order__isnull=False)
        .filter(product__genericimageryproduct__genericsensorproduct__opticalproduct__product_profile__satellite_instrument__satellite_instrument_group__exact=mySensor)
        .count())

    myResults = SortedDict()
    myResults['Searches for this sensor'] = mySearchForSensorCount
    myResults['Searches for all sensors'] = mySearchCount
    myResults['Total ordered products for this sensor'] = myProductOrdersForSensorCount
    myResults['Total ordered products for all sensors'] = myProductOrdersTotalCount
    myResults['Total products for this sensor'] = myProductForSensorCount
    myResults['Total products for all sensors'] = myProductTotalCount

    mySensorYearlyStats = mySensor.products_per_year()

    #define beginning year for yearly product summary
    myStartYear = 1981
    myCurrentYear = datetime.date.today().year
    # create a list of 'empty' records
    mySensorYearlyStatsAll = [
        {'year': myYear, 'count': 0}
        for myYear in range(myStartYear, myCurrentYear + 1)]

    # update records, replace with actual data
    for myIdx, myTmpYear in enumerate(mySensorYearlyStatsAll):
        for myDataYear in mySensorYearlyStats:
            if myDataYear.get('year') == myTmpYear.get('year'):
                mySensorYearlyStatsAll[myIdx] = myDataYear

    return ({
        'myResults': myResults, 'mySensor': mySensor,
        'mySensorYearyStats': sliceForDisplay(mySensorYearlyStatsAll)})


@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('dictionaryReport.html')
def dictionaryReport(theRequest):
    """
    Summary of mission, sensor, type and mode. Later we could add
    proc level too
    """

    myReport = (
        SatelliteInstrumentGroup.objects.all().select_related()
        .order_by('satellite__name')
    )

    return({"myResults": myReport})
