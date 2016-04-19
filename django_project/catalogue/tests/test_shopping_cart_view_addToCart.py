"""
SANSA-EO Catalogue - shopping_cart_view_addToCart - Shopping cart
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
from search.tests.model_factories import SearchRecordF
from .model_factories import OpticalProductF


class ShoppingCart_addToCart_Tests(TestCase):
    """
    Tests tasking.py addToCart method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_addToCart_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'addToCart',
                kwargs=myKwargTest)

    def test_addToCart_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('addToCart', kwargs={'theId': 1934163}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/addtocart/1934163/')

    def test_addToCart_login_staff(self):
        """
        Test view if user is staff
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OpticalProductF.create(**{
            'id': 1,
            'original_product_id': 'XY1234'
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('addToCart', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'text/html')
        self.assertEqual(
            myResp.content, ('Successfully added XY1234 to your myCart')
        )

    def test_addToCart_login_staff_ajax(self):
        """
        Test view if the request is an AJAX request
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        OpticalProductF.create(**{
            'id': 1,
            'unique_product_id': 'XY1234'
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('addToCart', kwargs={'theId': 1}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/json')
        self.assertEqual(
            myResp.content, '{"Status": "Added", "Item": "1"}')

    def test_addToCart_login_staff_duplicate_item(self):
        """
        Test view when trying to add duplicate item to cart
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
        myResp = myClient.get(reverse('addToCart', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/javascript')
        self.assertEqual(
            myResp.content, 'alert("Item already exists in your cart!");')
