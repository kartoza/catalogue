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

from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from ..forms import OrderForm

from ..models import Order

from core.model_factories import (
    UserF,
    CurrencyF,
    ExchangeRateF
)
from useraccounts.tests.model_factories import SansaUserProfileF
from search.tests.model_factories import SearchRecordF
from dictionaries.tests.model_factories import (
    SpectralModeF,
    OpticalProductProfileF,
    SpectralModeProcessingCostsF,
    ProcessingLevelF,
    ProjectionF,
    InstrumentTypeF,
    SatelliteInstrumentGroupF,
    SatelliteInstrumentF,
    InstrumentTypeProcessingLevelF
)

from catalogue.tests.model_factories import OpticalProductF

from .model_factories import (
    DeliveryMethodF,
    FileFormatF,
    ResamplingMethodF,
    DatumF,
    MarketSectorF,
    OrderStatusF
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
        myKwargsTests = [{'testargs': 1}]

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
            '/accounts/signin/?next=/addorder/')

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
                '/accounts/profile/edit/personal/'
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

        self.assertEqual(len(myResp.context['myRecords']), 1)
        self.assertEqual(myResp.context['myOrderForm'].__class__, OrderForm)

        # check used templates
        myExpTemplates = [
            'addPage.html', 'base.html', 'pipeline/css.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html', 'add.html',
            'cartContents.html', 'recordHeader.html', 'record.html'
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
            myResp['Location'], '/emptyCartHelp/')

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

        mySpecMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })

        superRand = CurrencyF.create(**{
            'name': 'SuperRand',
            'code': 'ZAR'
        })

        myCurrency = CurrencyF.create(**{
            'name': 'SuperGold',
            'code': 'SG'
        })

        ExchangeRateF.create(**{
            'source': myCurrency,
            'target': superRand,
            'rate': 2.0
        })

        proc_level = ProcessingLevelF.create(**{})
        inst_type = InstrumentTypeF.create()

        ins_type_proc_level = InstrumentTypeProcessingLevelF.create(**{
            'instrument_type': inst_type,
            'processinglevel': proc_level
        })

        SpectralModeProcessingCostsF.create(**{
            'spectral_mode': mySpecMode,
            'instrumenttypeprocessinglevel': ins_type_proc_level,
            'cost_per_scene': 123.45,
            'currency': myCurrency
        })

        sat_inst_grp = SatelliteInstrumentGroupF.create(**{
            'instrument_type': inst_type
        })

        sat_inst = SatelliteInstrumentF.create(**{
            'satellite_instrument_group': sat_inst_grp
        })
        opp = OpticalProductProfileF.create(**{
            'spectral_mode': mySpecMode,
            'satellite_instrument': sat_inst
        })

        product = OpticalProductF.create(**{
            'projection': myProjection,
            'product_profile': opp
        })

        SearchRecordF.create(**{
            'id': 6,
            'user': myUser,
            'order': None,
            'product': product,
            'processing_level': proc_level
        })

        OrderStatusF.create(**{'id': 1})

        orders_count = Order.objects.all().count()

        client = Client()
        client.login(username='timlinux', password='password')

        data = {
            'projection': ['86'], 'file_format': ['1'], 'notes': [''],
            'datum': ['1'], 'resampling_method': ['1'],
            'market_sector': ['1'], 'delivery_method': ['1'],
            'ref_id': ['6'], '6-file_format': ['1'], '6-datum': ['1'],
            '6-ref_id': ['6'], '6-resampling_method': ['1'],
            '6-projection': ['86']
        }

        resp = client.post(reverse('addOrder', kwargs={}), data)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            re.match(
                '/vieworder/(\d+)/',
                resp['Location']) is not None
        )

        myOrdersCount_new = Order.objects.all().count()
        self.assertEqual(myOrdersCount_new, orders_count + 1)

    def test_addOrder_login_staff_invalid_post(self):
        """
        Test view if user is staff, and post is invalid (projection)
        """

        user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SansaUserProfileF.create(**{
            'user': user,
            'address1': '12321 kjk',
            'address2': 'kjkj',
            'post_code': '123',
            'organisation': 'None',
            'contact_no': '123123'
        })
        projection = ProjectionF.create(**{
            'id': 86,
            'epsg_code': '4326'
        })
        FileFormatF.create(**{'id': 1})

        DatumF.create(**{'id': 1})
        ResamplingMethodF.create(**{'id': 1})
        MarketSectorF.create(**{'id': 1})
        DeliveryMethodF.create(**{'id': 1})

        product = OpticalProductF.create(**{
            'projection': projection
        })

        SearchRecordF.create(**{
            'id': 6,
            'user': user,
            'order': None,
            'product': product
        })

        OrderStatusF.create(**{'id': 1})

        client = Client()
        client.login(username='timlinux', password='password')

        data = {
            'projection': ['100'], 'file_format': ['1'], 'notes': [''],
            'datum': ['1'], 'resampling_method': ['1'],
            'market_sector': ['1'], 'ref_id': ['6']
        }

        res = client.post(reverse('addOrder', kwargs={}), data)

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.context['myShowSensorFlag'], False)
        self.assertEqual(res.context['myShowSceneIdFlag'], True)
        self.assertEqual(res.context['myShowDateFlag'], False)
        self.assertEqual(res.context['myShowRemoveIconFlag'], True)
        self.assertEqual(res.context['myShowRowFlag'], False)
        self.assertEqual(res.context['myShowPathFlag'], False)
        self.assertEqual(res.context['myShowCloudCoverFlag'], True)
        self.assertEqual(res.context['myShowMetdataFlag'], False)
        self.assertEqual(res.context['myShowCartFlag'], False)
        self.assertEqual(res.context['myShowCartContentsFlag'], True)
        self.assertEqual(res.context['myShowPreviewFlag'], False)
        self.assertEqual(res.context['myShowDeliveryDetailsFlag'], False)
        self.assertEqual(
            res.context['myShowDeliveryDetailsFormFlag'], True)
        self.assertEqual(res.context['myCartTitle'], 'Order Product List')
        self.assertEqual(len(res.context['myRecords']), 1)
        self.assertEqual(
            res.context['myBaseTemplate'], 'emptytemplate.html')
        self.assertEqual(res.context['mySubmitLabel'], 'Submit Order')
        # self.assertEqual(
        #     myResp.context['myLayerDefinitions'], myLayerDefinitions)
        # self.assertEqual(myResp.context['myLayersList'], myLayersList)
        # self.assertEqual(myResp.context['myActiveBaseMap'], myActiveBaseMap)
        self.assertEqual(res.context['myOrderForm'].__class__, OrderForm)
        self.assertEqual(res.context['myTitle'], 'Create a new order')
        self.assertEqual(res.context['mySubmitLabel'], 'Submit Order')
        self.assertEqual(res.context['myMessage'], (
            ' <div>Please specify any details for your order'
            ' requirements below. If you need specific processing'
            ' steps taken on individual images, please use the notes'
            ' area below to provide detailed instructions. If you'
            ' would like the product(s) to be clipped and masked'
            ' to a specific geographic region, you can digitise'
            ' that region using the map above, or the geometry'
            ' input field below.</div>'))

        # check used templates
        exp_templates = [
            'addPage.html', 'base.html', 'pipeline/css.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html', 'add.html',
            'cartContents.html', 'recordHeader.html', 'record.html'
        ]

        used_templates = [tmpl.name for tmpl in res.templates]
        self.assertEqual(used_templates, exp_templates)
