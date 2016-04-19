"""
SANSA-EO Catalogue - shopping_cart_view_downloadCart - Shopping cart
    views unittests

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
__date__ = '20/08/2013'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF


class ShoppingCart_downloadCart_Tests(TestCase):
    """
    Tests tasking.py downloadCart method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadCart_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'theId': 'testtest'}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadCart',
                kwargs=myKwargTest)

    def test_downloadCart_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadCart', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/downloadcart/')

    def test_downloadCart_login_staff_shp(self):
        """
        Test view if user is staff, requesing SHP file
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('downloadCart', kwargs={}), {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=timlinux-cart.zip')

    def test_downloadCart_login_staff_kml(self):
        """
        Test view if user is staff, requesing SHP file
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('downloadCart', kwargs={}), {'kml': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kml+xml')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=timlinux-cart.kml')

    def test_downloadCart_login_staff_kmz(self):
        """
        Test view if user is staff, requesing SHP file
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('downloadCart', kwargs={}), {'kmz': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kmz')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=timlinux-cart.kmz')

    def test_downloadCart_login_staff_invalidrequest(self):
        """
        Test view if staff user is logged in, but using invalid request params
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myTestParams = [{}, {'test': ''}, {'json': ''}]

        for myTestParam in myTestParams:
            myResp = myClient.get(
                reverse('downloadCart', kwargs={}),
                myTestParam)

            self.assertEqual(myResp.status_code, 404)
