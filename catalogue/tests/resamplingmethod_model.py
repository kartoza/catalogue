"""
SANSA-EO Catalogue - ResamplingMethod_model - implements basic CRUD unittests

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
__date__ = '09/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import ResamplingMethod
from datetime import datetime


class ResamplingMethodCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_resamplingmethod.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_ResamplingMethod_create(self):
        """
        Tests ResamplingMethod model creation
        """
        myNewData = {
            'name': 'Unknown ResamplingMethod'
        }
        myModel = ResamplingMethod(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_ResamplingMethod_read(self):
        """
        Tests ResamplingMethod model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'name': 'Nearest Neighbour'
        }
        #import ipdb;ipdb.set_trace()
        myModel = ResamplingMethod.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_ResamplingMethod_update(self):
        """
        Tests ResamplingMethod model update
        """
        myModelPK = 1
        myModel = ResamplingMethod.objects.get(pk=myModelPK)
        myNewModelData = {
            'name': 'Another Unknown ResamplingMethod'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_ResamplingMethod_delete(self):
        """
        Tests ResamplingMethod model delete
        """
        myModelPK = 1
        myModel = ResamplingMethod.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_ResamplingMethod_repr(self):
        """
        Tests ResamplingMethod model representation
        """
        myModelPKs = [1, 2]
        myExpResults = [u'Nearest Neighbour', u'Cubic convolution']

        for idx, PK in enumerate(myModelPKs):
            myModel = ResamplingMethod.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))
