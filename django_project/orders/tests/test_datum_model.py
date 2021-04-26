"""
SANSA-EO Catalogue - Datum_model - implements basic CRUD unittests

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
__date__ = '31/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import DatumF


class DatumCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Datum_create(self):
        """
        Tests Datum model creation
        """
        myModel = DatumF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_Datum_delete(self):
        """
        Tests Datum model delete
        """
        myModel = DatumF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Datum_read(self):
        """
        Tests Datum model read
        """
        myModel = DatumF.create(**{
            'name': 'WGS84'
        })

        self.assertEqual(myModel.name, 'WGS84')

    def test_Datum_update(self):
        """
        Tests Datum model update
        """

        myModel = DatumF.create()

        myModel.__dict__.update({
            'name': 'WGS84'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'WGS84')

    def test_Datum_repr(self):
        """
        Tests Datum model representation
        """
        myModel = DatumF.create(**{
            'name': 'WGS84'
        })
        self.assertEqual(str(myModel), 'WGS84')
