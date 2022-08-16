"""
SANSA-EO Catalogue - OrdinalProduct_model - implements basic CRUD unittests

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

from .model_factories import OrdinalProductF


class TestOrdinalProductCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OrdinalProduct_create(self):
        """
        Tests OrdinalProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """

        myModel = OrdinalProductF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_OrdinalProduct_delete(self):
        """
        Tests OrdinalProduct model delete
        """
        myModel = OrdinalProductF.create()
        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_OrdinalProduct_read(self):
        """
        Tests OrdinalProduct model read
        """
        myModel = OrdinalProductF.create(**{
            'class_count': 3,
            'confusion_matrix': '1,2,3,4,5',
            'kappa_score': None
        })

        self.assertEqual(myModel.class_count, 3)
        self.assertEqual(myModel.confusion_matrix, '1,2,3,4,5')
        self.assertEqual(myModel.kappa_score, None)

    def test_OrdinalProduct_update(self):
        """
        Tests OrdinalProduct model update
        """
        myModel = OrdinalProductF.create()

        myModel.__dict__.update(**{
            'class_count': 3,
            'confusion_matrix': '1,2,3,4,5',
            'kappa_score': None
        })

        self.assertEqual(myModel.class_count, 3)
        self.assertEqual(myModel.confusion_matrix, '1,2,3,4,5')
        self.assertEqual(myModel.kappa_score, None)
