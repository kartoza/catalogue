"""
SANSA-EO Catalogue - others_VisitorMap - Others views
    unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.2'
__date__ = '09/08/2013'
__copyright__ = 'South African National Space Agency'


import unittest
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF


class OthersViews_visitorMap_Tests(TestCase):
    """
    Tests others.py visitorMap method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_visitorMap_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'visitorMap',
                kwargs=myKwargTest)

    def test_visitorMap_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'visitorMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        # self.assertEqual(
        #     myResp.context['app_path'], u'/visitormap/')

    def test_visitorMap_userlogin(self):
        """
        Test view if user is logged as user
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'visitorMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        # self.assertEqual(
        #     myResp.context['app_path'], u'/visitormap/')

    @unittest.skip("Sometimes passed sometimes error")
    def test_visitorMap_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        # this assertion depends on the IP of the server that runs tests
        # ATM we can't reliably test this
        # self.assertEqual(
        #     len(myResp.context['myMessages']), 8)
        self.assertEqual(
            len(myResp.context['myExtents']), 16)
        definitions = myResp.context['myLayerDefinitions']
        self.assertEqual(
            len(definitions),
            2,
            str(definitions))
        myExpLaylersList = (
            '[TMSOverlay,visitors]'
        )
        self.assertEqual(
            myResp.context['myLayersList'], myExpLaylersList)

        myExpActiveBaseMap = 'TMSOverlay'
        self.assertEqual(
            myResp.context['myActiveBaseMap'], myExpActiveBaseMap)
        # check used templates
        myExpTemplates = [
            'simpleMap.html', u'base.html',
            u'pipeline/css.html', u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
