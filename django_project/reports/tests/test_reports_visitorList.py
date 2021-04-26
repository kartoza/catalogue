"""
SANSA-EO Catalogue - reports_visitorList - Reports views
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
__date__ = '20/08/2013'
__copyright__ = 'South African National Space Agency'

import unittest
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from catalogue.tests.model_factories import VisitF


class ReportsViews_visitorList_Tests(TestCase):
    """
    Tests reports.py visitorList method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_myReports_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'visitorList',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}))
        self.assertEqual(myResp.status_code, 302)

    def test_myReports_userlogin(self):
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
                'visitorList',
                kwargs={}))
        self.assertEqual(myResp.status_code, 302)

    def test_myReports_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        VisitF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('visitorList', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(len(myResp.context['records']), 1)
        # check used templates
        myExpTemplates = [
            'visitors.html', 'base.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html',
            'django_tables2/custom-table.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    @unittest.skip("Skip this test")
    def test_myReports_stafflogin_pdf(self):
        """
        Test view if pdf is requested
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        VisitF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(reverse('visitorList', kwargs={}), {'pdf': ''})

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['records']), 1)
        # check used templates
        myExpTemplates = ['<Unknown Template>']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(myResp['content-type'], 'application/pdf')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename="visitors.pdf"'
        )

    def test_myReports_stafflogin_invalidpage(self):
        """
        Test view if user is logged in, specifying invalid page parameter
        View will default to page 1
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        VisitF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}), {'page': 'this is a new page!'})
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['records']), 1)
        # check used templates
        myExpTemplates = [
            'visitors.html', 'base.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html',
            'django_tables2/custom-table.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_myReports_stafflogin_outboundpage(self):
        """
        Test view if user is logged in, specifying outbound page parameter
        View will default to page 1
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        VisitF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}), {'page': '10001'})
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['records']), 1)
        # check used templates
        myExpTemplates = [
            'visitors.html', 'base.html',
            'pipeline/css.html', 'pipeline/js.html', 'menu.html',
            'useraccounts/menu_content.html',
            'django_tables2/custom-table.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
