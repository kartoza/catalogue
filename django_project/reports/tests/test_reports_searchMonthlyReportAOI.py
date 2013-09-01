"""
SANSA-EO Catalogue - reports_searchMonthlyReportAOI - Reports views
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
__version__ = '0.2'
__date__ = '20/08/2013'
__copyright__ = 'South African National Space Agency'

import datetime
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from search.tests.model_factories import SearchF
from catalogue.tests.model_factories import WorldBordersF


class ReportsViews_searchMonthlyReportAOI_Tests(TestCase):
    """
    Tests reports.py searchMonthlyReportAOI method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_myReports_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'searchMonthlyReportAOI',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        myClient = Client()
        myResp = myClient.get(
            reverse('searchMonthlyReportAOI',
                    kwargs={'theYear': '2010', 'theMonth': '7'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/searchmonthlyreportaoi/2010/7/')

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('searchMonthlyReportAOI',
                    kwargs={'theYear': '2010', 'theMonth': '7'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/searchmonthlyreportaoi/2010/7/')

    def test_myReports_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        WorldBordersF.create()

        SearchF.create(**{
            'user': myUser,
            'geometry': 'POLYGON((1 -1, 1 1, -1 1, -1 -1, 1 -1))'
        })

        today = datetime.date.today()
        myDate = datetime.date(today.year, today.month, 1)

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('searchMonthlyReportAOI',
                    kwargs={'theYear': myDate.year, 'theMonth': myDate.month}))
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            myResp.context['myGraphLabel'], ({'Country': 'country'}))
        self.assertEqual(
            len(myResp.context['myScores']), 1)
        self.assertEqual(
            myResp.context['myCurrentDate'], myDate)
        self.assertEqual(
            myResp.context['myPrevDate'],
            myDate - datetime.timedelta(days=1))
        self.assertEqual(
            myResp.context['myNextDate'],
            myDate + datetime.timedelta(days=31))
        # check used templates
        myExpTemplates = [
            'searchMonthlyReportAOI.html', u'base.html',
            u'menu.html', u'useraccounts/menu_content.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
