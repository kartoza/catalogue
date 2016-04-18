"""
SANSA-EO Catalogue - shopping_cart_view_showMiniCartContents - Shopping cart
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
__date__ = '17/10/2012'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from search.tests.model_factories import SearchRecordF
from .model_factories import OpticalProductF


class ShoppingCart_showMiniCartContents_Tests(TestCase):
    """
    Tests tasking.py showMiniCartContents method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_showMiniCartContents_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showMiniCartContents',
                kwargs=myKwargTest)

    def test_showMiniCartContents_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('showMiniCartContents', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            '/accounts/signin/?next=/showminicartcontents/')

    def test_showMiniCartContents_login_staff(self):
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
        myResp = myClient.get(reverse('showMiniCartContents', kwargs={}))

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
        self.assertEqual(myResp.context['myShowIdFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], True)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowMiniCartFlag'], True)
        self.assertEqual(myResp.context['myShowPreviewFlag'], True)
        self.assertEqual(
            myResp.context['myBaseTemplate'], 'cartContentsPage.html')
        self.assertEqual(myResp.context['myMiniCartFlag'], True)

    def test_showMiniCartContents_login_staff_ajax(self):
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
            reverse('showMiniCartContents', kwargs={}),
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
        self.assertEqual(myResp.context['myShowIdFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], True)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], False)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowMiniCartFlag'], True)
        self.assertEqual(myResp.context['myShowPreviewFlag'], True)
        self.assertEqual(
            myResp.context['myBaseTemplate'], 'emptytemplate.html')
        self.assertEqual(myResp.context['myMiniCartFlag'], True)
