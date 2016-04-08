"""
SANSA-EO Catalogue - reports_sensor_fact_sheet - Reports views
    unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without express permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""
from django.http import Http404

__author__ = 'george@linfiniti.com'
__version__ = '0.1'
__date__ = '19/06/2014'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase, Client


class ReportsViewsSensorFactSheetTests(TestCase):
    """
    Tests reports.py sensor_fact_sheet method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_bad_url(self):
        """
        Test bad URL requests
        """
        test_kwargs = [{'test_args': 1}]

        for kwarg_test in test_kwargs:
            self.assertRaises(
                NoReverseMatch, reverse,
                'fact-sheet', kwargs=kwarg_test
            )

    def test_group(self):
        """
        Test that a correct URL format returns a 200 error for a exist
            SatelliteInstrumentGroup
        """
        client = Client()
        test_kwargs = [{'sat_abbr': 'LS-5', 'instrument_type': 'TM'}]

        for kwarg_test in test_kwargs:
            response = client.get(
                reverse('fact-sheet', kwargs=kwarg_test)
            )
            self.assertEqual(response.status_code, 200)
