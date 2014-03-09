"""
SANSA-EO Catalogue - OrderStatusHistory_model - implements basic CRUD unittests

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
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import OrderStatusHistoryF


class OrderStatusHistoryCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OrderStatusHistory_create(self):
        """
        Tests OrderStatusHistory model creation
        """

        myModel = OrderStatusHistoryF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_OrderStatusHistory_delete(self):
        """
        Tests OrderStatusHistory model delete
        """
        myModel = OrderStatusHistoryF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_OrderStatusHistory_read(self):
        """
        Tests OrderStatusHistory model read
        """
        myModel = OrderStatusHistoryF.create(**{
            'notes': 'Order Status changed'
        })

        self.assertEqual(myModel.notes, 'Order Status changed')

    def test_OrderStatusHistory_update(self):
        """
        Tests OrderStatusHistory model update
        """
        myModel = OrderStatusHistoryF.create()

        myModel.__dict__.update({
            'notes': 'Order Status changed'
        })
        myModel.save()

        self.assertEqual(myModel.notes, 'Order Status changed')

    def test_OrderStatusHistory_repr(self):
        """
        Tests OrderStatusHistory model repr
        """
        myModel = OrderStatusHistoryF.create(**{
            'notes': 'Order Status changed Order Status changed'
        })

        self.assertEqual(unicode(myModel), 'Order Status changed Orde')
