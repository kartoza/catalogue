"""
SANSA-EO Catalogue - orders_view_downloadOrderMetadata - Orders views
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


class OrdersViews_downloadOrderMetadata_Tests(TestCase):
    """
    Tests orders.py downloadOrderMetadata method/view
    """

    fixtures = [
        'test_user.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_order.json',
        'test_taskingrequest.json',
        'test_projection.json',
        'test_datum.json',
        'test_fileformat.json',
        'test_processinglevel.json',
        'test_resamplingmethod.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadOrderMetadata_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadOrderMetadata',
                kwargs=myKwargTest)

    def test_downloadOrderMetadata_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadOrderMetadata', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/downloadordermetadata/1/')

    def test_downloadOrderMetadata_login_staff(self):
        """
        Test view if user is staff
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadOrderMetadata', kwargs={'theId': 1}), {})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=SANSA-Order-1-Metadata.zip')

    def test_downloadOrderMetadata_login_staff_html(self):
        """
        Test view if user is staff, html param
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadOrderMetadata', kwargs={'theId': 1}),
            {'html': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=SANSA-Order-1-Metadata.zip')
