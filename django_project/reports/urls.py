from django.conf.urls import url

from .api import DataSummaryApiView
from .views import (
    search_history,
    recent_searches,
    search_monthly_report,
    search_monthly_report_aoi,
    visitor_list,
    visitor_report,
    visitor_monthly_report,
    data_summary_table,
    dictionary_report,
    sensor_summary_table,
    sensor_fact_sheet
)

urlpatterns = [
    url(r'^search-history/$', search_history, name='search-history'),
    url(r'^recentsearches/$', recent_searches, name='recentSearches'),
    url(r'^searchmonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        search_monthly_report, name='searchMonthlyReport'
        ),
    url(r'^searchmonthlyreportaoi/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        search_monthly_report_aoi, name='searchMonthlyReportAOI'
        ),
    url(r'^visitorlist/$', visitor_list, name='visitorList'),
    url(r'^visitorreport/$', visitor_report, name='visitorReport'),
    url(r'^visitormonthlyreport/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        visitor_monthly_report, name='visitorMonthlyReport'
        ),
    url(r'^data-summary-table/$', data_summary_table, name='data-summary-table'),
    url(r'^dictionaryReport/$', dictionary_report, name='dictionaryReport'),
    url(r'^sensor-fact-sheet/(?P<sat_abbr>[\w-]+)/(?P<instrument_type>[\w-]+)/$',
        sensor_fact_sheet, name='fact-sheet'),
    url(r'^data-summary/$',
        DataSummaryApiView.as_view(), name='data-summary')
]
