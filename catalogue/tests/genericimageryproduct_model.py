"""
SANSA-EO Catalogue - genericimageryproduct_model - implements basic CRUD unittests

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
from catalogue.models import GenericImageryProduct


class GenericImageryProductCRUD_Test(TestCase):
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
        #'test_genericsensorproduct.json',
        #'test_opticalproduct.json',
        #'test_radarproduct.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_genericImageryproduct_create(self):
        """
        Tests GenericImageryProduct model creation

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
            #specific model attributes
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 3
        }
        myModel = GenericImageryProduct(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_genericImageryproduct_read(self):
        """
        Tests GenericImageryProduct model read
        """
        myModelPK = 1960810
        myExpectedModelData = {
            'radiometric_resolution': 16,
            'spatial_resolution_y': 10.0,
            'spatial_resolution_x': 10.0,
            'spatial_resolution': 10.0,
            'band_count': 1
        }
        myModel = GenericImageryProduct.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_genericImageryproduct_update(self):
        """
        Tests GenericImageryProduct model update
        """
        myModelPK = 1960810
        myModel = GenericImageryProduct.objects.get(pk=myModelPK)
        myNewModelData = {
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 1
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_genericImageryproduct_delete(self):
        """
        Tests GenericImageryProduct model delete

        This test FAILS because current application doesn't support
        cascade delete on inherited models - Story #227
        """
        myModelPK = 1960810
        myModel = GenericImageryProduct.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_genericImageryproduct_getMetadataDict(self):
        """
        Tests GenericImageryProduct model getMetadataDict method

        This test results in ERROR because method getMetadataDict method
        can't access acquisition_mode attribute which available in child
        model GenericSensorProduct - Story #228
        """
        myModelPKs = [1960810, 2143443, 1001218]
        # myExpResults = [{}, {}, {}]

        for idx, PK in enumerate(myModelPKs):
            myModel = GenericImageryProduct.objects.get(pk=PK)

            self.assertRaises(AttributeError, myModel.getMetadataDict)
            # myRes = myModel.getMetadataDict()

            # self.assertEqual(myRes, myExpResults[idx],
            #    simpleMessage(myRes, myExpResults[idx],
            #        message='Model PK %s getMetadataDict:' % PK))
