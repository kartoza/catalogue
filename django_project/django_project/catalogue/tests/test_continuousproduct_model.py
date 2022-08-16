"""
SANSA-EO Catalogue - ContinuousProduct_model - implements basic CRUD unittests

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

from .model_factories import ContinuousProductF


class TestContinuousProductCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_ContinuousProduct_create(self):
        """
        Tests ContinuousProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """
        myModel = ContinuousProductF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_ContinuousProduct_delete(self):
        """
        Tests ContinuousProduct model delete
        """
        myModel = ContinuousProductF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ContinuousProduct_read(self):
        """
        Tests ContinuousProduct model read
        """

        myModel = ContinuousProductF.create(**{
            'range_min': 0.2,
            'range_max': 99.8
        })

        self.assertEqual(myModel.range_min, 0.2)
        self.assertEqual(myModel.range_max, 99.8)

    def test_ContinuousProduct_update(self):
        """
        Tests ContinuousProduct model update
        """

        myModel = ContinuousProductF.create()

        myModel.__dict__.update(**{
            'range_min': 0.2,
            'range_max': 99.8
        })

        myModel.save()

        self.assertEqual(myModel.range_min, 0.2)
        self.assertEqual(myModel.range_max, 99.8)
