"""
SANSA-EO Catalogue - topic_model - implements basic CRUD unittests

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

from django.test import TestCase

from .model_factories import TopicF


class TopicCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_topic_create(self):
        """
        Tests Topic model creation
        """

        myModel = TopicF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_topic_delete(self):
        """
        Tests Topic model delete
        """
        myModel = TopicF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_topic_read(self):
        """
        Tests Topic model read
        """
        myModel = TopicF.create(**{
            'abbreviation': 'SMPTOP',
            'name': 'Sample Topic'
        })

        self.assertEqual(myModel.abbreviation, 'SMPTOP')
        self.assertEqual(myModel.name, 'Sample Topic')

    def test_topic_update(self):
        """
        Tests Topic model update
        """
        myModel = TopicF.create()
        myModel.__dict__.update({
            'abbreviation': 'SMPTOP',
            'name': 'Sample Topic'
        })
        myModel.save()

        self.assertEqual(myModel.abbreviation, 'SMPTOP')
        self.assertEqual(myModel.name, 'Sample Topic')

    def test_topic_repr(self):
        """
        Tests Topic model repr
        """
        myModel = TopicF.create(**{
            'name': 'Sample Topic'
        })

        self.assertEqual(str(myModel), 'Sample Topic')
