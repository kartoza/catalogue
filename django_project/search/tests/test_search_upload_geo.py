"""
SANSA-EO Catalogue - search_upload_geo - test view for extracting geometry from
    uploaded geometry files

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
__date__ = '27/01/2014'
__copyright__ = 'South African National Space Agency'

from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class TestSearchViewsUploadGeo(TestCase):
    """
    Tests search views.py upload_geo method/view
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
                NoReverseMatch, reverse, 'upload_geo',
                kwargs=myKwargTest)

    def test_search_view_user_not_logged_in_get(self):
        """
        Test view if user is not logged in
        """

        myClient = Client()

        self.assertRaises(
            ValueError, myClient.get, reverse('upload_geo', kwargs={})
        )

    def test_searchView_user_not_logged_in_post_no_file(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()

        myPostData = {
            'file_upload': ''
        }

        self.assertRaises(
            ValueError, myClient.post, reverse('upload_geo', kwargs={}),
            myPostData
        )

    def test_searchView_user_not_logged_in_post_shp(self):
        """
        Test view if user is not logged in
        """
        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area.zip', 'rb')

        myClient = Client()

        myPostData = {
            'file_upload': myUploadFile
        }

        myResp = myClient.post(reverse('upload_geo', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(myResp['Content-Type'], 'application/json')
        self.assertEqual(
            myResp.content, (
                '{"wkt": "POLYGON ((28.6920935798624583 -22.3362862047120849, '
                '28.6998542329746975 -22.3360697290325270, 28.7002763605498394'
                ' -22.3424557615795543, 28.6913683863359310 -22.34292118429060'
                '99, 28.6913683863359310 -22.3429211842906099, 28.691043672816'
                '5905 -22.3385050804275807, 28.6920935798624583 -22.3362862047'
                '120849))"}')
        )

    def test_searchView_user_not_logged_in_post_kml(self):
        """
        Test view if user is not logged in
        """
        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area.kml', 'rb')

        myClient = Client()

        myPostData = {
            'file_upload': myUploadFile
        }

        myResp = myClient.post(reverse('upload_geo', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(myResp['Content-Type'], 'application/json')
        self.assertEqual(
            myResp.content, (
                '{"wkt": "POLYGON ((19.6655270000000009 -30.2400860000000016, '
                '20.4345700000000008 -31.5036290000000001, 22.3681640000000002'
                ' -31.7281669999999991, 24.6533200000000008 -31.18460899999999'
                '82, 22.8515629999999987 -29.1521609999999995, 19.665527000000'
                '0009 -30.2400860000000016))"}')
        )

    def test_searchView_user_not_logged_in_post_invalid_file(self):
        """
        Test view if user is not logged in
        """
        # prepare file for upload
        myUploadFile = open('core/__init__.py', 'rb')

        myClient = Client()

        myPostData = {
            'file_upload': myUploadFile
        }

        myResp = myClient.post(reverse('upload_geo', kwargs={}), myPostData)

        self.assertEqual(myResp.status_code, 500)
        self.assertEqual(myResp['Content-Type'], 'application/json')
        self.assertEqual(
            myResp.content, '{"error": "File needs to be KML/KMZ/ZIP"}'
        )

    def test_searchView_user_not_logged_in_post_invalid_geometry(self):
        """
        Test view if user is not logged in
        """
        # prepare file for upload
        myUploadFile = open('catalogue/fixtures/search-area-invalid.zip', 'rb')

        myClient = Client()

        myPostData = {
            'file_upload': myUploadFile
        }

        self.assertRaises(
            RuntimeError, myClient.post, reverse('upload_geo', kwargs={}),
            myPostData
        )
