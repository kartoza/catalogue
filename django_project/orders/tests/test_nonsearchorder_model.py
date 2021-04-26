"""
SANSA-EO Catalogue - NonSearchRecord model - implements basic CRUD unittests

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
__date__ = '06/02/2014'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase


from core.model_factories import CurrencyF
from core.model_factories import UserF
from .model_factories import NonSearchRecordF, OrderF


class NonSearchRecordCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_NonSearchRecord_create(self):
        """
        Tests NonSearchRecord model creation
        """
        myModel = NonSearchRecordF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_NonSearchRecord_delete(self):
        """
        Tests NonSearchRecord model delete
        """
        myModel = NonSearchRecordF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_NonSearchRecord_read(self):
        """
        Tests NonSearchRecord model read
        """
        tstUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password'
        })

        myOrder = OrderF.create(notes='New Order')
        tstCurrency = CurrencyF.create(**{
            'name': 'SuperGold'
        })

        myModel = NonSearchRecordF.create(**{
            'user': tstUser,
            'order': myOrder,
            'product_description': 'A new product description',
            'download_path': 'someplace/somewhere',
            'cost_per_scene': 123.12,
            'currency': tstCurrency,
            'rand_cost_per_scene': 321.21
        })

        self.assertTrue(myModel.pk is not None)
        self.assertEqual(
            myModel.product_description, 'A new product description')
        self.assertEqual(myModel.download_path, 'someplace/somewhere')
        self.assertEqual(myModel.cost_per_scene, 123.12)
        self.assertEqual(myModel.rand_cost_per_scene, 321.21)

    def test_NonSearchRecord_update(self):
        """
        Tests NonSearchRecord model update
        """
        myModel = NonSearchRecordF.create()

        myNewModelData = {
            'product_description': 'A new product description',
            'download_path': 'someplace/somewhere',
            'cost_per_scene': 123.12,
            'rand_cost_per_scene': 321.21
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in list(myNewModelData.items()):
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_NonSearchRecord_repr(self):
        """
        Tests NonSearchRecord model repr method
        """
        myModel = NonSearchRecordF.create(**{
            'id': 12321
        })

        self.assertEqual(str(myModel), '12321')
