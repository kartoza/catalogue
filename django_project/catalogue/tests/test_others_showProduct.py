"""
SANSA-EO Catalogue - others_showProduct - Others views
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
__date__ = '08/08/2012'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF

from .model_factories import OpticalProductF


class OthersViews_showProduct_Tests(TestCase):
    """
    Tests others.py showProduct method/view
    """

    def setUp(self):
        """
        Set up before each test
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

    def test_showProduct_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showProduct',
                kwargs=myKwargTest)

    def test_showProduct_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'showProduct',
                kwargs={
                    'theProductId': (
                        'S1-_RVV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_'
                        'ORBIT-')
                }
            )
        )
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/signin/?next=/showProduct/S1-_RVV_'
                'X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-/'
            )
        )

    def test_showProduct_userlogin(self):
        """
        Test view if user is logged as user and product id is found
        """

        OpticalProductF.create(**{
            'unique_product_id': (
                'S1-_RVV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-')
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'showProduct',
                kwargs={
                    'theProductId': (
                        'S1-_RVV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_'
                        'ORBIT-')
                }
            )
        )
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['messages'], ['Product found'])

        self.assertEqual(
            myResp.context['myProduct'].unique_product_id,
            'S1-_RVV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'
        )

        # check used templates
        myExpTemplates = [
            'productView.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html',
            'productTypes/opticalProduct.html',
            u'productTypes/genericSensorProduct.html',
            u'productTypes/genericImageryProduct.html',
            u'productTypes/genericProduct.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_showProduct_userlogin_bad_product(self):
        """
        Test view if user is logged as user and product id is not found
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'showProduct',
                kwargs={
                    'theProductId': (
                        'S1-_RVV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_'
                        'ORBIT-')
                }
            )
        )

        self.assertEqual(
            myResp.context['messages'], ['No matching product found'])

        self.assertEqual(myResp.context['myProduct'], None)