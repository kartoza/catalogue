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
__version__ = '0.2'
__date__ = '17/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage

from core.model_factories import UserF
from catalogue.tests.model_factories import OrderF, GenericProductF

from .model_factories import SearchRecordF


class SearchRecordCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SearchRecord_create(self):
        """
        Tests SearchRecord model creation
        """
        myModel = SearchRecordF.create()
        #check if PK exists
        self.assertTrue(
            myModel.pk is not None,
            simpleMessage(
                myModel.pk, 'not None',
                message='Model PK should NOT equal None')
        )

    def test_SearchRecord_read(self):
        """
        Tests SearchRecord model read
        """
        myOrder = OrderF.create(notes='New Order')
        myModel = SearchRecordF.create(order=myOrder)

        self.assertTrue(myModel.pk is not None)
        self.assertTrue(myModel.order.notes == 'New Order')
        self.assertTrue(myModel.product_ready is True)
        self.assertTrue(myModel.internal_order_id is None)

    def test_SearchRecord_update(self):
        """
        Tests SearchRecord model update
        """
        myModel = SearchRecordF.create()
        myNewOrder = OrderF()

        myNewModelData = {
            'order': myNewOrder,
            'download_path': 'Some path',
            'product_ready': True
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(
                myModel.__dict__.get(key), val,
                simpleMessage(
                    myModel.__dict__.get(key), val,
                    message='For key "%s"' % key)
            )

    def test_SearchRecord_delete(self):
        """
        Tests SearchRecord model delete
        """
        myModel = SearchRecordF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(
            myModel.pk is None,
            simpleMessage(
                myModel.pk, None,
                message='Model PK should equal None')
        )

    def test_SearchRecord_kmlExtents(self):
        """
        Tests SearchRecord model kmlExtents method
        """
        myExpResult = """<north>-32.05</north>
          <south>-35.17</south>
          <east>20.83</east>
          <west>17.54</west>"""

        myModel = SearchRecordF.create()
        myRes = myModel.kmlExtents()
        self.assertEqual(
            myRes, myExpResult,
            simpleMessage(myRes, myExpResult)
        )

    def test_SearchRecord_repr(self):
        """
        Tests SearchRecord model repr method
        """
        myProduct = GenericProductF.create(unique_product_id='123qwe')
        myModel = SearchRecordF.create(product=myProduct)

        myExpResult = '123qwe'
        self.assertEqual(unicode(myModel), myExpResult)

    def test_SearchRecord_create_method(self):
        """
        Tests SearchRecord model repr method
        """
        myProduct = GenericProductF.create(unique_product_id='123qwe')
        myUser = UserF.create(username='testuser')
        myModel = SearchRecordF.create()

        myNewModel = myModel.create(myUser, myProduct)

        self.assertEqual(unicode(myNewModel), '123qwe')
        self.assertEqual(myNewModel.user.username, 'testuser')