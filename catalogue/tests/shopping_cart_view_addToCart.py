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
__version__ = '0.1'
__date__ = '15/10/2012'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.models import SearchRecord


class ShoppingCart_addToCart_Tests(TestCase):
    """
    Tests tasking.py addToCart method/view
    """

    fixtures = [
        'test_user.json',
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
        'test_marketsector.json',
        'test_deliverymethod.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

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
            {'testargs':1}]

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
            'http://testserver/accounts/login/?next=/addtocart/1934163/')

    def test_addToCart_login_staff(self):
        """
        Test view if user is staff
        """
        #get initial objects count
        mySearchRecord_count = len(SearchRecord.objects.all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('addToCart', kwargs={'theId': 1934163}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'text/html')
        self.assertEqual(
            myResp.content,
            ('Successfully added S1-_HRV_X--_S1C2_0120_00_0404_00_860619_08463'
                '2_1B--_ORBIT- to your myCart'))
        # check if new record count
        myNewSearchRecord_count = len(SearchRecord.objects.all())
        self.assertEqual(myNewSearchRecord_count, mySearchRecord_count + 1)

    def test_addToCart_login_staff_ajax(self):
        """
        Test view if the request is an AJAX request
        """
        #get initial objects count
        mySearchRecord_count = len(SearchRecord.objects.all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('addToCart', kwargs={'theId': 1934163}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/javascript')
        self.assertEqual(
            myResp.content, '{"Status": "Added", "Item": "1934163"}')
        # check if new record count
        myNewSearchRecord_count = len(SearchRecord.objects.all())
        self.assertEqual(myNewSearchRecord_count, mySearchRecord_count + 1)

    def test_addToCart_login_staff_duplicate_item(self):
        """
        Test view when trying to add duplicate item to cart
        """
        #get initial objects count
        mySearchRecord_count = len(SearchRecord.objects.all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('addToCart', kwargs={'theId': 6541}))

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/javascript')
        self.assertEqual(
            myResp.content, 'alert("Item already exists in your cart!");')
        # check if new record count is the same as before changes
        myNewSearchRecord_count = len(SearchRecord.objects.all())
        self.assertEqual(myNewSearchRecord_count, mySearchRecord_count)
