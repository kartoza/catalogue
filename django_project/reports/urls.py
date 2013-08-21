from django.conf.urls import patterns, url

from .views import (
    searchHistory,
    recentSearches,
    searchMonthlyReport,
    searchMonthlyReportAOI,
    visitorList,
    visitorReport,
    visitorMonthlyReport,
    dataSummaryTable,
    dictionaryReport,
    sensorSummaryTable,
    renderVisitorListPDF
)


urlpatterns = patterns(
    '',
    url(r'^mysearches/$', searchHistory, name='searchHistory'),
    url(r'^recentsearches/$', recentSearches, name='recentSearches'),
    url(r'^searchmonthlyreport/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$',
        searchMonthlyReport, name='searchMonthlyReport'
        ),
    url(r'^searchmonthlyreportaoi/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$',
        searchMonthlyReportAOI, name='searchMonthlyReportAOI'
        ),
    url(r'^visitorlist/$', visitorList, name='visitorList'),
    url(r'^visitorreport/$', visitorReport, name='visitorReport'),
    url(r'^visitormonthlyreport/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$',
        visitorMonthlyReport, name='visitorMonthlyReport'
        ),
    url(r'^dataSummaryTable/$', dataSummaryTable, name='dataSummaryTable'),
    url(r'^dictionaryReport/$', dictionaryReport, name='dictionaryReport'),
    url(r'^sensorSummaryTable/(?P<theSensorId>[0-9]+)/$',
        sensorSummaryTable, name='sensorSummaryTable'
        ),

    # George's URLs
    url(r'^renderVisitorListPDF/$', renderVisitorListPDF,
        name='visitorListPDF'),
)
