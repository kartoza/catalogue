"""
SANSA-EO Catalogue - quality_model - implements basic CRUD unittests

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
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import Quality


class QualityCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_quality.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_quality_create(self):
        """
        Tests Quality model creation
        """
        myNewModelData = {
            'name': 'Unknown quality'
        }

        myModel = Quality(**myNewModelData)
        myModel.save()

        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_quality_read(self):
        """
        Tests Quality model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'name': 'Unknown'
        }
        myModel = Quality.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                    message='For key "%s"' % key))

    def test_quality_update(self):
        """
        Tests Quality model update
        """
        myModelPK = 1
        myModel = Quality.objects.get(pk=myModelPK)
        myNewModelData = {
            'name': 'Unknown quality'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(val, myModel.__dict__.get(key),
                message='For key "%s"' % key))

    def test_quality_delete(self):
        """
        Tests Quality model delete
        """
        myModelPK = 1
        myModel = Quality.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))
