"""
SANSA-EO Catalogue - reports_visitorMonthlyReport - Reports views
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
from catalogue.tests.model_factories import VisitF


class ReportsViews_visitorMonthlyReport_Tests(TestCase):
    """
    Tests reports.py visitorMonthlyReport method/view
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
                NoReverseMatch, reverse, 'visitorMonthlyReport',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'visitorMonthlyReport',
                kwargs={'year': '2010', 'month': '11'}))
        self.assertEqual(myResp.status_code, 302)

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'visitorMonthlyReport',
                kwargs={'year': '2010', 'month': '11'}))
        self.assertEqual(myResp.status_code, 302)

    def test_myReports_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        VisitF.create()

        today = datetime.date.today()
        myDate = datetime.date(today.year, today.month, 1)

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorMonthlyReport',
                kwargs={'year': myDate.year, 'month': myDate.month}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['myGraphLabel'], ({'Country': 'country'}))
        self.assertEqual(
            len(myResp.context['myScores']), 1)
        self.assertEqual(
            myResp.context['myCurrentDate'], myDate)
        self.assertEqual(
            myResp.context['myPrevDate'], myDate - datetime.timedelta(days=1))
        self.assertEqual(
            myResp.context['myNextDate'], myDate + datetime.timedelta(days=31))

