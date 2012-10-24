"""
SANSA-EO Catalogue - orders_view_viewOrderItems - Orders views
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
    SearchRecord
)


class OrdersViews_viewOrderItems_Tests(TestCase):
    """
    Tests orders.py viewOrderItems method/view
    """

    fixtures = [
        'test_user.json',
        'test_orderstatus.json',
        'test_orderstatushistory.json',
        'test_marketsector.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_viewOrderItems_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theOrderId': 'testtest'}, {'theOrderId': None},
            {'theOrderId': 3.14}, {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'viewOrderItems',
                kwargs=myKwargTest)

    def test_viewOrderItems_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('viewOrderItems', kwargs={'theOrderId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/vieworderitems/1/')

    def test_viewOrderItems_login_staff(self):
        """
        Test view if user is staff
        """
        myOrderId = 1
        myOrderObj = Order.objects.get(id=myOrderId)
        mySearchRecords = SearchRecord.objects.filter(
            order=myOrderObj).all()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewOrderItems', kwargs={'theOrderId': myOrderId}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], False)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(
            myResp.context['myBaseTemplate'], 'emptytemplate.html')

        # check used templates
        myExpTemplates = [
            'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_viewOrderItems_login_user_owned(self):
        """
        Test view if user is normal user and owns an object
        """
        myOrderId = 2
        myOrderObj = Order.objects.get(id=myOrderId)
        mySearchRecords = SearchRecord.objects.filter(
            order=myOrderObj).all()

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewOrderItems', kwargs={'theOrderId': myOrderId}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            len(myResp.context['myRecords']), len(mySearchRecords))
        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], False)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], True)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], False)
        self.assertEqual(
            myResp.context['myBaseTemplate'], 'emptytemplate.html')

        # check used templates
        myExpTemplates = 'cartContents.html'
        myUsedTemplates = myResp.template.name
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_viewOrderItems_login_user_notowned(self):
        """
        Test view if user is normal user and doesn't own an object
        """
        myOrderId = 1

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewOrderItems', kwargs={'theOrderId': myOrderId}))

        self.assertEqual(myResp.status_code, 404)

    def test_viewOrderItems_login_staff_invalid_order(self):
        """
        Test view if user is normal user and doesn't own an object
        """
        myOrderId = 13131

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewOrderItems', kwargs={'theOrderId': myOrderId}))

        self.assertEqual(myResp.status_code, 404)
