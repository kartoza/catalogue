"""
SANSA-EO Catalogue - search_submitSearch - test view for submiting search form

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '28/01/2014'
__copyright__ = 'South African National Space Agency'

from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client
from core.model_factories import UserF


class TestSearchViewsSubmitSearch(TestCase):
    """
    Tests search views.py submitSearch method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_searchGuid_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'theId': 'testtest'}, {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'submitSearch',
                kwargs=myKwargTest)

    def test_searchView_user_not_logged_in_get(self):
        """
        Test view if user is not logged in
        """

        myClient = Client()

        myResp = myClient.get(reverse('submitSearch', kwargs={}))

        self.assertEqual(myResp.status_code, 404)

        self.assertEqual(myResp['content-type'], 'text/html; charset=utf-8')

        self.assertEqual(myResp.content, 'Not a POST!')

    def test_searchView_user_not_logged_in_post_invalid(self):
        """
        Test view if user is not logged in
        """

        myClient = Client()

        myPostData = {}

        myResp = myClient.post(reverse('submitSearch', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 404)

        self.assertEqual(myResp['content-type'], 'application/json')

        self.assertEqual(
            myResp.content, '{"cloud_mean": ["This field is required."]}'
        )

    def test_searchView_user_not_logged_in_post_valid_missing_daterange(self):
        """
        Test view if user is not logged in
        """

        myClient = Client()

        myPostData = {
            'cloud_mean': 0,
            'searchdaterange_set-TOTAL_FORMS': 0,
            'searchdaterange_set-INITIAL_FORMS': 0,
            'searchdaterange_set-MAX_NUM_FORMS': 0
        }

        myResp = myClient.post(reverse('submitSearch', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 404)

        self.assertEqual(
            myResp.content,
            '{"daterange": ["At least one date range is required."]}'
        )

        self.assertEqual(myResp['content-type'], 'application/json')

    def test_searchView_user_not_logged_in_post_valid(self):
        """
        Test view if user is not logged in
        """

        myClient = Client()

        myPostData = {
            'cloud_mean': 0,
            'searchdaterange_set-TOTAL_FORMS': 1,
            'searchdaterange_set-INITIAL_FORMS': 0,
            'searchdaterange_set-MAX_NUM_FORMS': 1,
            'searchdaterange_set-0-start_date': '2012-02-02',
            'searchdaterange_set-0-end_date': '2013-03-03',
        }

        myResp = myClient.post(reverse('submitSearch', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        # we can't fix guid, so only test length of an response
        self.assertEqual(
            len(myResp.content),
            len('{"guid": "a5cc4a8b-4b75-4c50-a488-852cc7e83176"}')
        )

        self.assertEqual(myResp['content-type'], 'application/json')

    def test_searchView_user_not_logged_in_post_valid_geomfile(self):
        """
        Test view if user is not logged in
        """
        myUploadFile = open('catalogue/fixtures/search-area.zip', 'rb')

        myClient = Client()

        myPostData = {
            'cloud_mean': 0,
            'searchdaterange_set-TOTAL_FORMS': 1,
            'searchdaterange_set-INITIAL_FORMS': 0,
            'searchdaterange_set-MAX_NUM_FORMS': 1,
            'searchdaterange_set-0-start_date': '2012-02-02',
            'searchdaterange_set-0-end_date': '2013-03-03',
            'geometry_file': myUploadFile
        }

        myResp = myClient.post(reverse('submitSearch', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        # we can't fix guid, so only test length of an response
        self.assertEqual(
            len(myResp.content),
            len('{"guid": "a5cc4a8b-4b75-4c50-a488-852cc7e83176"}')
        )

        self.assertEqual(myResp['content-type'], 'application/json')

    def test_searchView_user_not_logged_in_post_valid_aiogeometry(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()

        myPostData = {
            'cloud_mean': 0,
            'searchdaterange_set-TOTAL_FORMS': 1,
            'searchdaterange_set-INITIAL_FORMS': 0,
            'searchdaterange_set-MAX_NUM_FORMS': 1,
            'searchdaterange_set-0-start_date': '2012-02-02',
            'searchdaterange_set-0-end_date': '2013-03-03',
            'aoi_geometry': '20,-32,100'
        }

        myResp = myClient.post(reverse('submitSearch', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        # we can't fix guid, so only test length of an response
        self.assertEqual(
            len(myResp.content),
            len('{"guid": "a5cc4a8b-4b75-4c50-a488-852cc7e83176"}')
        )

        self.assertEqual(myResp['content-type'], 'application/json')

    def test_searchView_user_in_post_valid(self):
        """
        Test view if user is not logged in
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password'
        })

        myClient = Client()

        myPostData = {
            'cloud_mean': 0,
            'searchdaterange_set-TOTAL_FORMS': 1,
            'searchdaterange_set-INITIAL_FORMS': 0,
            'searchdaterange_set-MAX_NUM_FORMS': 1,
            'searchdaterange_set-0-start_date': '2012-02-02',
            'searchdaterange_set-0-end_date': '2013-03-03',
            'aoi_geometry': '20,-32,100'
        }

        myResp = myClient.post(reverse('submitSearch', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)

        # we can't fix guid, so only test length of an response
        self.assertEqual(
            len(myResp.content),
            len('{"guid": "a5cc4a8b-4b75-4c50-a488-852cc7e83176"}')
        )

        self.assertEqual(myResp['content-type'], 'application/json')
