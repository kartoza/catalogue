"""
SANSA-EO Catalogue - shopping_cart_view_showCartContents - Shopping cart
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


class ShoppingCart_showCartContents_Tests(TestCase):
    """
    Tests tasking.py showCartContents method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_showCartContents_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showCartContents',
                kwargs=myKwargTest)

    def test_showCartContents_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('showCartContents', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/showcartcontents/')

    def test_showCartContents_login_staff(self):
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
        myResp = myClient.get(reverse('showCartContents', kwargs={}))

        # check response
        self.assertEqual(myResp.status_code, 200)

        # check number ot returned records
        self.assertEqual(len(myResp.context['myRecords']), 1)

        # check used templates
        myExpTemplates = [
            'cartContentsPage.html', u'base.html',
            u'pipeline/css.html', u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html', u'cartContents.html',
            u'recordHeader.html', u'record.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], True)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], True)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], True)
        self.assertEqual(myResp.context['myShowMetdataFlag'], True)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowPreviewFlag'], True)
        self.assertEqual(myResp.context['myCartTitle'], 'Cart Contents')
        self.assertEqual(myResp.context['myMiniCartFlag'], False)

        # test ajax flag
        self.assertEqual(myResp.context['myAjaxFlag'], False)

    def test_showCartContents_login_staff_ajax(self):
        """
        Test view if user is staff, and request is ajax
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
        myResp = myClient.get(
            reverse('showCartContents', kwargs={}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check response
        self.assertEqual(myResp.status_code, 200)

        # check number ot returned records
        self.assertEqual(len(myResp.context['myRecords']), 1)

        # check used templates
        myExpTemplates = [
            'cartContents.html', u'recordHeader.html', u'record.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], True)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], True)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], True)
        self.assertEqual(myResp.context['myShowMetdataFlag'], True)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowPreviewFlag'], True)
        self.assertEqual(myResp.context['myCartTitle'], 'Cart Contents')
        self.assertEqual(myResp.context['myMiniCartFlag'], False)

        # test ajax flag
        self.assertEqual(myResp.context['myAjaxFlag'], True)
