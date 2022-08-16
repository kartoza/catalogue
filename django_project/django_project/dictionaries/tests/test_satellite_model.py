"""
SANSA-EO Catalogue - Dictionaries Satellite - basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '18/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import SatelliteF, CollectionF, LicenseF


class TestSatelliteCRUD(TestCase):
    """
    Tests Satellite model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_Satellite_create(self):
        """
        Tests Satellite model creation
        """
        myModel = SatelliteF.create()

        self.assertTrue(myModel.pk is not None)

    def test_Satellite_delete(self):
        """
        Tests Satellite model delete
        """
        myModel = SatelliteF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Satellite_read(self):
        """
        Tests Satellite model read
        """
        myCollection = CollectionF.create(name='New Collection')
        myLicense = LicenseF.create(name='Free license')
        myModel = SatelliteF.create(**{
            'name': 'Satellite 1',
            'description': 'No description',
            'abbreviation': 'SAT1',
            'operator_abbreviation': 'SatOp1',
            'collection': myCollection,
            'launch_date': None,
            'status': None,
            'altitude_km': 10000,
            'orbit': '',
            'revisit_time_days': 90,
            'reference_url': '',
            'license_type': myLicense
        })

        self.assertEqual(myModel.name, 'Satellite 1')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.collection.name, 'New Collection')

        self.assertEqual(myModel.license_type.name, 'Free license')

        self.assertEqual(myModel.altitude_km, 10000)

    def test_Satellite_update(self):
        """
        Tests Satellite model update
        """
        myModel = SatelliteF.create()

        myCollection = CollectionF.create(name='New Collection')
        myLicense = LicenseF.create(name='Free license')
        myModel.__dict__.update(**{
            'name': 'Satellite 1',
            'description': 'No description',
            'abbreviation': 'SAT1',
            'operator_abbreviation': 'SatOp1',
            'launch_date': None,
            'status': None,
            'altitude_km': 10000,
            'orbit': '',
            'revisit_time_days': 90,
            'reference_url': ''
        })
        myModel.collection = myCollection
        myModel.license_type = myLicense
        myModel.save()

        self.assertEqual(myModel.name, 'Satellite 1')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.collection.name, 'New Collection')

        self.assertEqual(myModel.license_type.name, 'Free license')

        self.assertEqual(myModel.altitude_km, 10000)

    def test_Satellite_repr(self):
        """
        Tests Satellite model repr
        """
        myModel = SatelliteF.create(**{
            'operator_abbreviation': 'SatOp1'
        })

        self.assertEqual(str(myModel), 'SatOp1')
