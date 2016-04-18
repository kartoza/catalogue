"""
SANSA-EO Catalogue - search_searchGuid - test view for displaying search
    based on guid

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

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from dictionaries.tests.model_factories import CollectionF
from .model_factories import SearchF

from ..forms import AdvancedSearchForm


class SearchViews_searchGuid_Tests(TestCase):
    """
    Tests search views.py searchguid method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_searchGuid_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'searchGuid',
                kwargs=myKwargTest)

    def test_searchGuid_user_not_loged(self):
        """
        Test view if user is not logged in
        """
        SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[CollectionF.create(), CollectionF.create()]
        )

        myClient = Client()
        myResp = myClient.get(
            reverse(
                'searchGuid',
                kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'})
        )
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                '/accounts/signin/?next=/search/'
                '69d814b7-3164-42b9-9530-50ae77806da9/')
        )

    def test_searchGuid_user(self):
        """
        Test view if user is logged in
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myCol1 = CollectionF.create(**{'id': 10000, 'name': 'My Collection 1'})
        myCol2 = CollectionF.create(**{'id': 10001, 'name': 'My Collection 2'})

        mySearch = SearchF.create(
            guid='69d814b7-3164-42b9-9530-50ae77806da9',
            collections=[myCol1, myCol2]
        )

        myForm = AdvancedSearchForm(instance=mySearch)

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'searchGuid',
                kwargs={'theGuid': '69d814b7-3164-42b9-9530-50ae77806da9'})
        )
        self.assertEqual(myResp.status_code, 200)

        myExpTemplates = [
            'page.html', u'base-fluid.html', u'pipeline/css.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'search_form/content-1.html',
            u'search_form/content-2.html', u'search_form/content-3.html',
            u'search_form/content-4.html', u'search_form/content-5.html',
            u'pipeline/js.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(mySearch, myResp.context['mysearch'])
        self.assertEqual(
            myForm.__class__, myResp.context['searchform'].__class__)
        self.assertEqual(
            myResp.context['listreeoptions'], (
                '[{"values": [], "val": "cc10000", "key": "My Collection 1"}, '
                '{"values": [], "val": "cc10001", "key": "My Collection 2"}]')
        )
        self.assertEqual(
            myResp.context['selected_options'], (
                '[{"values": [], "val": "cc10000", "key": "My Collection 1"}, '
                '{"values": [], "val": "cc10001", "key": "My Collection 2"}]')
        )
