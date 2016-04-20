"""
SANSA-EO Catalogue - others_showThumbPage - Others views
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
from datetime import datetime

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF

from dictionaries.tests.model_factories import (
    OpticalProductProfileF, SpectralModeF, SatelliteInstrumentF,
    SatelliteInstrumentGroupF, SatelliteF
)

from .model_factories import OpticalProductF


class OthersViews_showThumbPage_Tests(TestCase):
    """
    Tests others.py showThumbPage method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_showThumbPage_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showThumbPage',
                kwargs=myKwargTest)

    @unittest.skip("Skip this test")
    def test_showThumbPage_nologin(self):
        """
        Test view if user is not logged in
        """

        OpticalProductF.create(**{
            'id': 123
        })

        myClient = Client()
        myResp = myClient.get(
            reverse('showThumbPage', kwargs={'theId': '123'})
        )

        self.assertEqual(myResp.status_code, 200)

        myExpResp = (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://'
            'www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http:/'
            '/www.w3.org/1999/xhtml">\n  <head>\n  </head>\n  <body >\n      '
            'You need to be logged in to see this page...<a href="/accounts/si'
            'gnin/">Login</a>\n  </body>\n</html>\n'
        )

        self.assertEqual(myResp.content, myExpResp)

        # check used templates
        myExpTemplates = ['thumbnail.html', u'popupbase.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    @unittest.skip("Skip this test")
    def test_showThumbPage_userlogin(self):
        """
        Test view if user is logged as user
        """

        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        mySat = SatelliteF.create(**{
            'abbreviation': 'mySAT'
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'satellite': mySat
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'SuperSpectralMode'
        })

        myOPP = OpticalProductProfileF.create(**{
            'spectral_mode': mySpecMode,
            u'satellite_instrument': mySatInst
        })

        OpticalProductF.create(**{
            'id': 123,
            'unique_product_id': 'PROD123',
            'product_profile': myOPP,
            'product_acquisition_start': datetime(2012, 12, 12, 12, 00),
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('showThumbPage', kwargs={'theId': '123'}))

        self.assertEqual(myResp.status_code, 200)

        myExpResp = (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://'
            'www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http:/'
            '/www.w3.org/1999/xhtml">\n  <head>\n  </head>\n  <body >\n      '
            '<table id="gradient-style" summary="Thumbnail Preview" style="wid'
            'th:100%; margin:0px;">\n        <thead>\n        </thead>\n      '
            '  <tfoot>\n        </tfoot>\n        <tbody>\n            <tr><th'
            '>Sensor:SuperSpectralMode</th></tr>\n            <tr><td><center>'
            '<img src="/thumbnail/123/large/"></center></td></tr>\n        </t'
            'body>\n      </table>\n    </div>\n  </body>\n</html>\n'
        )

        self.assertEqual(myResp.content, myExpResp)

        # check used templates
        myExpTemplates = ['thumbnail.html', u'popupbase.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
