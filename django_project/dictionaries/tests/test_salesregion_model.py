"""
SANSA-EO Catalogue - Dictionaries SalesRegion - basic CRUD unittests

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
__date__ = '04/02/2014'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import SalesRegionF


class TestSalesRegionCRUD(TestCase):
    """
    Tests SalesRegion model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SalesRegion_create(self):
        """
        Tests SalesRegion model creation
        """
        myModel = SalesRegionF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SalesRegion_delete(self):
        """
        Tests SalesRegion model delete
        """
        myModel = SalesRegionF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SalesRegion_read(self):
        """
        Tests SalesRegion model read
        """

        myModel = SalesRegionF.create(**{
            'abbreviation': 'SR',
            'name': 'SuperRegion',
        })

        self.assertEqual(myModel.name, 'SuperRegion')

        self.assertEqual(myModel.abbreviation, 'SR')

    def test_SalesRegion_update(self):
        """
        Tests SalesRegion model update
        """

        myModel = SalesRegionF.create()

        myModel.__dict__.update(**{
            'abbreviation': 'SR',
            'name': 'SuperRegion'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'SuperRegion')

        self.assertEqual(myModel.abbreviation, 'SR')

    def test_SalesRegion_repr(self):
        """
        Tests SalesRegion model repr
        """

        myModel = SalesRegionF.create(**{
            'abbreviation': 'SR'
        })

        self.assertEqual(str(myModel), 'SR')
