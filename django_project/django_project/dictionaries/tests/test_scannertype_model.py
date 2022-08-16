"""
SANSA-EO Catalogue - Dictionaries ScannerType - basic CRUD unittests

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

from .model_factories import ScannerTypeF


class TestScannerTypeCRUD(TestCase):
    """
    Tests ScannerType model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_ScannerType_create(self):
        """
        Tests ScannerType model creation
        """
        myModel = ScannerTypeF.create()

        self.assertTrue(myModel.pk is not None)

    def test_ScannerType_delete(self):
        """
        Tests ScannerType model delete
        """
        myModel = ScannerTypeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ScannerType_read(self):
        """
        Tests ScannerType model read
        """

        myModel = ScannerTypeF.create(**{
            'name': 'New ScannerType 1',
            'description': '',
            'abbreviation': 'NST1'
        })

        self.assertEqual(myModel.name, 'New ScannerType 1')

        self.assertEqual(myModel.description, '')

        self.assertEqual(myModel.abbreviation, 'NST1')

    def test_ScannerType_update(self):
        """
        Tests ScannerType model update
        """
        myModel = ScannerTypeF.create()

        myModel.__dict__.update(**{
            'name': 'New ScannerType 1',
            'description': '',
            'abbreviation': 'NST1'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'New ScannerType 1')

        self.assertEqual(myModel.description, '')

        self.assertEqual(myModel.abbreviation, 'NST1')

    def test_ScannerType_repr(self):
        """
        Tests ScannerType model repr
        """
        myModel = ScannerTypeF.create(**{
            'abbreviation': 'NST1'
        })

        self.assertEqual(str(myModel), 'NST1')
