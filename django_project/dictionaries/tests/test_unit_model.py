"""
SANSA-EO Catalogue - unit_model - implements basic CRUD unittests

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
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from model_factories import UnitF


class UnitCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_unit_create(self):
        """
        Tests Unit model creation
        """
        myModel = UnitF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_unit_delete(self):
        """
        Tests Unit model delete
        """
        myModel = UnitF.create()
        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_unit_read(self):
        """
        Tests Unit model read
        """
        myModel = UnitF.create(**{
            'name': 'Sample Unit',
            'abbreviation': 'SMPUNT'
        })

        self.assertEqual(myModel.name, 'Sample Unit')
        self.assertEqual(myModel.abbreviation, 'SMPUNT')

    def test_unit_update(self):
        """
        Tests Unit model update
        """
        myModel = UnitF.create()

        myModel.__dict__.update({
            'name': 'Sample Unit',
            'abbreviation': 'SMPUNT'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Sample Unit')
        self.assertEqual(myModel.abbreviation, 'SMPUNT')

    def test_unit_repr(self):
        """
        Tests Unit model repr
        """
        myModel = UnitF.create(**{
            'name': 'Sample Unit',
            'abbreviation': 'SMPUNT'
        })

        self.assertEqual(unicode(myModel), 'Sample Unit')
