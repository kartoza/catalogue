"""
SANSA-EO Catalogue - genericsensorproduct_model - implements basic CRUD unittests

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
from catalogue.models import GenericSensorProduct
from datetime import datetime

class GenericSensorProductCRUD_Test(TestCase):
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
        #'test_opticalproduct.json',
        #'test_radarproduct.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_genericSensorproduct_create(self):
        """
        Tests GenericSensorProduct model creation

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
            #specific model attributes
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
            'row': 404
        }
        myModel = GenericSensorProduct(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_genericSensorproduct_read(self):
        """
        Tests GenericSensorProduct model read
        """
        myModelPK = 1934163
        myExpectedModelData = {
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
            'product_acquisition_start': datetime.strptime('1986-06-19 08:46:32', '%Y-%m-%d %H:%M:%S'),
            'row': 404
        }
        myModel = GenericSensorProduct.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_genericSensorproduct_update(self):
        """
        Tests GenericSensorProduct model update
        """
        myModelPK = 1934163
        myModel = GenericSensorProduct.objects.get(pk=myModelPK)
        myNewModelData = {
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
            'row': 404
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_genericSensorproduct_delete(self):
        """
        Tests GenericSensorProduct model delete

        This test FAILS because current application doesn't support
        cascade delete on inherited models - Story #227
        """
        myModelPK = 1934163
        myModel = GenericSensorProduct.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_genericSensorproduct_getMetadataDict(self):
        """
        Tests GenericSensorProduct model getMetadataDict method
        """
        myModelPKs = [1960810, 1001218]
        myExpResults = [{'product_date': '1987-04-28T08:23:29', 'institution_address': u'Hartebeeshoek',
        'institution_region': '', 'image_quality_code': u'Unknown', 'vertical_cs': u'ORBIT', 'processing_level_code': u'3Ba',
        'file_identifier': u'S1-_HRV_P--_S1C2_0136_00_0388_00_870428_082329_1B--_ORBIT-',
        'spatial_coverage': '31.2155,-19.2338 31.3336,-18.7048 32.0064,-18.8 31.8906,-19.3289 31.2155,-19.2338',
        'bbox_east': 32.00640000000004, 'md_abstract': '', 'md_product_date': '1987-04-28T08:23:29',
        'institution_city': u'Gauteng', 'bbox_north': -18.704799999999977, 'institution_name': u'Satellite Applications Centre',
        'institution_country': u'South Africa', 'bbox_west': 31.21550000000002, 'institution_postcode': u'0000',
        'md_data_identification': u'HRV-1:Camera 2', 'bbox_south': -19.328899999999976},
         {'product_date': '1992-07-03T08:29:48', 'institution_address': u'Hartebeeshoek',
         'institution_region': '', 'image_quality_code': u'Unknown', 'vertical_cs': u'UTM35S', 'processing_level_code': u'2A',
         'file_identifier': u'S1-_Pan_P--_CAM2_0126_00_0387_00_920703_082948_L2A-_UTM35S',
         'spatial_coverage': '26.447275,-18.739992 27.00868,-18.826267 27.134314,-18.296593 26.574713,-18.210571 26.447275,-18.739992',
         'bbox_east': 27.134314, 'md_abstract': '', 'md_product_date': '1992-07-03T08:29:48',
         'institution_city': u'Gauteng', 'bbox_north': -18.210571, 'institution_name': u'Satellite Applications Centre',
         'institution_country': u'South Africa', 'bbox_west': 26.447275, 'institution_postcode': u'0000',
         'md_data_identification': u'Xs:P', 'bbox_south': -18.826267}]

        for idx, PK in enumerate(myModelPKs):
            myModel = GenericSensorProduct.objects.get(pk=PK)
            myRes = myModel.getMetadataDict()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s getMetadataDict:' % PK))
