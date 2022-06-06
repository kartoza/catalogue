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

from model_factories import SearchDateRangeF, SearchF
from search.models import SearchDateRange


class TestSearchDateRangeCRUD(TestCase):
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
        model = SearchDateRangeF.create()
        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_SearchDateRange_read(self):
        """
        Tests SearchDateRange model read
        """
        data = {
            'start_date': date(2010, 0o7, 15),
            'end_date': date(2012, 0o7, 15)
        }
        model = SearchDateRangeF.create()
        # check if data is correct
        for key, val in list(data.items()):
            self.assertEqual(model.__dict__.get(key), val)

    def test_SearchDateRange_update(self):
        """
        Tests SearchDateRange model update
        """
        model = SearchDateRangeF.create()
        data = {
            'start_date': '1941-01-01',
            'end_date': '2030-12-31'
        }

        model.__dict__.update(data)
        model.save()

        # check if updated
        for key, val in list(data.items()):
            self.assertEqual(model.__dict__.get(key), val)

    def test_SearchDateRange_delete(self):
        """
        Tests SearchDateRange model delete
        """
        model = SearchDateRangeF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_SearchDateRange_local_format(self):
        """
        Tests SearchDateRange model local_format method
        """
        model = SearchDateRangeF.create()

        result = '15-07-2010 : 15-07-2012'

        res = model.local_format()
        self.assertEqual(res, result)

    def test_SearchDateRange_from_local_format(self):
        """
        Tests SearchDateRange model from_local_format method
        """
        dates = ['01-01-1901 : 31-12-2100', '01-01-2009 : 31-12-2012']
        results = [
            (datetime(1901, 1, 1, 0, 0), datetime(2100, 12, 31, 0, 0)),
            (datetime(2009, 1, 1, 0, 0), datetime(2012, 12, 31, 0, 0))
        ]

        for idx, myDate in enumerate(dates):
            res = SearchDateRange.from_local_format(myDate)
            self.assertEqual(res, results[idx])

    def test_SearchDateRange_model_repr(self):
        """
        Tests SearchDateRange model repr
        """
        search = SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9'
        )
        model = SearchDateRangeF.create(search=search)

        self.assertEqual(
            str(model), (
                '15-07-2010 : 15-07-2012 '
                'Guid: 69d814b7-3164-42b9-9530-50ae77806da9')
        )
