"""
SANSA-EO Catalogue - radarproduct_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '26/07/2013'
__copyright__ = 'South African National Space Agency'


from django.test import TestCase

from .model_factories import RadarProductF


class TestRadarProductCRUD(TestCase):
    """
    Tests models.
    """
    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_RadarProduct_create(self):
        """
        Tests RadarProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """
        # myNewData = {
        #     #specific model attributes
        #     'imaging_mode': None,
        #     'polarising_list': None,
        #     'azimuth_range_resolution': None,
        #     'look_direction': 'L',
        #     'calibration': None,
        #     'slant_range_resolution': None,
        #     'orbit_direction': 'A',
        #     'polarising_mode': 'S',
        #     'incidence_angle': None,
        #     'antenna_receive_configuration': 'V'
        # }
        myModel = RadarProductF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_RadarProduct_delete(self):
        """
        Tests RadarProduct model delete
        """
        myModel = RadarProductF.create()

        myModel.delete()

        self.assertTrue(myModel.pk is None)

    def test_RadarProduct_read(self):
        """
        Tests RadarProduct model read
        """

        myModel = RadarProductF.create(**{
            'imaging_mode': None,
            'polarising_list': None,
            'azimuth_range_resolution': None,
            'look_direction': 'L',
            'calibration': None,
            'slant_range_resolution': None,
            'orbit_direction': 'A',
            'polarising_mode': 'S',
            'incidence_angle': None,
            'antenna_receive_configuration': 'V'
        })

        self.assertEqual(myModel.imaging_mode, None)
        self.assertEqual(myModel.polarising_list, None)
        self.assertEqual(myModel.azimuth_range_resolution, None)
        self.assertEqual(myModel.look_direction, 'L')
        self.assertEqual(myModel.calibration, None)
        self.assertEqual(myModel.slant_range_resolution, None)
        self.assertEqual(myModel.orbit_direction, 'A')
        self.assertEqual(myModel.polarising_mode, 'S')
        self.assertEqual(myModel.incidence_angle, None)
        self.assertEqual(myModel.antenna_receive_configuration, 'V')

    def test_RadarProduct_update(self):
        """
        Tests RadarProduct model update
        """
        myModel = RadarProductF.create()

        myModel.__dict__.update(**{
            'imaging_mode': None,
            'polarising_list': None,
            'azimuth_range_resolution': None,
            'look_direction': 'L',
            'calibration': None,
            'slant_range_resolution': None,
            'orbit_direction': 'A',
            'polarising_mode': 'S',
            'incidence_angle': None,
            'antenna_receive_configuration': 'V'
        })

        self.assertEqual(myModel.imaging_mode, None)
        self.assertEqual(myModel.polarising_list, None)
        self.assertEqual(myModel.azimuth_range_resolution, None)
        self.assertEqual(myModel.look_direction, 'L')
        self.assertEqual(myModel.calibration, None)
        self.assertEqual(myModel.slant_range_resolution, None)
        self.assertEqual(myModel.orbit_direction, 'A')
        self.assertEqual(myModel.polarising_mode, 'S')
        self.assertEqual(myModel.incidence_angle, None)
        self.assertEqual(myModel.antenna_receive_configuration, 'V')
