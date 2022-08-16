"""
SANSA-EO Catalogue - placeType_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '20/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import PlaceTypeF


class PlaceTypeCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_placeType_create(self):
        """
        Tests PlaceType model creation
        """

        myModel = PlaceTypeF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_placeType_delete(self):
        """
        Tests PlaceType model delete
        """
        myModel = PlaceTypeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_placeType_read(self):
        """
        Tests PlaceType model read
        """
        myModel = PlaceTypeF.create(**{
            'name': 'Sample Place Type'
        })

        self.assertEqual(myModel.name, 'Sample Place Type')

    def test_placeType_update(self):
        """
        Tests PlaceType model update
        """
        myModel = PlaceTypeF.create()

        myModel.__dict__.update({
            'name': 'Sample Place Type'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Sample Place Type')

    def test_PlaceType_repr(self):
        """
        Tests PlaceType model representation
        """
        myModel = PlaceTypeF.create(**{
            'name': 'Super place type'
        })

        self.assertEqual(str(myModel), 'Super place type')
