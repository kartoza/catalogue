"""
SANSA-EO Catalogue - Dictionaries ReferenceSystem - basic CRUD
unittests

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
__date__ = '23/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import ReferenceSystemF


class TestReferenceSystemCRUD(TestCase):
    """
    Tests ReferenceSystem model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_ReferenceSystem_create(self):
        """
        Tests ReferenceSystem model creation
        """
        myModel = ReferenceSystemF.create()

        self.assertTrue(myModel.pk is not None)

    def test_ReferenceSystem_delete(self):
        """
        Tests ReferenceSystem model delete
        """
        myModel = ReferenceSystemF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ReferenceSystem_read(self):
        """
        Tests ReferenceSystem model read
        """

        myModel = ReferenceSystemF.create(**{
            'name': 'New Reference System',
            'description': 'No description',
            'abbreviation': 'NRS',
        })

        self.assertEqual(myModel.name, 'New Reference System')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NRS')

    def test_ReferenceSystem_update(self):
        """
        Tests ReferenceSystem model update
        """

        myModel = ReferenceSystemF.create()

        myModel.__dict__.update(**{
            'name': 'New Reference System',
            'description': 'No description',
            'abbreviation': 'NRS',
        })

        myModel.save()
        self.assertEqual(myModel.name, 'New Reference System')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.abbreviation, 'NRS')

    def test_ReferenceSystem_repr(self):
        """
        Tests ReferenceSystem model repr
        """

        myModel = ReferenceSystemF.create(**{
            'name': 'New Reference System'
        })

        self.assertEqual(str(myModel), 'New Reference System')
