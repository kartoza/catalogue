"""
SANSA-EO Catalogue - shopping_cart_view_downloadCartMetadata - Shopping cart
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


class ShoppingCart_downloadCartMetadata_Tests(TestCase):
    """
    Tests tasking.py downloadCartMetadata method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadCartMetadata_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'theId': 'testtest'}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadCartMetadata',
                kwargs=myKwargTest)

    def test_downloadCartMetadata_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadCartMetadata', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/downloadcartmetadata/')

    def test_downloadCartMetadata_login_staff(self):
        """
        Test view if user is staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('downloadCartMetadata', kwargs={}), {})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=SANSA-Cart-timlinux-Metadata.zip')

    def test_downloadCartMetadata_login_staff_html(self):
        """
        Test view if user is staff, html param
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadCartMetadata', kwargs={}),
            {'html': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=SANSA-Cart-timlinux-Metadata.zip')
