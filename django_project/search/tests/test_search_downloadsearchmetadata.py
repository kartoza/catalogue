"""
SANSA-EO Catalogue - search_downloadSearchMetadata - test view for downloading
    search Metadata

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


class TestSearchViewsDownloadSearchMetadata(TestCase):
    """
    Tests search views.py downloadSearchResultMetadata method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadSearchMetadata_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadSearchResultMetadata',
                kwargs=myKwargTest)

    def test_downloadSearchResults_login_xml(self):
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
            'downloadSearchResultMetadata',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'}),
            {'xxx': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            ('attachment; filename=SANSA-Search-69d814b7-3164-42b9-9530-'
                '50ae77806da9-Metadata.zip')
        )

    def test_downloadSearchResults_login_html(self):
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
            'downloadSearchResultMetadata',
            kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'}),
            {'html': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            ('attachment; filename=SANSA-Search-69d814b7-3164-42b9-9530-'
                '50ae77806da9-Metadata.zip')
        )
