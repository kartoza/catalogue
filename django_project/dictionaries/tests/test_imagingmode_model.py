"""
SANSA-EO Catalogue - Dictionaries ImagingMode - basic CRUD unittests

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

from .model_factories import ImagingModeF, RadarBeamF


class TestImagingModeCRUD(TestCase):
    """
    Tests ImagingMode model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_ImagingMode_create(self):
        """
        Tests ImagingMode model creation
        """
        myModel = ImagingModeF.create()

        self.assertTrue(myModel.pk is not None)

    def test_ImagingMode_delete(self):
        """
        Tests ImagingMode model delete
        """
        myModel = ImagingModeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ImagingMode_read(self):
        """
        Tests ImagingMode model read
        """

        myRadarBeam = RadarBeamF.create(**{
            'band_name': 'New Band',
            'wavelength_cm': 20
        })
        myModel = ImagingModeF.create(**{
            'radarbeam':  myRadarBeam,
            'name': 'New ImagingMode',
            'incidence_angle_min': 34,
            'incidence_angle_max': 36.9,
            'approximate_resolution_m': 30,
            'swath_width_km': 30,
            'number_of_looks': 3,
            'polarization': 'VV'
        })

        self.assertEqual(myModel.name, 'New ImagingMode')

        self.assertEqual(myModel.incidence_angle_min, 34)

        self.assertEqual(myModel.incidence_angle_max, 36.9)

        self.assertEqual(myModel.approximate_resolution_m, 30)

        self.assertEqual(myModel.swath_width_km, 30)

        self.assertEqual(myModel.number_of_looks, 3)

        self.assertEqual(myModel.polarization, 'VV')

        self.assertEqual(myModel.radarbeam.band_name, 'New Band')

    def test_ImagingMode_update(self):
        """
        Tests ImagingMode model update
        """

        myModel = ImagingModeF.create()

        myRadarBeam = RadarBeamF.create(**{
            'band_name': 'New Band',
            'wavelength_cm': 20
        })

        myModel.__dict__.update(**{
            'name': 'New ImagingMode',
            'incidence_angle_min': 34,
            'incidence_angle_max': 36.9,
            'approximate_resolution_m': 30,
            'swath_width_km': 30,
            'number_of_looks': 3,
            'polarization': 'VV'
        })
        myModel.radarbeam = myRadarBeam

        myModel.save()

        self.assertEqual(myModel.name, 'New ImagingMode')

        self.assertEqual(myModel.incidence_angle_min, 34)

        self.assertEqual(myModel.incidence_angle_max, 36.9)

        self.assertEqual(myModel.approximate_resolution_m, 30)

        self.assertEqual(myModel.swath_width_km, 30)

        self.assertEqual(myModel.number_of_looks, 3)

        self.assertEqual(myModel.polarization, 'VV')

        self.assertEqual(myModel.radarbeam.band_name, 'New Band')

    def test_ImagingMode_repr(self):
        """
        Tests ImagingMode model repr
        """
        myModel = ImagingModeF.create(**{
            'name': 'New Imaging Mode',
            'polarization': 'HV'
        })

        self.assertEqual(
            str(myModel), 'New Imaging Mode (HV)')
