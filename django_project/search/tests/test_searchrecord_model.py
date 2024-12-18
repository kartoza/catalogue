"""
SANSA-EO Catalogue - SearchRecord_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '17/07/2013'
__copyright__ = 'South African National Space Agency'

from decimal import Decimal

from django.test import TestCase

from core.model_factories import (
    UserF,
    CurrencyF,
    ExchangeRateF
)
from orders.tests.model_factories import OrderF
from catalogue.tests.model_factories import (
    GenericProductF,
    OpticalProductF
)

from dictionaries.tests.model_factories import (
    OpticalProductProfileF,
    SpectralModeF,
    SpectralModeProcessingCostsF,
    ProcessingLevelF,
    ProjectionF,
    ProductProcessStateF,
    InstrumentTypeF,
    SatelliteInstrumentGroupF,
    SatelliteInstrumentF,
    InstrumentTypeProcessingLevelF
)

from model_factories import SearchRecordF


class TestSearchRecordCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SearchRecord_create(self):
        """
        Tests SearchRecord model creation
        """
        myModel = SearchRecordF.create(
            currency=CurrencyF.create(code='ZAR'),
        )

        # check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_SearchRecord_read(self):
        """
        Tests SearchRecord model read
        """
        mySpecMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })

        tstUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password'
        })

        tstCurrency = CurrencyF.create(**{
            'code': 'ZAR',
            'name': 'SuperGold'
        })

        tstProcLevel = ProcessingLevelF.create(**{})
        tstInstType = InstrumentTypeF.create()

        tstInsTypeProcLevel = InstrumentTypeProcessingLevelF.create(**{
            'instrument_type': tstInstType,
            'processing_level': tstProcLevel
        })

        SpectralModeProcessingCostsF.create(**{
            'spectral_mode': mySpecMode,
            'instrument_type_processing_level': tstInsTypeProcLevel,
            'cost_per_scene': Decimal(123.12),
            'currency': tstCurrency
        })

        tstSatInstGrp = SatelliteInstrumentGroupF.create(**{
            'instrument_type': tstInstType
        })

        tstSatInst = SatelliteInstrumentF.create(**{
            'satellite_instrument_group': tstSatInstGrp
        })
        myOPP = OpticalProductProfileF.create(**{
            'spectral_mode': mySpecMode,
            'satellite_instrument': tstSatInst
        })

        tstProduct = OpticalProductF.create(**{
            'product_profile': myOPP
        })

        myOrder = OrderF.create(notes='New Order')

        # tstProcLevel = ProcessingLevelF.create(**{})

        tstProjection = ProjectionF.create()

        tstProdProcState = ProductProcessStateF.create()

        myModel = SearchRecordF.create(**{
            'user': tstUser,
            'order': myOrder,
            'product': tstProduct,
            'internal_order_id': 98765,
            'download_path': 'someplace/somewhere',
            'product_ready': True,
            # 'rand_cost_per_scene': 321.21,
            'currency': tstCurrency,
            'processing_level': tstProcLevel,
            'projection': tstProjection,
            'product_process_state': tstProdProcState
        })

        self.assertTrue(myModel.pk is not None)
        self.assertEqual(
            myModel.internal_order_id, 98765)
        self.assertEqual(myModel.download_path, 'someplace/somewhere')
        self.assertEqual(myModel.cost_per_scene, Decimal(123.12).quantize(Decimal('.01')))
        # self.assertEqual(myModel.rand_cost_per_scene, 321.21)
        self.assertEqual(myModel.product_ready, True)

    def test_SearchRecord_update(self):
        """
        Tests SearchRecord model update
        """
        myModel = SearchRecordF.create(
            currency=CurrencyF.create(code='ZAR'),
        )

        myNewOrder = OrderF()

        myNewModelData = {
            'order': myNewOrder,
            'download_path': 'Some path',
            'product_ready': True,
            'cost_per_scene': 123,
            'rand_cost_per_scene': 123
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        # check if updated
        for key, val in list(myNewModelData.items()):
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_SearchRecord_delete(self):
        """
        Tests SearchRecord model delete
        """
        myModel = SearchRecordF.create(
            currency=CurrencyF.create(code='ZAR'),
        )

        myModel.delete()

        # check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SearchRecord_kmlExtents(self):
        """
        Tests SearchRecord model kmlExtents method
        """
        myExpResult = """<north>-32.05</north>
          <south>-35.17</south>
          <east>20.83</east>
          <west>17.54</west>"""

        myModel = SearchRecordF.create(
            currency=CurrencyF.create(code='ZAR'),
        )

        myRes = myModel.kmlExtents()
        self.assertEqual(myRes, myExpResult)

    def test_SearchRecord_repr(self):
        """
        Tests SearchRecord model repr method
        """
        myProduct = GenericProductF.create(original_product_id='123qwe')
        myModel = SearchRecordF.create(
            product=myProduct,
            currency=CurrencyF.create(code='ZAR'),
        )

        myExpResult = '123qwe'
        self.assertEqual(str(myModel), myExpResult)

    def test_SearchRecord_create_method(self):
        """
        Tests SearchRecord model create method
        """
        myProduct = GenericProductF.create(original_product_id='123qwe')
        myUser = UserF.create(username='testuser')
        myModel = SearchRecordF.create(
            currency=CurrencyF.create(code='ZAR'),
        )

        myNewModel = myModel.create(myUser, myProduct)

        self.assertEqual(str(myNewModel), '123qwe')
        self.assertEqual(myNewModel.user.username, 'testuser')

    def test_SearchRecord_snapshot_price_and_currency_method(self):
        """
        Tests SearchRecord model snapshot_price_and_currency method
        """

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

        tstProcLevel = ProcessingLevelF.create(**{})
        tstInstType = InstrumentTypeF.create()

        tstInsTypeProcLevel = InstrumentTypeProcessingLevelF.create(**{
            'instrument_type': tstInstType,
            'processing_level': tstProcLevel
        })

        SpectralModeProcessingCostsF.create(**{
            'spectral_mode': mySpecMode,
            'instrument_type_processing_level': tstInsTypeProcLevel,
            'cost_per_scene': Decimal(123.45),
            'currency': myCurrency
        })

        tstSatInstGrp = SatelliteInstrumentGroupF.create(**{
            'instrument_type': tstInstType
        })

        tstSatInst = SatelliteInstrumentF.create(**{
            'satellite_instrument_group': tstSatInstGrp
        })
        myOPP = OpticalProductProfileF.create(**{
            'spectral_mode': mySpecMode,
            'satellite_instrument': tstSatInst
        })

        myProduct = OpticalProductF.create(**{
            'product_profile': myOPP
        })
        myUser = UserF.create(username='testuser')
        myModel = SearchRecordF.create(**{
            'processing_level': tstProcLevel,
            'product': myProduct,
            'user': myUser
        })

        # preform the snapshot
        myModel._snapshot_cost_and_currency()

        self.assertEqual(
            myModel.cost_per_scene, Decimal(123.45).quantize(Decimal('.01'))
        )
        self.assertEqual(myModel.currency, myCurrency)
        self.assertEqual(
            myModel.rand_cost_per_scene,
            Decimal(246.90).quantize(Decimal('.01'))
        )
