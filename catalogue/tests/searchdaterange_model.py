"""
SANSA-EO Catalogue - SearchDateRange_model - implements basic CRUD unittests

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
from catalogue.models import SearchDateRange
from datetime import date, datetime


class SearchDateRangeCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_acquisitionmode.json',
        'test_sensortype.json',
        'test_processinglevel.json',
        'test_searchdaterange.json',
        'test_search.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SearchDateRange_create(self):
        """
        Tests SearchDateRange model creation
        """
        myNewData = {
            'search_id': 1,
            'start_date': '1941-01-01',
            'end_date': '2030-12-31'
        }
        myModel = SearchDateRange(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(myModel.pk != None,
            simpleMessage(myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_SearchDateRange_read(self):
        """
        Tests SearchDateRange model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'search_id': 1,
            'start_date': date(1901, 01, 01),
            'end_date': date(2100, 12, 31)
        }
        #import ipdb;ipdb.set_trace()
        myModel = SearchDateRange.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_SearchDateRange_update(self):
        """
        Tests SearchDateRange model update
        """
        myModelPK = 1
        myModel = SearchDateRange.objects.get(pk=myModelPK)
        myNewModelData = {
            'search_id': 1,
            'start_date': '1941-01-01',
            'end_date': '2030-12-31'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val,
                simpleMessage(myModel.__dict__.get(key), val,
                message='For key "%s"' % key))

    def test_SearchDateRange_delete(self):
        """
        Tests SearchDateRange model delete
        """
        myModelPK = 1
        myModel = SearchDateRange.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None,
            simpleMessage(myModel.pk, None,
            message='Model PK should equal None'))

    def test_SearchDateRange_local_format(self):
        """
        Tests SearchDateRange model local_format method
        """
        myModelPKs = [1, 2, 3]
        myExpResults = ['01-01-1901 : 31-12-2100', '01-01-2009 : 31-12-2012',
        '01-01-2011 : 31-12-2012']

        for idx, PK in enumerate(myModelPKs):
            myModel = SearchDateRange.objects.get(pk=PK)
            myRes = myModel.local_format()
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='Model PK %s local_format:' % PK))

    def test_SearchDateRange_from_local_format(self):
        """
        Tests SearchDateRange model from_local_format method
        """
        myDates = ['01-01-1901 : 31-12-2100', '01-01-2009 : 31-12-2012']
        myExpResults = [
        (datetime(1901, 1, 1, 0, 0), datetime(2100, 12, 31, 0, 0)),
        (datetime(2009, 1, 1, 0, 0), datetime(2012, 12, 31, 0, 0))]

        for idx, myDate in enumerate(myDates):
            myRes = SearchDateRange.from_local_format(myDate)
            self.assertEqual(myRes, myExpResults[idx],
                simpleMessage(myRes, myExpResults[idx],
                    message='SearchDateRange from_local_format:'))
