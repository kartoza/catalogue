"""
SANSA-EO Catalogue - Dictionaries SpectralMode - basic CRUD unittests

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

from .model_factories import SpectralModeF, InstrumentTypeF, SpectralGroupF


class TestSpectralModeCRUD(TestCase):
    """
    Tests SpectralMode model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SpectralMode_create(self):
        """
        Tests SpectralMode model creation
        """
        myModel = SpectralModeF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SpectralMode_delete(self):
        """
        Tests SpectralMode model delete
        """
        myModel = SpectralModeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SpectralMode_read(self):
        """
        Tests SpectralMode model read
        """

        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'NIT 1'
        })
        mySpectralGrp = SpectralGroupF.create(**{
            'name': 'New Spectral group'
        })

        myModel = SpectralModeF.create(**{
            'name': 'New Spectral mode',
            'description': 'No description',
            'abbreviation': 'NSM',
            'instrument_type': myInstType,
            'spectralgroup': mySpectralGrp,
        })

        self.assertEqual(myModel.name, 'New Spectral mode')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NSM')

        self.assertEqual(
            myModel.instrument_type.operator_abbreviation, 'NIT 1')

        self.assertEqual(myModel.spectralgroup.name, 'New Spectral group')

    def test_SpectralMode_update(self):
        """
        Tests SpectralMode model update
        """
        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'NIT 1'
        })
        mySpectralGrp = SpectralGroupF.create(**{
            'name': 'New Spectral group'
        })

        myModel = SpectralModeF.create()

        myModel.__dict__.update(**{
            'name': 'New Spectral mode',
            'description': 'No description',
            'abbreviation': 'NSM',
        })
        myModel.spectralgroup = mySpectralGrp
        myModel.instrument_type = myInstType
        myModel.save()

        self.assertEqual(myModel.name, 'New Spectral mode')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NSM')

        self.assertEqual(
            myModel.instrument_type.operator_abbreviation, 'NIT 1')

        self.assertEqual(myModel.spectralgroup.name, 'New Spectral group')

    def test_SpectralMode_repr(self):
        """
        Tests SpectralMode model repr
        """

        myInstType = InstrumentTypeF.create(**{
            'name': 'NIT 1'
        })
        myModel = SpectralModeF.create(**{
            'name': 'New Spectral mode',
            'instrument_type': myInstType
        })

        self.assertEqual(
            str(myModel), 'New Spectral mode - NIT 1')
