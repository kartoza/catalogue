"""
SANSA-EO Catalogue - SearchRecord_model - implements basic CRUD unittests

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
__date__ = '28/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import SearchRecord


class SearchRecordCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_genericproduct.json',
        'test_user.json',
        'test_orderstatus.json',
        'test_marketsector.json',
        'test_deliverymethod.json',
        'test_order.json',
        'test_searchrecord.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SearchRecord_create(self):
        """
        Tests SearchRecord model creation
        """
        myNewData = {
            'user_id': 1,
            'order_id': 1,
            'product_id': 1960810,
            'delivery_detail_id': None,
            'internal_order_id': None,
            'download_path': 'Some path',
            'product_ready': True
        }
        myModel = SearchRecord(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_SearchRecord_read(self):
        """
        Tests SearchRecord model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'user_id': 1,
            'order_id': 1,
            'product_id': 2277404,
            'delivery_detail_id': None,
            'internal_order_id': None,
            'download_path': '',
            'product_ready': False
        }
        #import ipdb;ipdb.set_trace()
        myModel = SearchRecord.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_SearchRecord_update(self):
        """
        Tests SearchRecord model update
        """
        myModelPK = 1
        myModel = SearchRecord.objects.get(pk=myModelPK)
        myNewModelData = {
            'user_id': 1,
            'order_id': 1,
            'product_id': 1960810,
            'delivery_detail_id': None,
            'internal_order_id': None,
            'download_path': 'Some path',
            'product_ready': True
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_SearchRecord_delete(self):
        """
        Tests SearchRecord model delete
        """
        myModelPK = 1
        myModel = SearchRecord.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_SearchRecord_kmlExtents(self):
        """
        Tests SearchRecord model kmlExtents method
        """
        myModelPKs = [1]
        myExpResults = ["""<north>-1.1967</north>
          <south>-1.8094</south>
          <east>35.8477</east>
          <west>35.1936</west>"""]

        for idx, PK in enumerate(myModelPKs):
            myModel = SearchRecord.objects.get(pk=PK)
            myRes = myModel.kmlExtents()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s kmlExtents:' % PK))