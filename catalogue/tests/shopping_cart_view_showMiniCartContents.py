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

from catalogue.models import SearchRecord


class ShoppingCart_showMiniCartContents_Tests(TestCase):
    """
    Tests tasking.py showMiniCartContents method/view
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

    def test_showMiniCartContents_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

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
            'http://testserver/accounts/login/?next=/showminicartcontents/')

    def test_showMiniCartContents_login_staff(self):
        """
        Test view if user is staff
        """
        #get initial objects count
        mySearchRecord_count = len(
            SearchRecord.objects.all().filter(user__username='timlinux')
            .filter(order__isnull=True))

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('showMiniCartContents', kwargs={}))

        # check response
        self.assertEqual(myResp.status_code, 200)

        # check number ot returned records
        self.assertEqual(
            len(myResp.context['myRecords']), mySearchRecord_count)

        # check used templates
        myExpTemplates = [
            'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
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
        #get initial objects count
        mySearchRecord_count = len(
            SearchRecord.objects.all().filter(user__username='timlinux')
            .filter(order__isnull=True))

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('showMiniCartContents', kwargs={}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # check response
        self.assertEqual(myResp.status_code, 200)

        # check number ot returned records
        self.assertEqual(
            len(myResp.context['myRecords']), mySearchRecord_count)

        # check used templates
        myExpTemplates = [
            'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
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
