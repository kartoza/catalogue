"""
SANSA-EO Catalogue - Dictionaries InstrumentType - basic CRUD unittests

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
__date__ = '19/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import (
    InstrumentTypeF, ScannerTypeF, ProcessingLevelF, ReferenceSystemF
)


class TestInstrumentTypeCRUD(TestCase):
    """
    Tests InstrumentType model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_InstrumentType_create(self):
        """
        Tests InstrumentType model creation
        """
        myModel = InstrumentTypeF.create()

        self.assertTrue(myModel.pk is not None)

    def test_InstrumentType_delete(self):
        """
        Tests InstrumentType model delete
        """
        myModel = InstrumentTypeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_InstrumentType_read(self):
        """
        Tests InstrumentType model read
        """

        myScannerType = ScannerTypeF.create(abbreviation='NST1')
        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'TST1',
            'name': 'Test Processing Level 1',
        })
        myRefSystem = ReferenceSystemF.create(name='NewRefSystem')
        myModel = InstrumentTypeF.create(**{
            'name': 'New Instrument Type',
            'description': 'No description',
            'abbreviation': 'NTY 1',
            'operator_abbreviation': 'OPNTY 1',
            'is_radar': False,
            'is_taskable': False,
            'is_searchable': False,
            'scanner_type': myScannerType,
            'base_processing_level': myProcLevel,
            'default_processing_level': myProcLevel,
            'reference_system': myRefSystem,
            'swath_optical_km': 20,
            'band_count': 3
        })

        self.assertEqual(myModel.name, 'New Instrument Type')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NTY 1')

        self.assertEqual(myModel.operator_abbreviation, 'OPNTY 1')

        self.assertEqual(myModel.is_radar, False)

        self.assertEqual(myModel.is_taskable, False)

        self.assertEqual(myModel.is_searchable, False)

        self.assertEqual(myModel.scanner_type.abbreviation, 'NST1')

        self.assertEqual(myModel.base_processing_level.abbreviation, 'TST1')

        self.assertEqual(myModel.default_processing_level.abbreviation, 'TST1')

        self.assertEqual(myModel.reference_system.name, 'NewRefSystem')

        self.assertEqual(myModel.swath_optical_km, 20)

        self.assertEqual(myModel.band_count, 3)

    def test_InstrumentType_update(self):
        """
        Tests InstrumentType model update
        """

        myModel = InstrumentTypeF.create()

        myScannerType = ScannerTypeF.create(abbreviation='NST1')
        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'TST1',
            'name': 'Test Processing Level 1',
        })
        myRefSystem = ReferenceSystemF.create(name='NewRefSystem')

        myModel.__dict__.update(**{
            'name': 'New Instrument Type',
            'description': 'No description',
            'abbreviation': 'NTY 1',
            'operator_abbreviation': 'OPNTY 1',
            'is_radar': False,
            'is_taskable': False,
            'is_searchable': False,
            'swath_optical_km': 20,
            'band_count': 3
        })

        myModel.scanner_type = myScannerType
        myModel.base_processing_level = myProcLevel
        myModel.reference_system = myRefSystem

        myModel.save()

        self.assertEqual(myModel.name, 'New Instrument Type')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NTY 1')

        self.assertEqual(myModel.operator_abbreviation, 'OPNTY 1')

        self.assertEqual(myModel.is_radar, False)

        self.assertEqual(myModel.is_taskable, False)

        self.assertEqual(myModel.is_searchable, False)

        self.assertEqual(myModel.scanner_type.abbreviation, 'NST1')

        self.assertEqual(myModel.base_processing_level.abbreviation, 'TST1')

        self.assertEqual(myModel.reference_system.name, 'NewRefSystem')

        self.assertEqual(myModel.swath_optical_km, 20)

        self.assertEqual(myModel.band_count, 3)

    def test_InstrumentType_repr(self):
        """
        Tests InstrumentType model repr
        """
        myModel = InstrumentTypeF.create(**{
            'operator_abbreviation': 'INSTYPE1'
        })

        self.assertEqual(str(myModel), 'INSTYPE1')
