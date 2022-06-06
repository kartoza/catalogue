"""
SANSA-EO Catalogue - Dictionaries InstrumentTypeProcessingLevel - basic CRUD
unittests

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
__date__ = '23/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import (
    InstrumentTypeProcessingLevelF, InstrumentTypeF, ProcessingLevelF
)


class TestInstrumentTypeProcessingLevelCRUD(TestCase):
    """
    Tests InstrumentTypeProcessingLevel model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_InstrumentTypeProcessingLevel_create(self):
        """
        Tests InstrumentTypeProcessingLevel model creation
        """
        myModel = InstrumentTypeProcessingLevelF.create()

        self.assertTrue(myModel.pk is not None)

    def test_InstrumentTypeProcessingLevel_delete(self):
        """
        Tests InstrumentTypeProcessingLevel model delete
        """
        myModel = InstrumentTypeProcessingLevelF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_InstrumentTypeProcessingLevel_read(self):
        """
        Tests InstrumentTypeProcessingLevel model read
        """

        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'NIS'
        })
        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'PL1'
        })

        myModel = InstrumentTypeProcessingLevelF.create(**{
            'instrument_type': myInstType,
            'processing_level': myProcLevel,
            'operator_processing_level_name': 'OP Name 1',
            'operator_processing_level_abbreviation': 'OPN1'
        })

        self.assertEqual(myModel.instrument_type.operator_abbreviation, 'NIS')

        self.assertEqual(myModel.processing_level.abbreviation, 'PL1')

        self.assertEqual(myModel.operator_processing_level_name, 'OP Name 1')

        self.assertEqual(
            myModel.operator_processing_level_abbreviation, 'OPN1')

    def test_InstrumentTypeProcessingLevel_update(self):
        """
        Tests InstrumentTypeProcessingLevel model update
        """
        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'NIS'
        })
        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'PL1'
        })

        myModel = InstrumentTypeProcessingLevelF.create()

        myModel.__dict__.update(**{
            'operator_processing_level_name': 'OP Name 1',
            'operator_processing_level_abbreviation': 'OPN1'
        })

        myModel.processing_level = myProcLevel
        myModel.instrument_type = myInstType
        myModel.save()

        self.assertEqual(myModel.instrument_type.operator_abbreviation, 'NIS')

        self.assertEqual(myModel.processing_level.abbreviation, 'PL1')

        self.assertEqual(myModel.operator_processing_level_name, 'OP Name 1')

        self.assertEqual(
            myModel.operator_processing_level_abbreviation, 'OPN1')

    def test_InstrumentTypeProcessingLevel_repr(self):
        """
        Tests InstrumentTypeProcessingLevel model repr
        """
        myInstType = InstrumentTypeF.create(**{
            'name': 'IT name'
        })
        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'PL1'
        })

        myModel = InstrumentTypeProcessingLevelF.create(**{
            'instrument_type': myInstType,
            'processing_level': myProcLevel
        })

        self.assertEqual(str(myModel), 'IT name - PL1')
