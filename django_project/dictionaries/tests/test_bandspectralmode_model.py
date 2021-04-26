"""
SANSA-EO Catalogue - Dictionaries BandSpectralMode - basic CRUD unittests

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

from .model_factories import BandSpectralModeF, BandF, SpectralModeF


class TestBandSpectralModeCRUD(TestCase):
    """
    Tests BandSpectralMode model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_BandSpectralMode_create(self):
        """
        Tests BandSpectralMode model creation
        """
        myModel = BandSpectralModeF.create()

        self.assertTrue(myModel.pk is not None)

    def test_BandSpectralMode_delete(self):
        """
        Tests BandSpectralMode model delete
        """
        myModel = BandSpectralModeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_BandSpectralMode_read(self):
        """
        Tests BandSpectralMode model read
        """

        myBand = BandF.create(**{
            'band_name': 'Band 1'
        })
        mySpectralMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })

        myModel = BandSpectralModeF.create(**{
            'band': myBand,
            'spectral_mode': mySpectralMode,
        })

        self.assertEqual(myModel.band.band_name, 'Band 1')

        self.assertEqual(myModel.spectral_mode.name, 'New Spectral mode')

    def test_BandSpectralMode_update(self):
        """
        Tests BandSpectralMode model update
        """
        myBand = BandF.create(**{
            'band_name': 'Band 1'
        })
        mySpectralMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })

        myModel = SpectralModeF.create()

        myModel.band = myBand
        myModel.spectral_mode = mySpectralMode
        myModel.save()

        self.assertEqual(myModel.band.band_name, 'Band 1')

        self.assertEqual(myModel.spectral_mode.name, 'New Spectral mode')

    def test_BandSpectralMode_repr(self):
        """
        Tests BandSpectralMode model repr
        """

        myBand = BandF.create(**{
            'band_name': 'Band 1'
        })
        mySpectralMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })

        myModel = BandSpectralModeF.create(**{
            'band': myBand,
            'spectral_mode': mySpectralMode,
        })

        self.assertEqual(str(myModel), 'Band 1 (New Spectral mode)')
