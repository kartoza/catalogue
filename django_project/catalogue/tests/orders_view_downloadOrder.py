"""
SANSA-EO Catalogue - orders_view_downloadOrder - Orders views
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


class OrdersViews_downloadOrder_Tests(TestCase):
    """
    Tests orders.py downloadOrder method/view
    """
    fixtures = [
        'test_user.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_order.json',
        'test_taskingrequest.json',
        'test_processinglevel.json',
        'test_projection.json',
        'test_datum.json',
        'test_resamplingmethod.json',
        'test_fileformat.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadOrder_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadOrder',
                kwargs=myKwargTest)

    def test_downloadOrder_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadOrder', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/signin/?next=/downloadorder/1/'))

    def test_downloadOrder_login_staff_shp(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadOrder', kwargs={'theId': 1}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=products_for_order_1.zip')

    def test_downloadOrder_login_staff_kml(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadOrder', kwargs={'theId': 1}),
            {'kml': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kml+xml')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=products_for_order_1.kml')

    def test_downloadOrder_login_staff_kmz(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadOrder', kwargs={'theId': 1}),
            {'kmz': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kmz')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=products_for_order_1.kmz')

    def test_downloadOrder_login_staff_unkformat(self):
        """
        Test view if staff user is logged in
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadOrder', kwargs={'theId': 1}),
            {'unkformat': ''})

        self.assertEqual(myResp.status_code, 404)
