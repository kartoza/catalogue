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
__version__ = '0.2'
__date__ = '13/08/2013'
__copyright__ = 'South African National Space Agency'

import re

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from ..forms import (
    OrderForm,
    DeliveryDetailForm
)

from ..models import Order

from core.model_factories import UserF
from useraccounts.tests.model_factories import SansaUserProfileF
from search.tests.model_factories import SearchRecordF

from .model_factories import (
    DeliveryMethodF, ProjectionF, FileFormatF, ResamplingMethodF, DatumF,
    MarketSectorF, OpticalProductF, OrderStatusF
)


class OrdersViews_addOrder_Tests(TestCase):
    """
    Tests orders.py addOrder method/view
    """

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
            'http://testserver/accounts/signin/?next=/addorder/')

    def test_addOrder_login_user_noprofile(self):
        """
        Test view if user has no profile
        """

        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

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
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': myUser,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })

        SearchRecordF.create(**{
            'user': myUser,
            'order': None
        })

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
        self.assertEqual(len(myResp.context['myRecords']), 1)
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
            'addPage.html', u'basev3.html', u'menu.html',
            u'useraccounts/menu_content.html', u'add.html',
            u'cartContents.html', u'recordHeader.html', u'record.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_addOrder_login_staff_emptyCart(self):
        """
        Test view if user is staff, and cart is empty
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': myUser,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })

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
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': myUser,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })
        myProjection = ProjectionF.create(**{
            'id': 86,
            'epsg_code': '4326'
        })
        FileFormatF.create(**{'id': 1})

        DatumF.create(**{'id': 1})
        ResamplingMethodF.create(**{'id': 1})
        MarketSectorF.create(**{'id': 1})
        DeliveryMethodF.create(**{'id': 1})

        myOProduct = OpticalProductF.create(**{
            'projection': myProjection
        })

        SearchRecordF.create(**{
            'id': 6,
            'user': myUser,
            'order': None,
            'product': myOProduct
        })

        OrderStatusF.create(**{'id': 1})

        myOrdersCount = len(Order.objects.all())

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'86'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'1'],
            u'market_sector': [u'1'], u'geometry_file': [u''],
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'1'], u'6-projection': [u'86']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertTrue(
            re.match(
                'http://testserver/vieworder/(\d+)/',
                myResp['Location']) is not None
        )

        myOrdersCount_new = len(Order.objects.all())
        self.assertEqual(myOrdersCount_new, myOrdersCount + 1)

    def test_addOrder_login_staff_invalid_post(self):
        """
        Test view if user is staff, and post is invalid (projection)
        """

        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': myUser,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })
        myProjection = ProjectionF.create(**{
            'id': 86,
            'epsg_code': '4326'
        })
        FileFormatF.create(**{'id': 1})

        DatumF.create(**{'id': 1})
        ResamplingMethodF.create(**{'id': 1})
        MarketSectorF.create(**{'id': 1})
        DeliveryMethodF.create(**{'id': 1})

        myOProduct = OpticalProductF.create(**{
            'projection': myProjection
        })

        SearchRecordF.create(**{
            'id': 6,
            'user': myUser,
            'order': None,
            'product': myOProduct
        })

        OrderStatusF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'100'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'1'],
            u'market_sector': [u'1'], u'geometry_file': [u''],
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'1'], u'6-projection': [u'100']}

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
        self.assertEqual(len(myResp.context['myRecords']), 1)
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
            'addPage.html', u'basev3.html', u'menu.html',
            u'useraccounts/menu_content.html', u'add.html',
            u'cartContents.html', u'recordHeader.html', u'record.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_addOrder_login_staff_valid_post_geometryfile(self):
        """
        Test view if user is staff, and post is valid, valid geometry_file
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': myUser,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })
        myProjection = ProjectionF.create(**{
            'id': 86,
            'epsg_code': '4326'
        })
        FileFormatF.create(**{'id': 1})

        DatumF.create(**{'id': 1})
        ResamplingMethodF.create(**{'id': 1})
        MarketSectorF.create(**{'id': 1})
        DeliveryMethodF.create(**{'id': 1})

        myOProduct = OpticalProductF.create(**{
            'projection': myProjection
        })

        SearchRecordF.create(**{
            'id': 6,
            'user': myUser,
            'order': None,
            'product': myOProduct
        })

        OrderStatusF.create(**{'id': 1})

        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area.zip', 'rb')

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'86'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'1'],
            u'market_sector': [u'1'], u'geometry_file': myUploadFile,
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'1'], u'6-projection': [u'86']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertTrue(
            re.match(
                'http://testserver/vieworder/(\d+)/',
                myResp['Location']) is not None
        )

        self.assertEqual(len(Order.objects.all()), 1)

    def test_addOrder_login_staff_valid_post_invalid_geometryfile(self):
        """
        Test view if user is staff, and post is valid, invalid geometry_file
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': myUser,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })
        myProjection = ProjectionF.create(**{
            'id': 86,
            'epsg_code': '4326'
        })
        FileFormatF.create(**{'id': 1})

        DatumF.create(**{'id': 1})
        ResamplingMethodF.create(**{'id': 1})
        MarketSectorF.create(**{'id': 1})
        DeliveryMethodF.create(**{'id': 1})

        myOProduct = OpticalProductF.create(**{
            'projection': myProjection
        })

        SearchRecordF.create(**{
            'id': 6,
            'user': myUser,
            'order': None,
            'product': myOProduct
        })

        OrderStatusF.create(**{'id': 1})

        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area-invalid.zip', 'rb')

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myPostData = {
            u'aoi_geometry': [u''], u'projection': [u'86'],
            u'file_format': [u'1'], u'geometry': [u''], u'notes': [u''],
            u'datum': [u'1'], u'resampling_method': [u'1'],
            u'market_sector': [u'1'], u'geometry_file': myUploadFile,
            u'delivery_method': [u'1'], u'ref_id': [u'6'],
            u'6-file_format': [u'1'],
            u'6-datum': [u'1'], u'6-ref_id': [u'6'],
            u'6-resampling_method': [u'1'], u'6-projection': [u'86']}

        myResp = myClient.post(reverse('addOrder', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 302)
        self.assertTrue(
            re.match(
                'http://testserver/vieworder/(\d+)/',
                myResp['Location']) is not None
        )

        self.assertEqual(len(Order.objects.all()), 1)