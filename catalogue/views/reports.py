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

# Django helpers for forming html pages
from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
# from django.contrib.gis.shortcuts import render_to_kml, render_to_kmz
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# from django.template import RequestContext
# from django.forms.util import ErrorList
#for sorted dictionaries, useful when rendering templates
from django.utils.datastructures import SortedDict

from django.contrib.auth.models import User

# for aggregate queries
from django.db.models import Count  # for aggregate queries

# Models and forms for our app
from catalogue.models import (
    Visit,
    Search,
    SearchRecord,
    Mission,
    MissionSensor,
    TaskingRequest,
    GenericSensorProduct,
    RadarProduct,
    OpticalProduct,
    SensorType,
    AcquisitionMode)
from catalogue.renderDecorator import renderWithContext

from acscatalogue.models import (
    SegmentCommon,)


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
    myQuerySet = Visit()
    myCountryStats = myQuerySet.customSQL("""
    SELECT LOWER(country), COUNT(*) AS count, (SELECT COUNT(*)
    FROM catalogue_visit) AS total
    FROM catalogue_visit
    GROUP BY LOWER(country)
    ORDER BY count DESC;""", ['country', 'count', 'total'])

    myMaximum = 1
    myScores = []
    for myRec in myCountryStats:
        myValue = myRec['count']
        myTotal = myRec['total']
        myPercent = (myValue / myTotal) * 100
        myScores.append({
            'country': myRec['country'], 'count': myRec['count'],
            'total': myRec['total'], 'percent': myPercent})
    myTopCountries = myScores[0:10]
    #by_date = query_set.customSQL("""
    #SELECT EXTRACT( year FROM added_date ) AS year, MIN( to_char(
    #   added_date, 'Mon' ) ), COUNT( * ) FROM users_qgisuser
    #GROUP BY EXTRACT( year FROM added_date ), EXTRACT(month FROM added_date)
    #ORDER BY EXTRACT( year FROM added_date );""", ['year', 'month', 'count'])

    #render_to_response is done by the renderWithContext decorator
    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myTopCountries': myTopCountries,
        'myScores': myScores,
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
            logging.error('Date arguments cannot be parsed')
            logging.info(traceback.format_exc())

    myQuerySet = Visit()
    myCountryStats = myQuerySet.customSQL("""
    SELECT LOWER(country),count(*) as count, DATE_TRUNC('month',
    visit_date) as month
    FROM catalogue_visit
    WHERE visit_date BETWEEN to_date(%(date)s,'MM-YYYY')
        AND to_date(%(date)s,'MM-YYYY')+ interval '1 month'
    GROUP BY LOWER(country),DATE_TRUNC('month',visit_date)
    ORDER BY month DESC""", ['country', 'count', 'month'], {
        'date': myDate.strftime('%m-%Y')
    })
    myMaximum = 1
    myScores = []
    for myRec in myCountryStats:
        myScores.append({
            'country': myRec['country'], 'count': myRec['count']})
    myTopCountries = myScores[0:10]

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myTopCountries': myTopCountries,
        'myScores': myScores,
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
            logging.error('Date arguments cannot be parsed')
            logging.info(traceback.format_exc())

    myQuerySet = Search()
    myCountryStats = myQuerySet.customSQL("""
    SELECT name,date_trunc('month',search_date) as date_of_search,
        count(*) as searches
    FROM (SELECT a.name, b.search_date FROM catalogue_worldborders a
        INNER JOIN catalogue_search b ON
        st_intersects(a.geometry,b.ip_position) OFFSET 0) ss
    WHERE search_date BETWEEN to_date(%(date)s,'MM-YYYY') AND
        to_date(%(date)s,'MM-YYYY') + interval '1 month'
    GROUP BY name,date_trunc('month',search_date)
    ORDER BY searches DESC""", [
        'country', 'month', 'count'], {'date': myDate.strftime('%m-%Y')})

    myScores = []
    for myRec in myCountryStats:
        myScores.append({
            'country': myRec['country'], 'count': myRec['count']})

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myScores': myScores,
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
            logging.error('Date arguments cannot be parsed')
            logging.info(traceback.format_exc())

    myQuerySet = Search()
    myCountryStats = myQuerySet.customSQL("""
    SELECT a.name, date_trunc('month',b.search_date) as date_of_search,
        count(*) as searches
    FROM catalogue_worldborders a INNER JOIN catalogue_search b
        ON st_intersects(a.geometry,b.geometry)
    WHERE search_date between to_date(%(date)s,'MM-YYYY') AND
        to_date(%(date)s,'MM-YYYY') + interval '1 month'
    GROUP BY  a.name,date_trunc('month',b.search_date)
    ORDER BY searches desc;""", [
        'country', 'month', 'count'], {'date': myDate.strftime('%m-%Y')})

    myScores = []
    for myRec in myCountryStats:
        myScores.append({'country': myRec['country'], 'count': myRec['count']})

    return ({
        'myGraphLabel': ({'Country': 'country'}),
        'myScores': myScores,
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
    #myResultSet = GenericProduct.objects.values("mission_sensor")
    # .annotate(Count("id")).order_by().aggregate(
    #    Min('product_acquisition_start'),Max('product_acquisition_end'))
    #ABP: changed to GenericSensorProduct
    #ABP: changed to MissionSensor
    myResultSet = (
        MissionSensor.objects
        .annotate(id__count=Count(
            'sensortype__acquisitionmode__genericsensorproduct'))
        .order_by('name'))

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
    mySensor = get_object_or_404(MissionSensor, id=theSensorId)
    myTaskingSensorCount = TaskingRequest.objects.filter(
        mission_sensor=mySensor).count()
    myTaskingTotalCount = TaskingRequest.objects.count()
    mySearchCount = Search.objects.all().count()
    mySearchForSensorCount = Search.objects.filter(sensors=mySensor).count()
    myProductForSensorCount = None
    if (mySensor.is_radar):
        myProductForSensorCount = RadarProduct.objects.filter(
            acquisition_mode__sensor_type__mission_sensor=mySensor).count()
    else:
        myProductForSensorCount = OpticalProduct.objects.filter(
            acquisition_mode__sensor_type__mission_sensor=mySensor).count()
    myProductTotalCount = GenericSensorProduct.objects.count()

    myRecords = SearchRecord.objects.filter(
        user__isnull=False).filter(order__isnull=False)
    myProductOrdersTotalCount = myRecords.count()
    myProductOrdersForSensorCount = (
        SearchRecord.objects.filter(user__isnull=False)
        .filter(order__isnull=False)
        .filter(product__genericimageryproduct__genericsensorproduct__acquisition_mode__sensor_type__mission_sensor__exact=mySensor)
        .count())

    myResults = SortedDict()
    myResults['Tasking requests for this sensor'] = myTaskingSensorCount
    myResults['Tasking requests all sensors'] = myTaskingTotalCount
    myResults['Searches for this sensor'] = mySearchForSensorCount
    myResults['Searches for all sensors'] = mySearchCount
    myResults['Total ordered products for this sensor'] = myProductOrdersForSensorCount
    myResults['Total ordered products for all sensors'] = myProductOrdersTotalCount
    myResults['Total products for this sensor'] = myProductForSensorCount
    myResults['Total products for all sensors'] = myProductTotalCount

    mySensorYearlyStats = Search().customSQL("""
    SELECT count(*) as count,
        extract(YEAR from catalogue_genericproduct.product_date)::int as year
    FROM
      public.catalogue_genericproduct,
      public.catalogue_genericimageryproduct,
      public.catalogue_genericsensorproduct,
      public.catalogue_acquisitionmode,
      public.catalogue_sensortype,
      public.catalogue_missionsensor
    WHERE
      catalogue_genericproduct.id =
        catalogue_genericimageryproduct.genericproduct_ptr_id AND
      catalogue_genericimageryproduct.genericproduct_ptr_id =
        catalogue_genericsensorproduct.genericimageryproduct_ptr_id AND
      catalogue_genericsensorproduct.acquisition_mode_id =
        catalogue_acquisitionmode.id AND
      catalogue_acquisitionmode.sensor_type_id = catalogue_sensortype.id AND
      catalogue_sensortype.mission_sensor_id = catalogue_missionsensor.id
      AND catalogue_missionsensor.id = %(sensor_id)s
    GROUP BY extract(YEAR from catalogue_genericproduct.product_date)
    -- order by year ASC, month ASC
    ORDER BY year ASC;""", ['count', 'year'], {'sensor_id': mySensor.pk})

    #define beginning year for yearly product summary
    myStartYear = 1981
    myCurrentYear = datetime.date.today().year
    # create a list of 'empty' records
    mySensorYearlyStatsAll = [
        {'year': myYear, 'count':0}
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
    Summary of mission, sensor, type and mode dictionaries. Later we could add
    proc level too
    """

    myReport = []
    myTypeReport = []
    myMissions = Mission.objects.all().order_by('name')
    for myMission in myMissions:
        mySensors = MissionSensor.objects.filter(
            mission=myMission).order_by('name')
        for mySensor in mySensors:
            myTypes = SensorType.objects.filter(
                mission_sensor=mySensor).order_by('name')
            for myType in myTypes:
                myModes = AcquisitionMode.objects.filter(
                    sensor_type=myType).order_by('name')
                myTypeRow = [myMission, mySensor, myType]
                myTypeReport.append(myTypeRow)
                for myMode in myModes:
                    myRow = [myMission, mySensor, myType, myMode]
                    myReport.append(myRow)

    return({"myTypeResults": myTypeReport, "myResults": myReport})
