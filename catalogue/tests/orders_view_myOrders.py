"""
SANSA-EO Catalogue - orders_view_myOrders - Orders views
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

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.models import Order


class OrdersViews_myOrders_Tests(TestCase):
    """
    Tests orders.py myOrders method/view
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

    def test_myOrders_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'myOrders',
                kwargs=myKwargTest)

    def test_myOrders_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('myOrders', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/myorders/')

    def test_myOrders_login_user(self):
        """
        Test view if user is logged in
        """
        # get initial counts
        myOrderCount = len(Order.base_objects.filter(
            user__username='timlinux').order_by('-order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myOrders', kwargs={}))
        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(
            myResp.context['myUrl'], 'myorders')

        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), myOrderCount)

    def test_myOrders_login_user_page_param_existant(self):
        """
        Test view if user is logged in, specifying page param
        """

        myOrderCount = len(Order.base_objects.filter(
            user__username='timlinux').order_by('-order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myOrders', kwargs={}),
            {'page': '1'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        # check response object
        self.assertEqual(
            myResp.context['myUrl'], 'myorders')

        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), myOrderCount)

    def test_myOrders_login_user_page_param_nonexistant(self):
        """
        Test view if user is logged in, specifying page that does not exist
        View will default to page 1
        """
        myOrderCount = len(Order.base_objects.filter(
            user__username='timlinux').order_by('-order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myOrders', kwargs={}),
            {'page': '1000'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        # check response object
        self.assertEqual(
            myResp.context['myUrl'], 'myorders')

        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), myOrderCount)

    def test_myOrders_login_page_param_invalid_input(self):
        """
        Test view if user is logged in, specifying invalid page parameter
        View will default to page 1
        """
        myOrderCount = len(Order.base_objects.filter(
            user__username='timlinux').order_by('-order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('myOrders', kwargs={}),
            {'page': 'this is a new page!'})

        self.assertEqual(myResp.status_code, 200)
        # check response object
        self.assertEqual(
            myResp.context['myUrl'], 'myorders')

        # check used templates
        myExpTemplates = [
            'orderListPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'orderList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), myOrderCount)

    def test_myOrders_pdf_pageSize(self):
        """
        Test view if pdf is requested
        """
        myOrderCount = len(Order.base_objects.filter(
            user__username='timlinux').order_by('-order_date').all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myResp = myClient.get(
            reverse('myOrders', kwargs={}),
            {'pdf': ''})

        self.assertEqual(myResp.status_code, 200)
        # check response object
        self.assertEqual(
            myResp.context['myUrl'], 'myorders')

        # check used templates
        myExpTemplates = ['pdf/orderListPage.html', u'pdfpage.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(
            len(myResp.context['myRecords'].object_list), myOrderCount)

        self.assertEqual(myResp['content-type'], 'application/pdf')
        self.assertEqual(
            myResp['content-disposition'], 'attachment; filename=report.pdf')
