"""
SANSA-EO Catalogue - Order_model - implements basic CRUD unittests

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

from datetime import datetime

from django.test import TestCase

from catalogue.tests.test_utils import simpleMessage
from catalogue.models import Order


class OrderCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_processinglevel.json',
        'test_projection.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_order.json',
        'test_datum.json',
        'test_resamplingmethod.json',
        'test_fileformat.json',
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Order_create(self):
        """
        Tests Order model creation
        """
        myNewData = {
            'user_id': 1,
            'notes': 'Sample Order notes',
            'order_status_id': 1,
            'delivery_method_id': 1,
            'delivery_detail_id': None,
            'market_sector_id': 1,
            # we don't test order_date as its auto now field
            #'order_date': '2010-11-10 10:23:37'
        }
        myModel = Order(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_Order_read(self):
        """
        Tests Order model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'user_id': 1,
            'notes': 'Sample Order notes',
            'order_status_id': 1,
            'delivery_method_id': 1,
            'delivery_detail_id': 1,
            'market_sector_id': 1,
            'order_date':  datetime.strptime('2010-11-10 10:23:37', '%Y-%m-%d %H:%M:%S'),
        }
        #import ipdb;ipdb.set_trace()
        myModel = Order.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_Order_update(self):
        """
        Tests Order model update
        """
        myModelPK = 1
        myModel = Order.objects.get(pk=myModelPK)
        myNewModelData = {
            'user_id': 1,
            'notes': 'Other Sample Order notes',
            'order_status_id': 3,
            'delivery_method_id': 1,
            'delivery_detail_id': None,
            'market_sector_id': 1,
            # we don't test order_date as its auto now field
            #'order_date': '2010-11-10 10:23:37'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_Order_delete(self):
        """
        Tests Order model delete
        """
        myModelPK = 1
        myModel = Order.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_Order_repr(self):
        """
        Tests Order model representation
        """
        myModelPKs = [1]
        myExpResults = [u'1']

        for idx, PK in enumerate(myModelPKs):
            myModel = Order.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))