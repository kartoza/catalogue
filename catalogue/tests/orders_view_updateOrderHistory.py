"""
SANSA-EO Catalogue - orders_view_updateOrderHistory - Orders views
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
__date__ = '23/10/2012'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.models import (
    Order,
    OrderStatusHistory,
    SearchRecord
)

from catalogue.forms import OrderStatusHistoryForm


class OrdersViews_updateOrderHistory_Tests(TestCase):
    """
    Tests orders.py updateOrderHistory method/view
    """

    fixtures = [
        'test_mission.json',
        'test_missionsensor.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_user.json',
        'test_orderstatus.json',
        'test_orderstatushistory.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_updateOrderHistory_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'updateOrderHistory',
                kwargs=myKwargTest)

    def test_updateOrderHistory_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('updateOrderHistory', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/updateorderhistory/')

    def test_updateOrderHistory_login_staff(self):
        """
        Test view if user is staff
        """

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('updateOrderHistory', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.content, 'You can only access this view from a form POST')

        self.assertEqual(myResp.context, None)

    def test_updateOrderHistory_login_user(self):
        """
        Test view if user is normal user
        """

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('updateOrderHistory', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.content, 'Access denied')

        self.assertEqual(myResp.context, None)

    def test_updateOrderHistory_login_staff_post(self):
        """
        Test view if user is staff, and has valid post
        """

        myOrderId = 1
        # get initial objects
        myOrderObj = Order.objects.get(pk=myOrderId)
        mySearchRecords = SearchRecord.objects.all().filter(order=myOrderObj)
        myFormObj = OrderStatusHistoryForm()
        myHistoryObj = OrderStatusHistory.objects.all().filter(
            order=myOrderObj)
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [u'4'], u'notes': [u'simple notes'],
            u'order': [myOrderId]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['myOrder'], myOrderObj)
        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], True)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], True)

        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)

        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(
            myResp.context['myForm'].__class__, myFormObj.__class__)
        self.assertEqual(len(myResp.context['myHistory']), len(myHistoryObj))
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')

        # check used templates
        myExpTemplates = [
            'mail/order.txt', u'mail/base.txt', 'mail/order.html',
            u'mail/base.html', 'orderPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'order.html',
            u'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html', u'orderStatusHistory.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_updateOrderHistory_login_staff_post_ajax(self):
        """
        Test view if user is staff, and has valid post
        """

        myOrderId = 1
        # get initial objects
        myOrderObj = Order.objects.get(pk=myOrderId)
        mySearchRecords = SearchRecord.objects.all().filter(order=myOrderObj)
        myFormObj = OrderStatusHistoryForm()
        myHistoryObj = OrderStatusHistory.objects.all().filter(
            order=myOrderObj)
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [u'4'], u'notes': [u'simple notes'],
            u'order': [myOrderId]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['myOrder'], myOrderObj)
        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], True)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], True)

        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)

        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(
            myResp.context['myForm'].__class__, myFormObj.__class__)
        self.assertEqual(len(myResp.context['myHistory']), len(myHistoryObj))
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')

        # check used templates
        myExpTemplates = [
            'mail/order.txt', u'mail/base.txt', 'mail/order.html',
            u'mail/base.html', 'orderStatusHistory.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_updateOrderHistory_login_staff_post_invalid_order(self):
        """
        Test view if user is staff, and has invalid post (mismatched order)
        """

        myOrderId = 1331
        # get initial objects
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [u'4'], u'notes': [u'simple notes'],
            u'order': [myOrderId]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 404)

    def test_updateOrderHistory_login_staff_post_invalid_orderstatus(self):
        """
        Test view if user is staff, and has invalid post (mismatched
            orderstatus)
        """

        myOrderId = 1
        myOrderStatus = 1331
        # get initial objects
        # create the request
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myPostData = {
            u'new_order_status': [myOrderStatus], u'notes': [u'simple notes'],
            u'order': [myOrderId]
        }
        myResp = myClient.post(
            reverse('updateOrderHistory', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 404)
