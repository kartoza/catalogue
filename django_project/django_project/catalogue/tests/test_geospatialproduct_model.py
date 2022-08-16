"""
SANSA-EO Catalogue - geospatialproduct_model - implements basic CRUD unittests

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
__date__ = '26/07/2013'
__copyright__ = 'South African National Space Agency'


from django.test import TestCase

from .model_factories import GeospatialProductF


class TestGeospatialProductCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_GeospatialProduct_create(self):
        """
        Tests GeospatialProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """

        myModel = GeospatialProductF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_GeospatialProduct_delete(self):
        """
        Tests GeospatialProduct model delete
        """
        myModel = GeospatialProductF.create()
        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_GeospatialProduct_read(self):
        """
        Tests GeospatialProduct model read
        """

        myModel = GeospatialProductF.create(**{
            'name': 'Sample geospatialproduct',
            'description': 'Sample description',
            'processing_notes': None,
            'equivalent_scale': None,
            'data_type': None,
            'temporal_extent_start': '2100-01-01 12:00:00',
            'temporal_extent_end': None
        })

        self.assertEqual(myModel.name, 'Sample geospatialproduct')
        self.assertEqual(myModel.description, 'Sample description')
        self.assertEqual(myModel.processing_notes, None)
        self.assertEqual(myModel.equivalent_scale, None)
        self.assertEqual(myModel.data_type, None)
        self.assertEqual(myModel.temporal_extent_start, '2100-01-01 12:00:00')
        self.assertEqual(myModel.temporal_extent_end, None)

    def test_GeospatialProduct_update(self):
        """
        Tests GeospatialProduct model update
        """

        myModel = GeospatialProductF.create()

        myModel.__dict__.update(**{
            'name': 'Sample geospatialproduct',
            'description': 'Sample description',
            'processing_notes': None,
            'equivalent_scale': None,
            'data_type': None,
            'temporal_extent_start': '2100-01-01 12:00:00',
            'temporal_extent_end': None
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Sample geospatialproduct')
        self.assertEqual(myModel.description, 'Sample description')
        self.assertEqual(myModel.processing_notes, None)
        self.assertEqual(myModel.equivalent_scale, None)
        self.assertEqual(myModel.data_type, None)
        self.assertEqual(myModel.temporal_extent_start, '2100-01-01 12:00:00')
        self.assertEqual(myModel.temporal_extent_end, None)
