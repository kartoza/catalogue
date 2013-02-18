"""
SANSA-EO Catalogue - others_mapHelp - Others views
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
__version__ = '0.1'
__date__ = '22/11/2012'
__copyright__ = 'South African National Space Agency'

import datetime
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class OthersViews_mapHelp(TestCase):
    """
    Tests others.py mapHelp method/view
    """
    fixtures = [
        'test_user.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_contact_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'mapHelp',
                kwargs=myKwargTest)

    def test_contact_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(reverse('mapHelp', kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        # check used templates
        myExpTemplates = ['mapHelp.html', u'base.html', u'menu.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
