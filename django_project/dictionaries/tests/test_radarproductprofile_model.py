"""
SANSA-EO Catalogue - Dictionaries RadarProductProfile - basic CRUD
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
    RadarProductProfileF, SatelliteInstrumentF, ImagingModeF
)


class TestRadarProductProfileCRUD(TestCase):
    """
    Tests RadarProductProfile model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_RadarProductProfile_create(self):
        """
        Tests RadarProductProfile model creation
        """
        myModel = RadarProductProfileF.create()

        self.assertTrue(myModel.pk is not None)

    def test_RadarProductProfile_delete(self):
        """
        Tests RadarProductProfile model delete
        """
        myModel = RadarProductProfileF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_RadarProductProfile_read(self):
        """
        Tests RadarProductProfile model read
        """

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })
        myImgMode = ImagingModeF.create(**{
            'name': 'Temp Imaging mode'
        })

        myModel = RadarProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'imaging_mode': myImgMode
        })

        self.assertEqual(
            myModel.satellite_instrument.operator_abbreviation, 'SATIN 1')

        self.assertEqual(myModel.imaging_mode.name, 'Temp Imaging mode')

    def test_RadarProductProfile_update(self):
        """
        Tests RadarProductProfile model update
        """

        myModel = RadarProductProfileF.create()

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })
        myImgMode = ImagingModeF.create(**{
            'name': 'Temp Imaging mode'
        })

        myModel.satellite_instrument = mySatInst
        myModel.imaging_mode = myImgMode

        myModel.save()

        self.assertEqual(
            myModel.satellite_instrument.operator_abbreviation, 'SATIN 1')

        self.assertEqual(myModel.imaging_mode.name, 'Temp Imaging mode')

    def test_RadarProductProfile_repr(self):
        """
        Tests RadarProductProfile model repr
        """

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })
        myImgMode = ImagingModeF.create(**{
            'name': 'Temp Imaging mode',
            'polarization': 'VV'
        })

        myModel = RadarProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'imaging_mode': myImgMode
        })

        self.assertEqual(
            str(myModel), 'SATIN 1 -- Temp Imaging mode (VV)')
