"""
SANSA-EO Catalogue - Search_model - implements basic CRUD unittests

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
__date__ = '16/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from core.model_factories import UserF
from dictionaries.tests.model_factories import CollectionF
from .model_factories import SearchF, SearchDateRangeF


class TestSearchCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_Search_create(self):
        """
        Tests Search model creation
        """
        myCollections = [CollectionF.create(), CollectionF.create()]
        myModel = SearchF.create(collections=myCollections)

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        self.assertTrue(myModel.collection.count() == 2)

    def test_Search_read(self):
        """
        Tests Search model read
        """
        myExpectedModelData = {
            'record_count': None,
            'use_cloud_cover': False,
            'sensor_inclination_angle_end': None,
            'satellite_id': None,
            'spectral_mode_id': None,
            'guid': '69d814b7-3164-42b9-9530-50ae77806da9',
            'sensor_inclination_angle_start': None,
            'ip_position': None,
            'deleted': False,
            'spatial_resolution': None,
            'k_orbit_path': None,
            'band_count': None,
            'j_frame_row': None,
            'cloud_mean': 5,
            'license_type': None
        }
        myModel = SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )
        #check if data is correct
        for key, val in list(myExpectedModelData.items()):
            self.assertEqual(myModel.__dict__.get(key), val)

        self.assertEqual(
            myModel.geometry.hex,
            '010300000001000000050000000AD7A3703D8A314066666666660640C014AE47E'
            '17AD4344014AE47E17A3440C0CDCCCCCCCC4C3440F6285C8FC29541C0D7A3703D'
            '0AD7314033333333335341C00AD7A3703D8A314066666666660640C0')

        self.assertEqual(
            myModel.processing_level.count(), 0)

        self.assertEqual(
            myModel.collection.count(), 2)

        self.assertTrue(
            myModel.user.pk is not None)

    def test_Search_update(self):
        """
        Tests Search model update
        """
        myModel = SearchF.create()
        myNewModelData = {
            'order_id': 1,
            'product_id': 1960810,
            'delivery_detail_id': None,
            'internal_order_id': None,
            'download_path': 'Some path',
            'product_ready': True
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in list(myNewModelData.items()):
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Search_delete(self):
        """
        Tests Search model delete
        """
        myModel = SearchF.create(guid=None)

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Search_datesAsString_single(self):
        """
        Tests Search model dates_as_string method
        """
        mySearch = SearchF.create()
        SearchDateRangeF.create(search=mySearch)

        myExpResults = '15-07-2010 : 15-07-2012'

        myRes = mySearch.dates_as_string()
        self.assertEqual(myRes, myExpResults)

    def test_Search_datesAsString_multiple(self):
        """
        Tests Search model dates_as_string method
        """
        mySearch = SearchF.create()
        # add date ranges
        SearchDateRangeF.create(search=mySearch)
        SearchDateRangeF.create(search=mySearch, end_date='2013-07-16')
        SearchDateRangeF.create(search=mySearch, end_date='2012-07-16')

        myExpResults = (
            '15-07-2010 : 15-07-2012, 15-07-2010 : 16-07-2013, '
            '15-07-2010 : 16-07-2012'
        )

        myRes = mySearch.dates_as_string()
        self.assertEqual(myRes, myExpResults)

    def test_Search_model_repr(self):
        """
        Tests Search model repr
        """
        myUser = UserF(username='test user')
        mySearch = SearchF.build(
            search_date='15-07-2010',
            user=myUser,
            guid='69d814b7-3164-42b9-9530-50ae77806da9'
        )

        self.assertEqual(
            str(mySearch),
            '15-07-2010 Guid: 69d814b7-3164-42b9-9530-50ae77806da9 User: '
            'test user')
