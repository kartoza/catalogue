"""
SANSA-EO Catalogue - orders_view_orderMonthlyReport - Orders views
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
__date__ = '19/08/2013'
__copyright__ = 'South African National Space Agency'

from datetime import date, timedelta

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from .model_factories import OrderF


class OrdersViews_orderMonthlyReport_Tests(TestCase):
    """
    Tests orders.py orderMonthlyReport method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_orderMonthlyReport_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {'year': '', 'month': ''},
            {'year': '12345', 'month': '5'},
            {'year': '12345', 'month': '5'},
            {'year': 'abcd', 'month': 'ab'},
            {'testarg1': '1234', 'thearg2': '5'}
        ]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'orderMonthlyReport',
                kwargs=myKwargTest)

    def test_orderMonthlyReport_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={'year': 2012, 'month': 6}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            ('/accounts/signin/?next=/ordermonthlyreport/'
                '2012/6/'))

    def test_orderMonthlyReport_login_staff(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        today = date.today()
        myTestDate = date(today.year, today.month, 1)
        OrderF.create(**{
            'id': 1
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={
                    'year': myTestDate.year,
                    'month': myTestDate.month}
            )
        )
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myCurrentDate'], myTestDate)

        self.assertEqual(
            myResp.context['myPrevDate'],
            myTestDate - timedelta(days=1))

        self.assertEqual(
            myResp.context['myNextDate'],
            myTestDate + timedelta(days=31))

        # check used templates
        myExpTemplates = [
            'orderMonthlyReport.html', u'base.html',
            u'pipeline/css.html', u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html', u'django_tables2/custom-table.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(len(myResp.context['myRecords']), 1)

    def test_orderMonthlyReport_login_user(self):
        """
        Test view if normal user is logged in
        """
        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        today = date.today()
        myTestDate = date(today.year, today.month, 1)
        OrderF.create(**{
            'id': 1,
            'user': myUser
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={
                    'year': myTestDate.year,
                    'month': myTestDate.month}
            )
        )
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myCurrentDate'], myTestDate)

        self.assertEqual(
            myResp.context['myPrevDate'],
            myTestDate - timedelta(days=1))

        self.assertEqual(
            myResp.context['myNextDate'],
            myTestDate + timedelta(days=31))

        # check used templates
        myExpTemplates = [
            'orderMonthlyReport.html', u'base.html',
            u'pipeline/css.html', u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html', u'django_tables2/custom-table.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(len(myResp.context['myRecords']), 1)

    def test_orderMonthlyReport_login_staff_pdf(self):
        """
        Test view if staff user is logged in, requesting pdf
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        today = date.today()
        myTestDate = date(today.year, today.month, 1)
        OrderF.create(**{
            'id': 1
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={
                    'year': myTestDate.year,
                    'month': myTestDate.month}
            ),
            {'pdf': ''}
        )
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myCurrentDate'], myTestDate)

        self.assertEqual(
            myResp.context['myPrevDate'],
            myTestDate - timedelta(days=1))

        self.assertEqual(
            myResp.context['myNextDate'],
            myTestDate + timedelta(days=31))

        # check used templates
        myExpTemplates = None

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertContains(myUsedTemplates, myExpTemplates)

        self.assertEqual(len(myResp.context['myRecords']), 1)
