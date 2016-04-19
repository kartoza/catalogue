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
__version__ = '0.2'
__date__ = '19/10/2013'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from .model_factories import OrderF


class OrdersViews_downloadOrderMetadata_Tests(TestCase):
    """
    Tests orders.py downloadOrderMetadata method/view
    """

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
            '/accounts/signin/?next=/downloadordermetadata/1/')

    def test_downloadOrderMetadata_login_staff(self):
        """
        Test view if user is staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1})

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
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OrderF.create(**{'id': 1})

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
