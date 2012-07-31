"""
SANSA-EO Catalogue - TaskingRequest_model - implements basic CRUD unittests

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
__date__ = '10/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import TaskingRequest
from datetime import datetime


class TaskingRequestCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_missionsensor.json',
        'test_order.json',
        'test_taskingrequest.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_TaskingRequest_create(self):
        """
        Tests TaskingRequest model creation
        """
        myNewData = {
            # order model fields
            'user_id': 1,
            'notes': 'Sample Order notes',
            'order_status_id': 1,
            'delivery_method_id': 1,
            'delivery_detail_id': None,
            'market_sector_id': 1,
            # actual taskingrequest model fields
            'target_date': '2010-11-10 10:23:37',
            'mission_sensor_id': 1
        }
        myModel = TaskingRequest(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_TaskingRequest_read(self):
        """
        Tests TaskingRequest model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'target_date': datetime.strptime('2010-11-10 10:23:37', '%Y-%m-%d %H:%M:%S'),
            'mission_sensor_id': 1
        }

        myModel = TaskingRequest.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_TaskingRequest_update(self):
        """
        Tests TaskingRequest model update
        """
        myModelPK = 1
        myModel = TaskingRequest.objects.get(pk=myModelPK)
        myNewModelData = {
            'target_date': '2012-11-10 10:23:37',
            'mission_sensor_id': 2
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def Xtest_TaskingRequest_delete(self):
        """
        Tests TaskingRequest model delete

        This test FAILS because current application doesn't support
        cascade delete on inherited models - Story #227
        """
        myModelPK = 1
        myModel = TaskingRequest.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
