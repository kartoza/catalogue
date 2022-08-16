"""
SANSA-EO Catalogue - shopping_cart_view_removeFromCart - Shopping cart
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
__version__ = '0.1'
__date__ = '15/10/2012'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from search.tests.model_factories import SearchRecordF
from .model_factories import OpticalProductF


class ShoppingCart_removeFromCart_Tests(TestCase):
    """
    Tests tasking.py removeFromCart method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_removeFromCart_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'removeFromCart',
                kwargs=myKwargTest)

    def test_removeFromCart_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('removeFromCart', kwargs={'theId': 5}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/removefromcart/5/')

    def test_removeFromCart_login_staff(self):
        """
        Test view if user is staff
        """

        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOProduct = OpticalProductF.create(**{
            'id': 1,
            'unique_product_id': 'XY1234'
        })

        SearchRecordF.create(**{
            'id': 1,
            'user': myUser,
            'order': None,
            'product': myOProduct
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('removeFromCart', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'text/plain')
        self.assertEqual(
            myResp.content,
            ('Successfully removed item from your basket')
        )

    def test_removeFromCart_login_staff_notowned(self):
        """
        Test view if user is staff, but doesn't own search record
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOProduct = OpticalProductF.create(**{
            'id': 1,
            'unique_product_id': 'XY1234'
        })

        SearchRecordF.create(**{
            'id': 1,
            'order': None,
            'product': myOProduct
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('removeFromCart', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'text/plain')
        self.assertEqual(
            myResp.content,
            ('You don\'t own this record so you can not delete it!'))

    def test_removeFromCart_login_staff_owned_ordered(self):
        """
        Test view if user is staff, owns searchrecord, but search record
        already is ordered

        WARNING: is it allowed to delete ordered records ?
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myOProduct = OpticalProductF.create(**{
            'id': 1,
            'unique_product_id': 'XY1234'
        })

        SearchRecordF.create(**{
            'id': 1,
            'user': myUser,
            'product': myOProduct
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('removeFromCart', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'text/plain')
        self.assertEqual(
            myResp.content,
            ('Successfully removed item from your basket'))
