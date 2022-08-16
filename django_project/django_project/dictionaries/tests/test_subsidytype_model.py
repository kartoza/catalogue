"""
SANSA-EO Catalogue - Dictionaries SubsidyType - basic CRUD unittests

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

from .model_factories import SubsidyTypeF


class TestSubsidyTypeCRUD(TestCase):
    """
    Tests SubsidyType model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SubsidyType_create(self):
        """
        Tests SubsidyType model creation
        """
        myModel = SubsidyTypeF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SubsidyType_delete(self):
        """
        Tests SubsidyType model delete
        """
        myModel = SubsidyTypeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SubsidyType_read(self):
        """
        Tests SalesRegion model read
        """

        myModel = SubsidyTypeF.create(**{
            'abbreviation': 'NS',
            'name': 'NoSubsidy',
        })

        self.assertEqual(myModel.name, 'NoSubsidy')

        self.assertEqual(myModel.abbreviation, 'NS')

    def test_SubsidyType_update(self):
        """
        Tests SubsidyType model update
        """

        myModel = SubsidyTypeF.create()

        myModel.__dict__.update(**{
            'abbreviation': 'NS',
            'name': 'NoSubsidy'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'NoSubsidy')

        self.assertEqual(myModel.abbreviation, 'NS')

    def test_SubsidyType_repr(self):
        """
        Tests SubsidyType model repr
        """

        myModel = SubsidyTypeF.create(**{
            'abbreviation': 'NS'
        })

        self.assertEqual(str(myModel), 'NS')
