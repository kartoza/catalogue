"""
SANSA-EO Catalogue - DeliveryMethod_model - implements basic CRUD unittests

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
__date__ = '07/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from model_factories import DeliveryMethodF


class TestDeliveryMethodCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_DeliveryMethod_create(self):
        """
        Tests DeliveryMethod model creation
        """

        model = DeliveryMethodF.create()

        self.assertTrue(model.pk is not None)

    def test_delivery_method_delete(self):
        """
        Tests DeliveryMethod model delete
        """
        model = DeliveryMethodF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_delivery_method_read(self):
        """
        Tests DeliveryMethod model read
        """

        model = DeliveryMethodF.create(**{
            'name': 'Courier + External Hard Disk'
        })

        self.assertEqual(model.name, 'Courier + External Hard Disk')

    def test_delivery_method_update(self):
        """
        Tests DeliveryMethod model update
        """
        model = DeliveryMethodF.create()

        model.__dict__.update({
            'name': 'Courier + External Hard Disk'
        })
        model.save()

        self.assertEqual(model.name, 'Courier + External Hard Disk')

    def test_delivery_method_repr(self):
        """
        Tests DeliveryMethod model representation
        """
        myModel = DeliveryMethodF.create(**{
            'name': 'Courier + External Hard Disk'
        })

        self.assertEqual(str(myModel.name), 'Courier + External Hard Disk')
