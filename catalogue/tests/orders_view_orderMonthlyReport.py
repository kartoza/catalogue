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
__version__ = '0.1'
__date__ = '19/10/2012'
__copyright__ = 'South African National Space Agency'

from datetime import date, timedelta

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.models import Order


class OrdersViews_orderMonthlyReport_Tests(TestCase):
    """
    Tests orders.py orderMonthlyReport method/view
    """
    fixtures = [
        'test_user.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_order.json',
        'test_taskingrequest.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_orderMonthlyReport_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {'theyear':'', 'themonth':''}, {'theyear':'12345', 'themonth':'5'},
            {'theyear':'12345', 'themonth':'5'},
            {'theyear':'abcd', 'themonth':'ab'},
            {'testarg1':'1234', 'thearg2':'5'}
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
                kwargs={'theyear': 2012, 'themonth': 6}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            ('http://testserver/accounts/login/?next=/ordermonthlyreport/'
                '2012/6/'))

    def test_orderMonthlyReport_login_staff(self):
        """
        Test view if staff user is logged in
        """
        # get initial counts
        myTestDate = date(2012, 6, 1)
        myOrderCount = len(
            Order.base_objects.filter(
                order_date__month=myTestDate.month)
            .filter(
                order_date__year=myTestDate.year)
            .order_by('order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={
                    'theyear': myTestDate.year,
                    'themonth': myTestDate.month}
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
            'orderMonthlyReport.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords']), myOrderCount)

    def test_orderMonthlyReport_login_user(self):
        """
        Test view if normal user is logged in
        """
        # get initial counts
        myTestDate = date(2012, 6, 1)
        myOrderCount = len(
            Order.base_objects.filter(
                order_date__month=myTestDate.month)
            .filter(
                order_date__year=myTestDate.year)
            .filter(user__username='pompies')
            .order_by('order_date').all())

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={
                    'theyear': myTestDate.year,
                    'themonth': myTestDate.month}
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
            'orderMonthlyReport.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords']), myOrderCount)

    def test_orderMonthlyReport_login_staff_pdf(self):
        """
        Test view if staff user is logged in, requesting pdf
        """
        # get initial counts
        myTestDate = date(2012, 6, 1)
        myOrderCount = len(
            Order.base_objects.filter(
                order_date__month=myTestDate.month)
            .filter(
                order_date__year=myTestDate.year)
            .order_by('order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'orderMonthlyReport',
                kwargs={
                    'theyear': myTestDate.year,
                    'themonth': myTestDate.month}
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
        myExpTemplates = ['pdf/orderMonthlyReport.html', u'pdfpage.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords']), myOrderCount)
