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
    url(r'^recent-searches/$', recent_searches, name='recent-searches'),
    url(r'^search-monthly-report/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        search_monthly_report, name='search-monthly-report'
        ),
    url(r'^search-monthly-report-aoi/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        search_monthly_report_aoi, name='search-monthly-report-aoi'
        ),
    url(r'^visitor-list/$', visitor_list, name='visitor-list'),
    url(r'^visitor-report/$', visitor_report, name='visitor-report'),
    url(r'^visitor-monthly-report/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        visitor_monthly_report, name='visitor-monthly-report'
        ),
    url(r'^data-summary-table/$', data_summary_table, name='data-summary-table'),
    url(r'^dictionary-report/$', dictionary_report, name='dictionary-report'),
    url(r'^sensor-fact-sheet/(?P<sat_abbr>[\w-]+)/(?P<instrument_type>[\w-]+)/$',
        sensor_fact_sheet, name='fact-sheet'),
    url(r'^data-summary/$',
        DataSummaryApiView.as_view(), name='data-summary')
]
