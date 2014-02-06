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
__version__ = '0.2'
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from search.tests.model_factories import SearchRecordF
from .model_factories import OrderF


class OrderCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Order_create(self):
        """
        Tests Order model creation
        """
        myModel = OrderF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_Order_delete(self):
        """
        Tests Order model delete
        """
        myModel = OrderF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Order_read(self):
        """
        Tests Order model read
        """
        myModel = OrderF.create(**{
            'notes': 'Sample Order notes'
        })

        self.assertEqual(myModel.notes, 'Sample Order notes')

    def test_Order_update(self):
        """
        Tests Order model update
        """
        myModel = OrderF.create()

        myModel.__dict__.update({
            'notes': 'Sample Order notes'
        })
        myModel.save()

        #check if updated
        self.assertEqual(myModel.notes, 'Sample Order notes')

    def test_Order_repr(self):
        """
        Tests Order model representation
        """
        myModel = OrderF.create(**{
            'id': 1
        })

        self.assertEqual(unicode(myModel), '1')

    def test_Order_value(self):
        """
        Tests Order model value attribute
        """

        tstOrder = OrderF.create()

        SearchRecordF.create(**{
            'rand_cost_per_scene': 120.49,
            'order': tstOrder
        })
        SearchRecordF.create(**{
            'rand_cost_per_scene': 101.51,
            'order': tstOrder
        })

        self.assertEqual(tstOrder.value(), 222)
