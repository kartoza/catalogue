"""
SANSA-EO Catalogue - reports_sensorSummaryTable - Reports views
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


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from catalogue.tests.model_factories import OpticalProductF
from search.tests.model_factories import SearchF, SearchRecordF

from dictionaries.tests.model_factories import (
    SatelliteInstrumentGroupF, InstrumentTypeF, SatelliteF,
    SatelliteInstrumentF, OpticalProductProfileF
)


class ReportsViews_sensorSummaryTable_Tests(TestCase):
    """
    Tests reports.py sensorSummaryTable method/view
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
                NoReverseMatch, reverse, 'sensorSummaryTable',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '34'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/sensorSummaryTable/34/')

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
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '34'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/sensorSummaryTable/34/')

    def test_myReports_stafflogin_generic(self):
        """
        Test view if user is logged as staff and basic functionality
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myInstType = InstrumentTypeF.create(**{
            'operator_abbreviation': 'ITOP 1'
        })
        mySatellite = SatelliteF.create(**{
            'operator_abbreviation': 'ST 1'
        })

        mySensor = SatelliteInstrumentGroupF.create(**{
            'id': 1,
            'instrument_type': myInstType,
            'satellite': mySatellite
        })
        SearchF.create(**{'satellites': [mySatellite]})

        mySatInst = SatelliteInstrumentF.create(**{
            'satellite_instrument_group': mySensor
        })

        myOPP = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst
        })
        myProduct = OpticalProductF.create(**{
            'product_profile': myOPP
        })

        SearchRecordF.create(**{
            'product': myProduct
        })
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '1'}))
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(unicode(myResp.context['mySensor']), u'ST 1 - ITOP 1')
        self.assertEqual(
            myResp.context['mySensorYearyStats'].__name__, 'sliceForDisplay')
        self.assertEqual(
            myResp.context['myResults']['Searches for this sensor'], 1)
        self.assertEqual(
            myResp.context['myResults']['Searches for all sensors'], 1)
        self.assertEqual(
            myResp.context['myResults']['Total products for this sensor'], 1)
        self.assertEqual(
            myResp.context['myResults']['Total products for all sensors'], 1)
        self.assertEqual(
            myResp.context['myResults']
            ['Total ordered products for this sensor'], 1)
        self.assertEqual(
            myResp.context['myResults']
            ['Total ordered products for all sensors'], 1)

        # check used templates
        myExpTemplates = ['sensorSummaryTable.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
