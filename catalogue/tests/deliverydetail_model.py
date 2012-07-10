"""
SANSA-EO Catalogue - DeliveryDetail_model - implements basic CRUD unittests

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
__date__ = '09/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import DeliveryDetail


class DeliveryDetailCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_deliverydetail.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_DeliveryDetail_create(self):
        """
        Tests DeliveryDetail model creation
        """
        myNewData = {
            'user_id': 1,
            'processing_level_id': 1,
            'projection_id': 1,
            'datum_id': 1,
            'resampling_method_id': 1,
            'file_format_id': 1,
            'geometry': 'POLYGON ((17.5400390625000000 -32.0595703125000000, 20.8359375000000000 -32.4111328125000000, 20.3085937500000000 -35.1796875000000000, 17.8476562500000000 -34.6523437500000000, 17.5400390625000000 -32.0595703125000000))'
        }
        myModel = DeliveryDetail(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_DeliveryDetail_read(self):
        """
        Tests DeliveryDetail model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'user_id': 1,
            'processing_level_id': 1,
            'projection_id': 1,
            'datum_id': 1,
            'resampling_method_id': 1,
            'file_format_id': 1,
            'geometry': '0103000020E6100000010000000500000000000000408A314000000000A00740C00000000000D6344000000000A03440C000000000004F344000000000009741C00000000000D9314000000000805341C000000000408A314000000000A00740C0'
        }

        myModel = DeliveryDetail.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_DeliveryDetail_update(self):
        """
        Tests DeliveryDetail model update
        """
        myModelPK = 1
        myModel = DeliveryDetail.objects.get(pk=myModelPK)
        myNewModelData = {
            'user_id': 1,
            'processing_level_id': 1,
            'projection_id': 1,
            'datum_id': 1,
            'resampling_method_id': 1,
            'file_format_id': 1,
            'geometry': 'POLYGON ((17.5400390625000000 -32.0595703125000000, 20.8359375000000000 -32.4111328125000000, 20.3085937500000000 -35.1796875000000000, 17.8476562500000000 -34.6523437500000000, 17.5400390625000000 -32.0595703125000000))'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_DeliveryDetail_delete(self):
        """
        Tests DeliveryDetail model delete
        """
        myModelPK = 1
        myModel = DeliveryDetail.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
