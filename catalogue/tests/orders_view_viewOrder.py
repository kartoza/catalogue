"""
SANSA-EO Catalogue - orders_view_viewOrder - Orders views
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
    SearchRecord,
    OrderStatusHistory,
)

from catalogue.forms import OrderStatusHistoryForm

from catalogue.views.orders import coverageForOrder


class OrdersViews_viewOrder_Tests(TestCase):
    """
    Tests orders.py viewOrder method/view
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
        'test_marketsector.json',
        'test_deliverymethod.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_viewOrder_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'viewOrder',
                kwargs=myKwargTest)

    def test_viewOrder_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/vieworder/1/')

    def test_viewOrder_login_staff(self):
        """
        Test view if user is staff
        """

        myOrderPk = 1
        myOrderObj = Order.objects.get(pk=myOrderPk)
        mySearchRecords = SearchRecord.objects.all().filter(order=myOrderObj)
        myFormObj = OrderStatusHistoryForm()
        myHistoryObj = OrderStatusHistory.objects.all().filter(
            order=myOrderObj)
        myCoverageObj = coverageForOrder(myOrderObj, mySearchRecords)

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': myOrderPk}))

        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myOrder'], myOrderObj)
        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(myResp.context['myDownloadOrderFlag'], True)
        self.assertEqual(
            myResp.context['myForm'].__class__, myFormObj.__class__)
        self.assertEqual(len(myResp.context['myHistory']), len(myHistoryObj))
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')
        self.assertEqual(myResp.context['myCoverage'], myCoverageObj)

        # check used templates
        myExpTemplates = [
            'orderPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'order.html',
            u'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html', u'orderStatusHistory.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_viewOrder_login_user(self):
        """
        Test view if user is normal user
        """

        myOrderPk = 2
        myOrderObj = Order.objects.get(pk=myOrderPk)
        mySearchRecords = SearchRecord.objects.all().filter(order=myOrderObj)
        myFormObj = None
        myHistoryObj = OrderStatusHistory.objects.all().filter(
            order=myOrderObj)
        myCoverageObj = coverageForOrder(myOrderObj, mySearchRecords)

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': myOrderPk}))

        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myOrder'], myOrderObj)
        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(myResp.context['myDownloadOrderFlag'], True)
        self.assertEqual(
            myResp.context['myForm'].__class__, myFormObj.__class__)
        self.assertEqual(len(myResp.context['myHistory']), len(myHistoryObj))
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')
        self.assertEqual(myResp.context['myCoverage'], myCoverageObj)

        # check used templates
        myExpTemplates = [
            'orderPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'order.html',
            u'cartContents.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_viewOrder_login_user_notowned(self):
        """
        Test view if user is normal user, not owned order
        """

        myOrderPk = 1

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': myOrderPk}))

        self.assertEqual(myResp.status_code, 404)

    def test_showCartContents_login_staff_ajax(self):
        """
        Test view if user is staff, and request is ajax
        """
        myOrderPk = 2
        myOrderObj = Order.objects.get(pk=myOrderPk)
        mySearchRecords = SearchRecord.objects.all().filter(order=myOrderObj)
        myFormObj = OrderStatusHistoryForm()
        myHistoryObj = OrderStatusHistory.objects.all().filter(
            order=myOrderObj)
        myCoverageObj = coverageForOrder(myOrderObj, mySearchRecords)

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewOrder', kwargs={'theId': myOrderPk}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)

        # check response object
        self.assertEqual(myResp.context['myOrder'], myOrderObj)
        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myRemoveFlag'], False)
        self.assertEqual(myResp.context['myThumbFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myCartFlag'], False)
        self.assertEqual(myResp.context['myPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(myResp.context['myDownloadOrderFlag'], True)
        self.assertEqual(
            myResp.context['myForm'].__class__, myFormObj.__class__)
        self.assertEqual(len(myResp.context['myHistory']), len(myHistoryObj))
        self.assertEqual(myResp.context['myCartTitle'], 'Product List')
        self.assertEqual(myResp.context['myCoverage'], myCoverageObj)

        # check used templates
        myExpTemplates = [
            'orderPageAjax.html', u'emptytemplate.html', u'order.html',
            u'cartContents.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)
