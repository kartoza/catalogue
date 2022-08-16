"""
SANSA-EO Catalogue - Dictionaries SatelliteInstrumentGroup - basic CRUD
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
__date__ = '19/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import (
    SatelliteInstrumentGroupF, SatelliteF, InstrumentTypeF
)


class TestSatelliteInstrumentGroupCRUD(TestCase):
    """
    Tests SatelliteInstrumentGroup model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SatelliteInstrumentGroup_create(self):
        """
        Tests SatelliteInstrumentGroup model creation
        """
        myModel = SatelliteInstrumentGroupF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SatelliteInstrumentGroup_delete(self):
        """
        Tests SatelliteInstrumentGroup model delete
        """
        myModel = SatelliteInstrumentGroupF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SatelliteInstrumentGroup_read(self):
        """
        Tests SatelliteInstrumentGroup model read
        """

        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'ITOP 1'
        })
        mySatellite = SatelliteF.create(**{
            'operator_abbreviation': 'ST 1'
        })

        myModel = SatelliteInstrumentGroupF.create(**{
            'instrument_type': myInstType,
            'satellite': mySatellite
        })

        self.assertEqual(
            myModel.instrument_type.operator_abbreviation, 'ITOP 1')

        self.assertEqual(
            myModel.satellite.operator_abbreviation, 'ST 1')

    def test_SatelliteInstrumentGroup_update(self):
        """
        Tests SatelliteInstrumentGroup model update
        """

        myModel = SatelliteInstrumentGroupF.create()

        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'ITOP 1'
        })
        mySatellite = SatelliteF.create(**{
            'operator_abbreviation': 'ST 1'
        })

        myModel.instrument_type = myInstType
        myModel.satellite = mySatellite

        myModel.save()

        self.assertEqual(
            myModel.instrument_type.operator_abbreviation, 'ITOP 1')

        self.assertEqual(
            myModel.satellite.operator_abbreviation, 'ST 1')

    def test_SatelliteInstrumentGroup_repr(self):
        """
        Tests SatelliteInstrumentGroup model repr
        """
        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'ITOP 1'
        })
        mySatellite = SatelliteF.create(**{
            'operator_abbreviation': 'ST 1'
        })

        myModel = SatelliteInstrumentGroupF.create(**{
            'instrument_type': myInstType,
            'satellite': mySatellite
        })

        self.assertEqual(
            str(myModel), 'ST 1 - ITOP 1')
