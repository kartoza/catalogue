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

from .model_factories import DeliveryMethodF


class DeliveryMethodCRUD_Test(TestCase):
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

        myModel = DeliveryMethodF.create()

        self.assertTrue(myModel.pk is not None)

    def test_DeliveryMethod_delete(self):
        """
        Tests DeliveryMethod model delete
        """
        myModel = DeliveryMethodF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_DeliveryMethod_read(self):
        """
        Tests DeliveryMethod model read
        """

        myModel = DeliveryMethodF.create(**{
            'name': 'Courier + External Hard Disk'
        })

        self.assertEqual(myModel.name, 'Courier + External Hard Disk')

    def test_DeliveryMethod_update(self):
        """
        Tests DeliveryMethod model update
        """
        myModel = DeliveryMethodF.create()

        myModel.__dict__.update({
            'name': 'Courier + External Hard Disk'
        })
        myModel.save()

        self.assertEqual(myModel.name, 'Courier + External Hard Disk')

    def test_DeliveryMethod_repr(self):
        """
        Tests DeliveryMethod model representation
        """
        myModel = DeliveryMethodF.create(**{
            'name': 'Courier + External Hard Disk'
        })

        self.assertEqual(str(myModel.name), 'Courier + External Hard Disk')
