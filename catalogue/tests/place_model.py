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
__version__ = '0.1'
__date__ = '20/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import Place


class PlaceCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_placetype.json',
        'test_place.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_place_create(self):
        """
        Tests Place model creation
        """
        myNewModelData = {
            'name': 'Unknown Place',
            'place_type_id': 1,
            'geometry': 'POINT (25.356 -32.201)'
        }

        myModel = Place(**myNewModelData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_place_read(self):
        """
        Tests Place model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'name': 'Sample Place',
            'place_type_id': 1,
            'geometry': '0101000020E6100000F0C039234A5B3540106A4DF38E333BC0'
        }
        myModel = Place.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                    message='For key "%s"' % key))

    def test_place_update(self):
        """
        Tests Place model update
        """
        myModelPK = 1
        myModel = Place.objects.get(pk=myModelPK)
        myNewModelData = {
            'name': 'Unknown Place',
            'place_type_id': 1,
            'geometry': 'POINT (25.3560000000000016 -32.2010000000000005)'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                message='For key "%s"' % key))

    def test_place_delete(self):
        """
        Tests Place model delete
        """
        myModelPK = 1
        myModel = Place.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
