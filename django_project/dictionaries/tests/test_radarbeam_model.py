"""
SANSA-EO Catalogue - Dictionaries RadarBeam - basic CRUD unittests

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

from .model_factories import InstrumentTypeF, RadarBeamF


class TestRadarBeamCRUD(TestCase):
    """
    Tests RadarBeam model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_RadarBeam_create(self):
        """
        Tests RadarBeam model creation
        """
        myModel = RadarBeamF.create()

        self.assertTrue(myModel.pk is not None)

    def test_RadarBeam_delete(self):
        """
        Tests RadarBeam model delete
        """
        myModel = RadarBeamF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_RadarBeam_read(self):
        """
        Tests RadarBeam model read
        """

        myInstrumentType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'OPNTY 1',
        })
        myModel = RadarBeamF.create(**{
            'band_name': 'New band name',
            'wavelength_cm': 40,
            'instrument_type': myInstrumentType
        })

        self.assertEqual(myModel.band_name, 'New band name')

        self.assertEqual(myModel.wavelength_cm, 40)

        self.assertEqual(
            myModel.instrument_type.operator_abbreviation, 'OPNTY 1')

    def test_RadarBeam_update(self):
        """
        Tests RadarBeam model update
        """

        myModel = RadarBeamF.create()

        myInstrumentType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'OPNTY 1',
        })

        myModel.__dict__.update(**{
            'band_name': 'New band name',
            'wavelength_cm': 40
        })
        myModel.instrument_type = myInstrumentType

        myModel.save()

        self.assertEqual(myModel.band_name, 'New band name')

        self.assertEqual(myModel.wavelength_cm, 40)

        self.assertEqual(
            myModel.instrument_type.operator_abbreviation, 'OPNTY 1')

    def test_RadarBeam_repr(self):
        """
        Tests RadarBeam model repr
        """
        myModel = RadarBeamF.create(**{
            'band_name': 'New Band',
            'wavelength_cm': 20
        })

        self.assertEqual(str(myModel), 'New Band (20)')
