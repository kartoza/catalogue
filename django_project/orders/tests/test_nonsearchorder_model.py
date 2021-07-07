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
from core.model_factories import UserF
from model_factories import NonSearchRecordF, OrderF, CurrencyF


class TestNonSearchRecordCRUD(TestCase):
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
        model = NonSearchRecordF.create()
        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_NonSearchRecord_delete(self):
        """
        Tests NonSearchRecord model delete
        """
        model = NonSearchRecordF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_NonSearchRecord_read(self):
        """
        Tests NonSearchRecord model read
        """
        user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password'
        })

        order = OrderF.create(notes='New Order')
        currency = CurrencyF.create(**{
            'name': 'SuperGold'
        })

        model = NonSearchRecordF.create(**{
            'user': user,
            'order': order,
            'product_description': 'A new product description',
            'download_path': 'someplace/somewhere',
            'cost_per_scene': 123.12,
            'currency': currency,
            'rand_cost_per_scene': 321.21
        })

        self.assertTrue(model.pk is not None)
        self.assertEqual(
            model.product_description, 'A new product description')
        self.assertEqual(model.download_path, 'someplace/somewhere')
        self.assertEqual(model.cost_per_scene, 123.12)
        self.assertEqual(model.rand_cost_per_scene, 321.21)

    def test_NonSearchRecord_update(self):
        """
        Tests NonSearchRecord model update
        """
        model = NonSearchRecordF.create()

        data = {
            'product_description': 'A new product description',
            'download_path': 'someplace/somewhere',
            'cost_per_scene': 123.12,
            'rand_cost_per_scene': 321.21
        }

        model.__dict__.update(data)
        model.save()

        # check if updated
        for key, val in list(data.items()):
            self.assertEqual(model.__dict__.get(key), val)

    def test_NonSearchRecord_repr(self):
        """
        Tests NonSearchRecord model repr method
        """
        model = NonSearchRecordF.create(**{
            'id': 12321
        })

        self.assertEqual(str(model), '12321')
