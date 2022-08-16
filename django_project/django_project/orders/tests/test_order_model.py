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

import unittest
from django.test import TestCase
from dictionaries.tests.model_factories import SubsidyTypeF
from search.tests.model_factories import SearchRecordF
from model_factories import OrderF
from core.model_factories import CurrencyF


class TestOrderCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_order_create(self):
        """
        Tests Order model creation
        """
        model = OrderF.create()
        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_order_delete(self):
        """
        Tests Order model delete
        """
        model = OrderF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_order_read(self):
        """
        Tests Order model read
        """
        model = OrderF.create(**{
            'notes': 'Sample Order notes'
        })

        self.assertEqual(model.notes, 'Sample Order notes')

    def test_order_update(self):
        """
        Tests Order model update
        """
        model = OrderF.create()

        model.__dict__.update({
            'notes': 'Sample Order notes'
        })
        model.save()

        # check if updated
        self.assertEqual(model.notes, 'Sample Order notes')

    def test_order_repr(self):
        """
        Tests Order model representation
        """
        model = OrderF.create(**{
            'id': 1
        })

        self.assertEqual(str(model), '1')

    @unittest.skip("Skiping this test")
    def test_order_value(self):
        """
        Tests Order model value attribute
        """

        tst_order = OrderF.create()

        SearchRecordF.create(**{
            'currency': CurrencyF.create(code='ZAR'),
            'rand_cost_per_scene': 120.49,
            'order': tst_order
        })
        SearchRecordF.create(**{
            'currency': CurrencyF.create(code='USD'),
            'rand_cost_per_scene': 101.51,
            'order': tst_order
        })

        self.assertEqual(tst_order.cost(), 222)

    @unittest.skip("Skiping this test")
    def test_order_cost_no_subsidy(self):
        """
        Tests Order model cost attribute without subsidy
        """

        subsidy_type = SubsidyTypeF.create(**{
            'name': 'None'
        })

        order = OrderF.create(**{
            'subsidy_type_assigned': subsidy_type
        })

        SearchRecordF.create(**{
            'currency': CurrencyF.create(code='ZAR'),
            'rand_cost_per_scene': 120.49,
            'order': order
        })
        SearchRecordF.create(**{
            'currency': CurrencyF.create(code='USD'),
            'rand_cost_per_scene': 101.51,
            'order': order
        })

        self.assertEqual(order.cost(), 222.0)

    def test_order_cost_with_subsidy(self):
        """
        Tests Order model cost attribute with subsidy
        """

        subsidy_type = SubsidyTypeF.create(**{
            'name': 'PhD Grant'
        })
        order = OrderF.create(**{
            'subsidy_type_assigned': subsidy_type
        })

        SearchRecordF.create(**{
            'currency': CurrencyF.create(code='ZAR'),
            'rand_cost_per_scene': 120.49,
            'order': order
        })
        SearchRecordF.create(**{
            'currency': CurrencyF.create(code='USD'),
            'rand_cost_per_scene': 101.51,
            'order': order
        })

        self.assertEqual(order.cost(), 0)
