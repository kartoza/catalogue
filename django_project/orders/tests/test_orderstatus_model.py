"""
SANSA-EO Catalogue - OrderStatus_model - implements basic CRUD unittests

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

from .model_factories import OrderStatusF


class OrderStatusCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OrderStatus_create(self):
        """
        Tests OrderStatus model creation
        """
        myModel = OrderStatusF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_OrderStatus_delete(self):
        """
        Tests OrderStatus model delete
        """
        myModel = OrderStatusF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_OrderStatus_read(self):
        """
        Tests OrderStatus model read
        """
        myModel = OrderStatusF.create(**{
            'name': 'Placed'
        })

        self.assertEqual(myModel.name, 'Placed')

    def test_OrderStatus_update(self):
        """
        Tests OrderStatus model update
        """
        myModel = OrderStatusF.create()

        myModel.__dict__.update({
            'name': 'Placed'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Placed')

    def test_OrderStatus_repr(self):
        """
        Tests OrderStatus model representation
        """
        myModel = OrderStatusF.create(**{
            'name': 'Placed'
        })

        self.assertEqual(unicode(myModel), 'Placed')
