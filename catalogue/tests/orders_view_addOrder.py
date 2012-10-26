"""
SANSA-EO Catalogue - orders_view_addOrder - Orders views
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
__version__ = '0.1'
__date__ = '23/10/2012'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.forms import (
    OrderForm,
    DeliveryDetailForm
)

from catalogue.models import (
    SearchRecord,
    Order
)


class OrdersViews_addOrder_Tests(TestCase):
    """
    Tests orders.py addOrder method/view
    """

    fixtures = [
        'test_projection.json',
        'test_datum.json',
        'test_fileformat.json',
        'test_processinglevel.json',
        'test_resamplingmethod.json',
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
        'test_sacuserprofile.json',
        'test_orderstatus.json',
        'test_orderstatushistory.json',
        'test_marketsector.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_addOrder_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'addOrder',
                kwargs=myKwargTest)

    def test_addOrder_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('addOrder', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/login/?next=/addorder/')

    def test_addOrder_login_user_noprofile(self):
        """
        Test view if user has no profile
        """

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(reverse('addOrder', kwargs={}))

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/profile/edit/personal/'
                '?next=/addorder/'))

    def test_addOrder_login_staff(self):
        """
        Test view if user is staff
        """
        myRecords = SearchRecord.objects.all().filter(
            user__username='timlinux').filter(order__isnull=True)

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('addOrder', kwargs={}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], True)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], True)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowCartContentsFlag'], True)
        self.assertEqual(myResp.context['myShowPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], False)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], True)
        self.assertEqual(myResp.context['myCartTitle'], 'Order Product List')
        self.assertEqual(len(myResp.context['myRecords']), len(myRecords))
        self.assertEqual(
            myResp.context['myBaseTemplate'], 'emptytemplate.html')
        self.assertEqual(myResp.context['mySubmitLabel'], 'Submit Order')
        # self.assertEqual(
        #     myResp.context['myLayerDefinitions'], myLayerDefinitions)
        # self.assertEqual(myResp.context['myLayersList'], myLayersList)
        # self.assertEqual(myResp.context['myActiveBaseMap'], myActiveBaseMap)
        self.assertEqual(myResp.context['myOrderForm'].__class__, OrderForm)
        self.assertEqual(
            myResp.context['myDeliveryDetailForm'].__class__,
            DeliveryDetailForm)
        self.assertEqual(myResp.context['myTitle'], 'Create a new order')
        self.assertEqual(myResp.context['mySubmitLabel'], 'Submit Order')
        self.assertEqual(myResp.context['myMessage'], (
            ' <div>Please specify any details for your order'
            ' requirements below. If you need specific processing'
            ' steps taken on individual images, please use the notes'
            ' area below to provide detailed instructions. If you'
            ' would like the product(s) to be clipped and masked'
            ' to a specific geographic region, you can digitise'
            ' that region using the map above, or the geometry'
            ' input field below.</div>'))

        # check used templates
        myExpTemplates = [
            'addPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'add.html',
            u'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_addOrder_login_staff_emptyCart(self):
        """
        Test view if user is staff, and cart is empty
        """
        # update all records, empty the cart
        myRecords = SearchRecord.objects.all().filter(
            user__username='timlinux').filter(order__isnull=True)

        for record in myRecords:
            record.order_id = 1
            record.save()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('addOrder', kwargs={}))

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], 'http://testserver/emptyCartHelp/')

    def test_addOrder_login_staff_valid_post(self):
        """
        Test view if user is staff, and post is valid
        """
        myOrdersCount = len(Order.objects.all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'86'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'2'],
            u'market_sector': [u'1'], u'geometry_file': [u''],
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'2'], u'6-projection': [u'86']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], 'http://testserver/vieworder/4')

        myOrdersCount_new = len(Order.objects.all())
        self.assertEqual(myOrdersCount_new, myOrdersCount + 1)

    def test_addOrder_login_staff_invalid_post(self):
        """
        Test view if user is staff, and post is invalid (projection)
        """
        myRecords = SearchRecord.objects.all().filter(
            user__username='timlinux').filter(order__isnull=True)

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'100'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'2'],
            u'market_sector': [u'1'], u'geometry_file': [u''],
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'2'], u'6-projection': [u'100']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(myResp.context['myShowSensorFlag'], False)
        self.assertEqual(myResp.context['myShowSceneIdFlag'], True)
        self.assertEqual(myResp.context['myShowDateFlag'], False)
        self.assertEqual(myResp.context['myShowRemoveIconFlag'], True)
        self.assertEqual(myResp.context['myShowRowFlag'], False)
        self.assertEqual(myResp.context['myShowPathFlag'], False)
        self.assertEqual(myResp.context['myShowCloudCoverFlag'], True)
        self.assertEqual(myResp.context['myShowMetdataFlag'], False)
        self.assertEqual(myResp.context['myShowCartFlag'], False)
        self.assertEqual(myResp.context['myShowCartContentsFlag'], True)
        self.assertEqual(myResp.context['myShowPreviewFlag'], False)
        self.assertEqual(myResp.context['myShowDeliveryDetailsFlag'], False)
        self.assertEqual(
            myResp.context['myShowDeliveryDetailsFormFlag'], True)
        self.assertEqual(myResp.context['myCartTitle'], 'Order Product List')
        self.assertEqual(len(myResp.context['myRecords']), len(myRecords))
        self.assertEqual(
            myResp.context['myBaseTemplate'], 'emptytemplate.html')
        self.assertEqual(myResp.context['mySubmitLabel'], 'Submit Order')
        # self.assertEqual(
        #     myResp.context['myLayerDefinitions'], myLayerDefinitions)
        # self.assertEqual(myResp.context['myLayersList'], myLayersList)
        # self.assertEqual(myResp.context['myActiveBaseMap'], myActiveBaseMap)
        self.assertEqual(myResp.context['myOrderForm'].__class__, OrderForm)
        self.assertEqual(
            myResp.context['myDeliveryDetailForm'].__class__,
            DeliveryDetailForm)
        self.assertEqual(myResp.context['myTitle'], 'Create a new order')
        self.assertEqual(myResp.context['mySubmitLabel'], 'Submit Order')
        self.assertEqual(myResp.context['myMessage'], (
            ' <div>Please specify any details for your order'
            ' requirements below. If you need specific processing'
            ' steps taken on individual images, please use the notes'
            ' area below to provide detailed instructions. If you'
            ' would like the product(s) to be clipped and masked'
            ' to a specific geographic region, you can digitise'
            ' that region using the map above, or the geometry'
            ' input field below.</div>'))

        # check used templates
        myExpTemplates = [
            'addPage.html', u'base.html', u'menu.html',
            u'userprofile/menu_content.html', u'add.html',
            u'cartContents.html', u'recordHeader.html', u'record.html',
            u'record.html', u'record.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.template]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_addOrder_login_staff_valid_post_geometryfile(self):
        """
        Test view if user is staff, and post is valid, valid geometry_file
        """
        myOrdersCount = len(Order.objects.all())

        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area.zip', 'rb')

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'86'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'2'],
            u'market_sector': [u'1'], u'geometry_file': myUploadFile,
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'2'], u'6-projection': [u'86']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], 'http://testserver/vieworder/4')

        myOrdersCount_new = len(Order.objects.all())
        self.assertEqual(myOrdersCount_new, myOrdersCount + 1)

    def test_addOrder_login_staff_valid_post_invalid_geometryfile(self):
        """
        Test view if user is staff, and post is valid, invalid geometry_file
        """
        myOrdersCount = len(Order.objects.all())

        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area-invalid.zip', 'rb')

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'86'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'2'],
            u'market_sector': [u'1'], u'geometry_file': myUploadFile,
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'2'], u'6-projection': [u'86']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], 'http://testserver/vieworder/4')

        myOrdersCount_new = len(Order.objects.all())
        self.assertEqual(myOrdersCount_new, myOrdersCount + 1)
