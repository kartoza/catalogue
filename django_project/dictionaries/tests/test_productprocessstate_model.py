"""
SANSA-EO Catalogue - Dictionaries ProductProcessState - basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '05/02/2014'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import ProductProcessStateF


class TestProductProcessStateCRUD(TestCase):
    """
    Tests ProductProcessState model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_ProductProcessState_create(self):
        """
        Tests ProductProcessState model creation
        """
        myModel = ProductProcessStateF.create()

        self.assertTrue(myModel.pk is not None)

    def test_ProductProcessState_delete(self):
        """
        Tests ProductProcessState model delete
        """
        myModel = ProductProcessStateF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ProductProcessState_read(self):
        """
        Tests SalesRegion model read
        """

        myModel = ProductProcessStateF.create(**{
            'name': 'Best state evar!',
        })

        self.assertEqual(myModel.name, 'Best state evar!')

    def test_ProductProcessState_update(self):
        """
        Tests ProductProcessState model update
        """

        myModel = ProductProcessStateF.create()

        myModel.__dict__.update(**{
            'name': 'Best state evar!'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'Best state evar!')

    def test_ProductProcessState_repr(self):
        """
        Tests ProductProcessState model repr
        """

        myModel = ProductProcessStateF.create(**{
            'name': 'Best state evar!'
        })

        self.assertEqual(unicode(myModel), u'Best state evar!')
