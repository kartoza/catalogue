"""
SANSA-EO Catalogue - place_model - implements basic CRUD unittests

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

from model_factories import PlaceF


class PlaceCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_place_create(self):
        """
        Tests Place model creation
        """
        myModel = PlaceF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_place_delete(self):
        """
        Tests Place model delete
        """
        myModel = PlaceF.create()
        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_place_read(self):
        """
        Tests Place model read
        """

        myModel = PlaceF.create(**{
            "name": "Super place",
            "geometry": "POINT (21.3566000000000145 -27.2013999999999783)"
        })

        self.assertEqual(myModel.name, 'Super place')
        self.assertEqual(
            myModel.geometry.hex, '0101000000F0C039234A5B3540106A4DF38E333BC0')

    def test_place_update(self):
        """
        Tests Place model update
        """

        myModel = PlaceF.create()

        myModel.__dict__.update({
            "name": "Super place",
            "geometry": "POINT (21.3566000000000145 -27.2013999999999783)"
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Super place')
        self.assertEqual(
            myModel.geometry.hex, '0101000000F0C039234A5B3540106A4DF38E333BC0')

    def test_Place_repr(self):
        """
        Tests Place model representation
        """
        myModel = PlaceF.create(**{
            'name': 'Super place'
        })

        self.assertEqual(unicode(myModel), 'Super place')
