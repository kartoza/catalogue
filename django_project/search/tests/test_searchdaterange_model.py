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
__version__ = '0.2'
__date__ = '17/07/2013'
__copyright__ = 'South African National Space Agency'

from datetime import date, datetime
from django.test import TestCase

from .model_factories import SearchDateRangeF, SearchF
from ..models import SearchDateRange


class SearchDateRangeCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SearchDateRange_create(self):
        """
        Tests SearchDateRange model creation
        """
        myModel = SearchDateRangeF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_SearchDateRange_read(self):
        """
        Tests SearchDateRange model read
        """
        myExpectedModelData = {
            'start_date': date(2010, 07, 15),
            'end_date': date(2012, 07, 15)
        }
        myModel = SearchDateRangeF.create()
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_SearchDateRange_update(self):
        """
        Tests SearchDateRange model update
        """
        myModel = SearchDateRangeF.create()
        myNewModelData = {
            'start_date': '1941-01-01',
            'end_date': '2030-12-31'
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_SearchDateRange_delete(self):
        """
        Tests SearchDateRange model delete
        """
        myModel = SearchDateRangeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SearchDateRange_local_format(self):
        """
        Tests SearchDateRange model local_format method
        """
        myModel = SearchDateRangeF.create()

        myExpResult = '15-07-2010 : 15-07-2012'

        myRes = myModel.local_format()
        self.assertEqual(myRes, myExpResult)

    def test_SearchDateRange_from_local_format(self):
        """
        Tests SearchDateRange model from_local_format method
        """
        myDates = ['01-01-1901 : 31-12-2100', '01-01-2009 : 31-12-2012']
        myExpResults = [
            (datetime(1901, 1, 1, 0, 0), datetime(2100, 12, 31, 0, 0)),
            (datetime(2009, 1, 1, 0, 0), datetime(2012, 12, 31, 0, 0))
        ]

        for idx, myDate in enumerate(myDates):
            myRes = SearchDateRange.from_local_format(myDate)
            self.assertEqual(myRes, myExpResults[idx])

    def test_SearchDateRange_model_repr(self):
        """
        Tests SearchDateRange model repr
        """
        mySearch = SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9'
        )
        myModel = SearchDateRangeF.create(search=mySearch)

        self.assertEqual(
            unicode(myModel), (
                u'15-07-2010 : 15-07-2012 '
                'Guid: 69d814b7-3164-42b9-9530-50ae77806da9')
        )
