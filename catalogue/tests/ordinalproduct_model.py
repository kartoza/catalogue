"""
SANSA-EO Catalogue - OrdinalProduct_model - implements basic CRUD unittests

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
from catalogue.models import OrdinalProduct
from datetime import datetime


class OrdinalProductCRUD_Test(TestCase):
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
        'test_ordinalproduct.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OrdinalProduct_create(self):
        """
        Tests OrdinalProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """
        myNewData = {
            # we need to include 'parent' model attributes
            # without it parent models will no be created
            'product_date': '2111-01-01 12:00:00',
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
            'product_id': 'S1-_HRV_X--_S1C2_0120_00_0404_00_110101_095632_1B--_ORBIT-',
            #specific model attributes
            'class_count': 3,
            'confusion_matrix': '1,2,3,4,5',
            'kappa_score': None
        }
        myModel = OrdinalProduct(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_OrdinalProduct_read(self):
        """
        Tests OrdinalProduct model read
        """
        myModelPK = 55000001
        myExpectedModelData = {
            'class_count': 3,
            'confusion_matrix': '1,2,3,4,5',
            'kappa_score': None
        }
        #import ipdb;ipdb.set_trace()
        myModel = OrdinalProduct.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_OrdinalProduct_update(self):
        """
        Tests OrdinalProduct model update
        """
        myModelPK = 55000001
        myModel = OrdinalProduct.objects.get(pk=myModelPK)
        myNewModelData = {
            'class_count': 5,
            'confusion_matrix': '1,2,4,5,3',
            'kappa_score': 1.32
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_OrdinalProduct_delete(self):
        """
        Tests OrdinalProduct model delete

        This test FAILS because current application doesn't support
        cascade delete on inherited models - Story #227
        """
        myModelPK = 55000001
        myModel = OrdinalProduct.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
