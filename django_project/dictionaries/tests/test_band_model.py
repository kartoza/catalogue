"""
SANSA-EO Catalogue - Dictionaries Band - basic CRUD unittests

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

from .model_factories import BandF, InstrumentTypeF


class TestBandCRUD(TestCase):
    """
    Tests Band model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_Band_create(self):
        """
        Tests Band model creation
        """
        myModel = BandF.create()

        self.assertTrue(myModel.pk is not None)

    def test_Band_delete(self):
        """
        Tests Band model delete
        """
        myModel = BandF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Band_read(self):
        """
        Tests Band model read
        """

        myInstType = InstrumentTypeF.create(**{'name': 'Cool Instrument Type'})
        myModel = BandF.create(**{
            'band_name': 'Cool band',
            'band_abbr': 'CB',
            'band_number': 1,
            'min_wavelength_nm': 200,
            'max_wavelength_nm': 400,
            'pixelsize_resampled_m': 30,
            'pixelsize_acquired_m': 28,
            'instrument_type': myInstType
        })

        self.assertEqual(myModel.band_name, 'Cool band')

        self.assertEqual(myModel.band_abbr, 'CB')

        self.assertEqual(myModel.band_number, 1)

        self.assertEqual(myModel.min_wavelength_nm, 200)

        self.assertEqual(myModel.max_wavelength_nm, 400)

        self.assertEqual(myModel.pixelsize_resampled_m, 30)

        self.assertEqual(myModel.pixelsize_acquired_m, 28)

        self.assertEqual(myModel.instrument_type.name, 'Cool Instrument Type')

    def test_Band_update(self):
        """
        Tests Band model update
        """

        myInstType = InstrumentTypeF.create(**{'name': 'Cool Instrument Type'})
        myModel = BandF.create()

        myModel.__dict__.update(**{
            'band_name': 'Cool band',
            'band_abbr': 'CB',
            'band_number': 1,
            'min_wavelength_nm': 200,
            'max_wavelength_nm': 400,
            'pixelsize_resampled_m': 30,
            'pixelsize_acquired_m': 28
        })
        myModel.instrument_type = myInstType
        myModel.save()

        self.assertEqual(myModel.band_name, 'Cool band')

        self.assertEqual(myModel.band_abbr, 'CB')

        self.assertEqual(myModel.band_number, 1)

        self.assertEqual(myModel.min_wavelength_nm, 200)

        self.assertEqual(myModel.max_wavelength_nm, 400)

        self.assertEqual(myModel.pixelsize_resampled_m, 30)

        self.assertEqual(myModel.pixelsize_acquired_m, 28)

        self.assertEqual(myModel.instrument_type.name, 'Cool Instrument Type')

    def test_Band_repr(self):
        """
        Tests Band model repr
        """

        myModel = BandF.create(**{
            'band_name': 'Cool band',
            'min_wavelength_nm': 200,
            'max_wavelength_nm': 400,
            'pixelsize_resampled_m': 30
        })

        self.assertEqual(
            str(myModel), 'Cool band (200 400) 30')
