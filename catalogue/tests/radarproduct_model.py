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
__version__ = '0.1'
__date__ = '27/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import RadarProduct


class RadarProductCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_quality.json',
        'test_projection.json',
        'test_institution.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_radarproduct.json'
        ]

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
        myNewData = {
            # we need to include 'parent' model attributes
            # without it parent models will no be created
            'product_date': '2100-01-01 12:00:00',
            'spatial_coverage': 'POLYGON ((21.3566000000000145 -27.2013999999999783, 21.4955000000000496 -26.6752999999999929, 22.0914000000000215 -26.7661999999999978, 21.9554000000000542 -27.2926999999999964, 21.3566000000000145 -27.2013999999999783))',
            'projection_id': 89,
            'license_id': 1,
            'original_product_id': '11204048606190846322X',
            'local_storage_path': None,
            'creating_software_id': 1,
            'remote_thumbnail_url': '',
            'product_revision': None,
            'owner_id': 1,
            'metadata': '',
            'quality_id': 1,
            'processing_level_id': 16,
            'product_id': 'S1-_HRV_X--_S1C2_0120_00_0404_00_000101_084632_1B--_ORBIT-',
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 3,
            'product_acquisition_end': None,
            'acquisition_mode_id': 87,
            'path_offset': 0,
            'orbit_number': None,
            'radiometric_signal_to_noise_ratio': None,
            'geometric_accuracy_mean': None,
            'spectral_accuracy': None,
            'geometric_accuracy_2sigma': None,
            'radiometric_percentage_error': None,
            'row_offset': 0,
            'online_storage_medium_id': None,
            'geometric_accuracy_1sigma': None,
            'offline_storage_medium_id': None,
            'path': 120,
            'product_acquisition_start': '2100-01-01 12:05:00',
            'row': 404,
            #specific model attributes
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
        }
        myModel = RadarProduct(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_RadarProduct_read(self):
        """
        Tests RadarProduct model read
        """
        myModelPK = 6541
        myExpectedModelData = {
            'imaging_mode': None,
            'polarising_list': None,
            'azimuth_range_resolution': None,
            'look_direction': None,
            'calibration': None,
            'slant_range_resolution': None,
            'orbit_direction': None,
            'polarising_mode': None,
            'incidence_angle': None,
            'antenna_receive_configuration': None
        }
        myModel = RadarProduct.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_RadarProduct_update(self):
        """
        Tests RadarProduct model update
        """
        myModelPK = 6541
        myModel = RadarProduct.objects.get(pk=myModelPK)
        myNewModelData = {
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
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def Xtest_RadarProduct_delete(self):
        """
        Tests RadarProduct model delete

        This test FAILS because current application doesn't support
        cascade delete on inherited models - Story #227
        """
        myModelPK = 6541
        myModel = RadarProduct.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
