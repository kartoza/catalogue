"""
SANSA-EO Catalogue - Dictionaries Collection - basic CRUD unittests

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
__date__ = '18/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import CollectionF, InstitutionF


class TestCollectionCRUD(TestCase):
    """
    Tests Collection model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_Collection_create(self):
        """
        Tests Collection model creation
        """
        myModel = CollectionF.create()

        self.assertTrue(myModel.pk is not None)

    def test_Collection_delete(self):
        """
        Tests Collection model delete
        """
        myModel = CollectionF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Collection_read(self):
        """
        Tests Collection model read
        """
        myInstitution = InstitutionF.create(name='New Institution')
        myModel = CollectionF.create(**{
            'name': 'Collection 1',
            'description': 'No description',
            'institution': myInstitution
        })

        self.assertEqual(myModel.name, 'Collection 1')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.institution.name, 'New Institution')

    def test_Collection_update(self):
        """
        Tests Collection model update
        """
        myModel = CollectionF.create()

        myInstitution = InstitutionF.create(**{'name': 'New Institution'})

        myModel.__dict__.update(**{
            'name': 'Collection 1',
            'description': 'No description'
        })
        myModel.institution = myInstitution
        myModel.save()

        self.assertEqual(myModel.name, 'Collection 1')

        self.assertEqual(myModel.description, 'No description')

        self.assertEqual(myModel.institution.name, 'New Institution')

    def test_Collection_repr(self):
        """
        Tests Collection model repr
        """
        myModel = CollectionF.create(**{
            'name': 'Collection 1',
        })

        self.assertEqual(str(myModel), 'Collection 1')
