"""
SANSA-EO Catalogue - genericimageryproduct_model - implements basic CRUD
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


from django.test import TestCase

from .model_factories import GenericImageryProductF


class TestGenericImageryProductCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_genericImageryproduct_create(self):
        """
        Tests GenericImageryProduct model creation
        """
        myNewData = {
            #specific model attributes
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 3
        }
        myModel = GenericImageryProductF.create(**myNewData)

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_genericImageryproduct_delete(self):
        """
        Tests GenericImageryProduct model delete
        """
        myModel = GenericImageryProductF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_genericImageryproduct_read(self):
        """
        Tests GenericImageryProduct model read
        """

        myModel = GenericImageryProductF.create(**{
            #specific model attributes
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 3
        })

        self.assertEqual(myModel.radiometric_resolution, 16)

        self.assertEqual(myModel.spatial_resolution_y, 1.0)

        self.assertEqual(myModel.spatial_resolution_x, 1.0)

        self.assertEqual(myModel.spatial_resolution, 1.0)

        self.assertEqual(myModel.band_count, 3)

    def test_genericImageryproduct_update(self):
        """
        Tests GenericImageryProduct model update
        """

        myModel = GenericImageryProductF.create()

        myModel.__dict__.update(**{
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 3
        })

        myModel.save()

        self.assertEqual(myModel.radiometric_resolution, 16)

        self.assertEqual(myModel.spatial_resolution_y, 1.0)

        self.assertEqual(myModel.spatial_resolution_x, 1.0)

        self.assertEqual(myModel.spatial_resolution, 1.0)

        self.assertEqual(myModel.band_count, 3)

    def test_genericImageryproduct_getMetadataDict(self):
        """
        Tests GenericImageryProduct model getMetadataDict method

        This test results in ERROR because method getMetadataDict method
        can't access acquisition_mode attribute which available in child
        model GenericSensorProduct
        """

        myModel = GenericImageryProductF.create()

        self.assertRaises(AttributeError, myModel.getMetadataDict)

    def test_genericImageryproduct_getAbstract(self):
        """
        Tests GenericImageryProduct model getAbstract method
        """

        myModel = GenericImageryProductF.create()

        self.assertEqual(myModel.getAbstract(), '')
