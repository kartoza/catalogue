"""
SANSA-EO Catalogue - search_downloadSearchResult - test view for downloading
    search results

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
__date__ = '19/08/2013'
__copyright__ = 'South African National Space Agency'

from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client
from core.model_factories import UserF
from dictionaries.tests.model_factories import CollectionF
from model_factories import SearchF


class TestSearchViewsDownloadSearchResult(TestCase):
    """
    Tests search views.py downloadSearchResult method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadSearchResults_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadSearchResult',
                kwargs=myKwargTest)

    def test_downloadSearchResults_login_shp(self):
        """
        Test view if user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadSearchResult',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            ('attachment; filename=69d814b7-3164-42b9-9530-50ae77806da9-'
                'imagebounds.zip')
        )

    def test_downloadSearchResults_login_kml(self):
        """
        Test view if user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadSearchResult',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'}),
            {'kml': ''}
        )

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kml+xml')
        self.assertEqual(
            myResp['content-disposition'],
            ('attachment; filename=69d814b7-3164-42b9-9530-50ae77806da9-'
                'imagebounds.kml')
        )

    def test_downloadSearchResults_login_kmz(self):
        """
        Test view if user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadSearchResult',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'}),
            {'kmz': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kmz')
        self.assertEqual(
            myResp['content-disposition'],
            ('attachment; filename=69d814b7-3164-42b9-9530-50ae77806da9-'
                'imagebounds.kmz')
        )

    def test_downloadSearchResults_login_wrong_guid(self):
        """
        Test view if user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadSearchResult',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806db9'}),
            {'kmz': ''})

        self.assertEqual(myResp.status_code, 404)

    def test_downloadSearchResults_login_wrong_filetype(self):
        """
        Test view if user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse(
            'downloadSearchResult',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'}),
            {'xxx': ''}
        )

        self.assertEqual(myResp.status_code, 404)
