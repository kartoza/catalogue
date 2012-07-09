"""
SANSA-EO Catalogue - MarketSector_model - implements basic CRUD unittests

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
from catalogue.models import MarketSector


class MarketSectorCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_marketsector.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_MarketSector_create(self):
        """
        Tests MarketSector model creation
        """
        myNewData = {
            'name': 'Unknown MarketSector'
        }
        myModel = MarketSector(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_MarketSector_read(self):
        """
        Tests MarketSector model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'name': 'Decline to say'
        }
        #import ipdb;ipdb.set_trace()
        myModel = MarketSector.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_MarketSector_update(self):
        """
        Tests MarketSector model update
        """
        myModelPK = 1
        myModel = MarketSector.objects.get(pk=myModelPK)
        myNewModelData = {
            'name': 'Another Unknown MarketSector'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_MarketSector_delete(self):
        """
        Tests MarketSector model delete
        """
        myModelPK = 1
        myModel = MarketSector.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_MarketSector_repr(self):
        """
        Tests MarketSector model representation
        """
        myModelPKs = [1, 2]
        myExpResults = [u'Decline to say', u'Government']

        for idx, PK in enumerate(myModelPKs):
            myModel = MarketSector.objects.get(pk=PK)
            self.assertEqual(myModel.__unicode__(), myExpResults[idx],
                simpleMessage(myModel.__unicode__(), myExpResults[idx],
                    message='Model PK %s repr:' % PK))
