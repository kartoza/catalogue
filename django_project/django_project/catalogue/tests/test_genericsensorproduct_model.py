"""
SANSA-EO Catalogue - genericsensorproduct_model - implements basic CRUD
unittests

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
__date__ = '25/07/2013'
__copyright__ = 'South African National Space Agency'

from datetime import datetime

from django.test import TestCase

from .model_factories import GenericSensorProductF


class GenericSensorProductCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_genericSensorproduct_create(self):
        """
        Tests GenericSensorProduct model creation
        """
        myModel = GenericSensorProductF.create(**{
            'product_acquisition_start': datetime(2008, 1, 1, 12, 00),
            'product_acquisition_end': datetime(2008, 1, 1, 13, 00),
            'geometric_accuracy_mean': 5.0,
            'geometric_accuracy_1sigma': 2.0,
            'geometric_accuracy_2sigma': 3.0,
            'radiometric_signal_to_noise_ratio': 0.0,
            'radiometric_percentage_error': 0.0,
            'spectral_accuracy': 20.0,
            'orbit_number': 1,
            'path': 123,
            'path_offset': 0,
            'row': 321,
            'row_offset': 0,
            'offline_storage_medium_id': '',
            'online_storage_medium_id': '',
        })

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_genericSensorproduct_delete(self):
        """
        Tests GenericSensorProduct model delete
        """
        myModel = GenericSensorProductF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_genericSensorproduct_read(self):
        """
        Tests GenericSensorProduct model read
        """
        myModel = GenericSensorProductF.create(**{
            'product_acquisition_start': datetime(2008, 1, 1, 12, 00),
            'product_acquisition_end': datetime(2008, 1, 1, 13, 00),
            'geometric_accuracy_mean': 50.0,
            'geometric_accuracy_1sigma': 20.0,
            'geometric_accuracy_2sigma': 30.0,
            'radiometric_signal_to_noise_ratio': 5.0,
            'radiometric_percentage_error': 10.0,
            'spectral_accuracy': 20.0,
            'orbit_number': 1,
            'path': 321,
            'path_offset': 0,
            'row': 123,
            'row_offset': 0,
            'offline_storage_medium_id': '',
            'online_storage_medium_id': '',
        })

        self.assertEqual(
            myModel.product_acquisition_start, datetime(2008, 1, 1, 12, 00))

        self.assertEqual(
            myModel.product_acquisition_end, datetime(2008, 1, 1, 13, 00))

        self.assertEqual(myModel.geometric_accuracy_mean, 50.0)
        self.assertEqual(myModel.geometric_accuracy_1sigma, 20.0)
        self.assertEqual(myModel.geometric_accuracy_2sigma, 30.0)
        self.assertEqual(myModel.radiometric_signal_to_noise_ratio, 5.0)
        self.assertEqual(myModel.radiometric_percentage_error, 10.0)
        self.assertEqual(myModel.spectral_accuracy, 20.0)
        self.assertEqual(myModel.orbit_number, 1)
        self.assertEqual(myModel.path, 321)
        self.assertEqual(myModel.path_offset, 0)
        self.assertEqual(myModel.row, 123)
        self.assertEqual(myModel.row_offset, 0)
        self.assertEqual(myModel.offline_storage_medium_id, '')
        self.assertEqual(myModel.online_storage_medium_id, '')

    def test_genericSensorproduct_update(self):
        """
        Tests GenericSensorProduct model update
        """
        myModel = GenericSensorProductF.create()

        myModel.__dict__.update(**{
            'product_acquisition_start': datetime(2008, 1, 1, 12, 00),
            'product_acquisition_end': datetime(2008, 1, 1, 13, 00),
            'geometric_accuracy_mean': 50.0,
            'geometric_accuracy_1sigma': 20.0,
            'geometric_accuracy_2sigma': 30.0,
            'radiometric_signal_to_noise_ratio': 5.0,
            'radiometric_percentage_error': 10.0,
            'spectral_accuracy': 20.0,
            'orbit_number': 1,
            'path': 321,
            'path_offset': 0,
            'row': 123,
            'row_offset': 0,
            'offline_storage_medium_id': '',
            'online_storage_medium_id': '',
        })

        myModel.save()

        self.assertEqual(
            myModel.product_acquisition_start, datetime(2008, 1, 1, 12, 00))

        self.assertEqual(
            myModel.product_acquisition_end, datetime(2008, 1, 1, 13, 00))

        self.assertEqual(myModel.geometric_accuracy_mean, 50.0)
        self.assertEqual(myModel.geometric_accuracy_1sigma, 20.0)
        self.assertEqual(myModel.geometric_accuracy_2sigma, 30.0)
        self.assertEqual(myModel.radiometric_signal_to_noise_ratio, 5.0)
        self.assertEqual(myModel.radiometric_percentage_error, 10.0)
        self.assertEqual(myModel.spectral_accuracy, 20.0)
        self.assertEqual(myModel.orbit_number, 1)
        self.assertEqual(myModel.path, 321)
        self.assertEqual(myModel.path_offset, 0)
        self.assertEqual(myModel.row, 123)
        self.assertEqual(myModel.row_offset, 0)
        self.assertEqual(myModel.offline_storage_medium_id, '')
        self.assertEqual(myModel.online_storage_medium_id, '')

    def test_genericSensorproduct_getMetadataDict(self):
        """
        Tests GenericSensorProduct model getMetadataDict method
        """

        myModel = GenericSensorProductF.create()

        self.assertRaises(AttributeError, myModel.getMetadataDict)

    def test_genericSensorproduct_productDirectory(self):
        """
        Tests GenericSensorProduct model _productDirectory method
        """

        myModel = GenericSensorProductF.create()

        self.assertRaises(AttributeError, myModel._productDirectory)

    def test_genericSensorproduct_thumbnailDirectory(self):
        """
        Tests GenericSensorProduct model _thumbnailDirectory method
        """
        myModel = GenericSensorProductF.create()

        self.assertRaises(AttributeError, myModel._thumbnailDirectory)
