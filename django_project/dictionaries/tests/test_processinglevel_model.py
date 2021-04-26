"""
SANSA-EO Catalogue - Dictionaries ProcessingLevel - basic CRUD unittests

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

from .model_factories import ProcessingLevelF


class TestProcessingLevelCRUD(TestCase):
    """
    Tests ProcessingLevel model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_processingLevel_create(self):
        """
        Tests ProcessingLevel model creation
        """
        myModel = ProcessingLevelF.create()

        self.assertTrue(myModel.pk is not None)

    def test_processingLevel_delete(self):
        """
        Tests ProcessingLevel model delete
        """
        myModel = ProcessingLevelF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_processingLevel_read(self):
        """
        Tests processingLevel model read
        """

        myModel = ProcessingLevelF.create(**{
            'abbreviation': 'TST1',
            'name': 'Test Processing Level 1',
            'description': 'No description'
        })

        self.assertEqual(myModel.abbreviation, 'TST1')

        self.assertEqual(myModel.name, 'Test Processing Level 1')

        self.assertEqual(myModel.description, 'No description')

    def test_processingLevel_update(self):
        """
        Tests processingLevel model update
        """

        myModel = ProcessingLevelF.create()

        myModel.__dict__.update(**{
            'abbreviation': 'TST1',
            'name': 'Test Processing Level 1',
            'description': 'No description'
        })
        myModel.save()

        self.assertEqual(myModel.abbreviation, 'TST1')

        self.assertEqual(myModel.name, 'Test Processing Level 1')

        self.assertEqual(myModel.description, 'No description')

    def test_processingLevel_repr(self):
        """
        Tests processingLevel model repr
        """
        myModel = ProcessingLevelF.create(**{
            'abbreviation': 'TST1',
            'name': 'Test Processing Level 1',
            'description': 'No description'
        })

        self.assertEqual(
            str(myModel),
            'TST1 Test Processing Level 1')
