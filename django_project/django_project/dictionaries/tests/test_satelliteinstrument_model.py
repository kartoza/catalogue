"""
SANSA-EO Catalogue - Dictionaries SatelliteInstrument - basic CRUD
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
__date__ = '22/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import (
    SatelliteInstrumentF, SatelliteInstrumentGroupF
)


class TestSatelliteInstrumentCRUD(TestCase):
    """
    Tests SatelliteInstrument model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SatelliteInstrument_create(self):
        """
        Tests SatelliteInstrument model creation
        """
        myModel = SatelliteInstrumentF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SatelliteInstrument_delete(self):
        """
        Tests SatelliteInstrument model delete
        """
        myModel = SatelliteInstrumentF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SatelliteInstrument_read(self):
        """
        Tests SatelliteInstrument model read
        """

        mySatInstGroup = SatelliteInstrumentGroupF.create()
        myModel = SatelliteInstrumentF.create(**{
            'name': 'SatInstrument',
            'description': 'No description',
            'abbreviation': 'SatInst1',
            'operator_abbreviation': 'SatInstOperator1',
            'satellite_instrument_group': mySatInstGroup
        })

        self.assertEqual(myModel.name, 'SatInstrument')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'SatInst1')

        self.assertEqual(myModel.operator_abbreviation, 'SatInstOperator1')

        self.assertTrue(myModel.satellite_instrument_group.pk is not None)

    def test_SatelliteInstrument_update(self):
        """
        Tests SatelliteInstrument model update
        """

        myModel = SatelliteInstrumentF.create()

        myModel.__dict__.update(**{
            'name': 'SatInstrument',
            'description': 'No description',
            'abbreviation': 'SatInst1',
            'operator_abbreviation': 'SatInstOperator1'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'SatInstrument')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'SatInst1')

        self.assertEqual(myModel.operator_abbreviation, 'SatInstOperator1')

    def test_SatelliteInstrument_repr(self):
        """
        Tests SatelliteInstrument model repr
        """

        myModel = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SatInstOperator1'
        })

        self.assertEqual(
            str(myModel), 'SatInstOperator1')
