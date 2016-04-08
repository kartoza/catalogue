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


import unittest
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF

from .model_factories import GenericProductF


class OthersViews_showProduct_Tests(TestCase):
    """
    Tests others.py showProduct method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_showProduct_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showProduct',
                kwargs=myKwargTest)

    @unittest.skip("Currently not used anymore")
    def test_showProduct(self):
        """
        Test view show product and product id is found
        """

        GenericProductF.create(**{'unique_product_id': 'XY1234'})
        myClient = Client()
        myResp = myClient.get(
            reverse('showProduct', kwargs={'theProductId': 'XY1234'})
        )
        self.assertEqual(myResp.status_code, 200)
        
        self.assertEqual(myResp.context['messages'], ['Product found'])
        self.assertEqual(
            myResp.context['myProduct'].unique_product_id,
            'XY1234'
        )

        # check used templates
        myExpTemplates = [
            'productView.html', u'base.html',
            u'pipeline/css.html', u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html',
            'productTypes/opticalProduct.html',
            u'productTypes/genericSensorProduct.html',
            u'productTypes/genericImageryProduct.html',
            u'productTypes/genericProduct.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_showProduct_bad_product(self):
        """
        Test view product id is not found
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('showProduct', kwargs={'theProductId': 'XY1234'})
        )

        self.assertEqual(
            myResp.context['messages'], ['No matching product found'])

        self.assertEqual(myResp.context['myProduct'], None)
