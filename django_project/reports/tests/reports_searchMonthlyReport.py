"""
SANSA-EO Catalogue - reports_searchMonthlyReport - Reports views
    unittests

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
__date__ = '22/11/2012'
__copyright__ = 'South African National Space Agency'

import datetime
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class ReportsViews_searchMonthlyReport_Tests(TestCase):
    """
    Tests reports.py visitorReport method/view
    """
    fixtures = [
        'test_user.json',
        'test_search.json',
        'test_searchdatarange.json',
        'test_searchrecord.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_order.json',
        #'test_taskingrequest.json',
        'test_processinglevel.json',
        'test_fileformat.json',
        'test_projection.json',
        'test_datum.json',
        'test_resamplingmethod.json',
        #'test_fileformat.json',
        'test_genericproduct.json',
        'test_institution.json',
        'test_license.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_worldborders.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_myReports_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'searchMonthlyReport',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('searchMonthlyReport',
                    kwargs={'theYear': '2010', 'theMonth': '7'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/searchmonthlyreport/2010/7/')

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('searchMonthlyReport',
                    kwargs={'theYear': '2010', 'theMonth': '7'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/searchmonthlyreport/2010/7/')

    def test_myReports_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('searchMonthlyReport',
                    kwargs={'theYear': '2010', 'theMonth': '7'}))
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            myResp.context['myGraphLabel'], ({'Country': 'country'}))
        self.assertEqual(
            len(myResp.context['myScores']), 1)
        self.assertEqual(
            myResp.context['myCurrentDate'], datetime.date(2010, 7, 1))
        self.assertEqual(
            myResp.context['myPrevDate'],
            datetime.date(2010, 7, 1) - datetime.timedelta(days=1))
        self.assertEqual(
            myResp.context['myNextDate'],
            datetime.date(2010, 7, 1) + datetime.timedelta(days=31))
        # check used templates
        myExpTemplates = [
            'searchMonthlyReport.html', u'base.html',
            u'menu.html', u'useraccounts/menu_content.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)