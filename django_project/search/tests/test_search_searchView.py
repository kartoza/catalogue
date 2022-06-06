"""
SANSA-EO Catalogue - search_searchView - test view for basic search page

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

from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from dictionaries.tests.model_factories import CollectionF

from search.forms import AdvancedSearchForm
from search.views import DateRangeInlineFormSet


class TestSearchViewsSearchView(TestCase):
    """
    Tests search views.py searchView method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_searchView_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'theId': 'testtest'}, {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'search',
                kwargs=myKwargTest)

    def test_searchView_user_not_logged_in(self):
        """
        Test view if user is not logged in
        """

        CollectionF.create(**{'id': 10000, 'name': 'My Collection 1'})
        CollectionF.create(**{'id': 10001, 'name': 'My Collection 2'})

        myClient = Client()
        myResp = myClient.get(reverse('search', kwargs={}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            AdvancedSearchForm().__class__,
            myResp.context['searchform'].__class__
        )

        self.assertEqual(
            DateRangeInlineFormSet().__class__,
            myResp.context['dateformset'].__class__
        )

        self.assertEqual(
            myResp.context['listreeoptions'], (
                '[{"values": [], "val": "cc10000", "key": "My Collection 1"}, '
                '{"values": [], "val": "cc10001", "key": "My Collection 2"}]')
        )

        self.assertEqual(
            myResp.context['selected_options'], []
        )

        self.assertEqual(
            myResp.context['searchlistnumber'],
            settings.RESULTS_NUMBER
        )

    def test_searchView_user_is_logged_in(self):
        """
        Test view if user is logged in
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        CollectionF.create(**{'id': 10000, 'name': 'My Collection 1'})
        CollectionF.create(**{'id': 10001, 'name': 'My Collection 2'})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('search', kwargs={}))

        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            AdvancedSearchForm().__class__,
            myResp.context['searchform'].__class__
        )

        self.assertEqual(
            DateRangeInlineFormSet().__class__,
            myResp.context['dateformset'].__class__
        )

        self.assertEqual(
            myResp.context['listreeoptions'], (
                '[{"values": [], "val": "cc10000", "key": "My Collection 1"}, '
                '{"values": [], "val": "cc10001", "key": "My Collection 2"}]')
        )

        self.assertEqual(
            myResp.context['selected_options'], []
        )

        self.assertEqual(
            myResp.context['searchlistnumber'],
            settings.RESULTS_NUMBER
        )
