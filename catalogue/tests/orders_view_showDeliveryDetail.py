"""
SANSA-EO Catalogue - orders_view_showDeliveryDetail - Orders views
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

from catalogue.models import DeliveryDetail


class OrdersViews_showDeliveryDetail_Tests(TestCase):
    """
    Tests orders.py showDeliveryDetail method/view
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
        'test_deliverydetail.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_showDeliveryDetail_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theReferenceId': 'testtest'}, {'theReferenceId': None},
            {'theReferenceId': 3.14}, {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showDeliveryDetail',
                kwargs=myKwargTest)

    def test_showDeliveryDetail_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('showDeliveryDetail', kwargs={'theReferenceId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/showdeliverydetail/1/')

    def test_showDeliveryDetail_login_staff(self):
        """
        Test view if user is staff
        """
        myReferenceId = 1
        myDeliveryDetailObj = DeliveryDetail.objects.filter(
            pk__exact=myReferenceId).get()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'showDeliveryDetail',
                kwargs={'theReferenceId': myReferenceId}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['myDeliveryDetail'],
            myDeliveryDetailObj)

        # check used templates
        myExpTemplates = 'deliveryDetail.html'
        myUsedTemplates = myResp.template.name

        self.assertEqual(myUsedTemplates, myExpTemplates)