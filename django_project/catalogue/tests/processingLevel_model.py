"""
SANSA-EO Catalogue - processingLevel_model - implements basic CRUD unittests

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
__date__ = '20/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from django_project.catalogue.tests.test_utils import simpleMessage
from django_project.catalogue.models import ProcessingLevel


class ProcessingLevelCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_processinglevel.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_processinglevel_create(self):
        """
        Tests ProcessingLevel model creation
        """
        myNewModelData = {
            'abbreviation': 'None',
            'name': 'Level Unknown'
        }

        myModel = ProcessingLevel(**myNewModelData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_processinglevel_read(self):
        """
        Tests ProcessingLevel model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'abbreviation': '2A',
            'name': 'Level 2A'
        }
        myModel = ProcessingLevel.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                    message='For key "%s"' % key))

    def test_processinglevel_update(self):
        """
        Tests ProcessingLevel model update
        """
        myModelPK = 1
        myModel = ProcessingLevel.objects.get(pk=myModelPK)
        myNewModelData = {
            'abbreviation': 'None',
            'name': 'Level Unknown'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                message='For key "%s"' % key))

    def test_processinglevel_delete(self):
        """
        Tests ProcessingLevel model delete
        """
        myModelPK = 1
        myModel = ProcessingLevel.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
