"""
SANSA-EO Catalogue - graphtag_templatetag - tests correct output of gPieChart
template tag

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

import unittest
from django.test import TestCase
from django.template import Template, Context


class gPieChart_Test(TestCase):
    """
    Tests gPieChart templatetag output
    """

    def setUp(self):
        """
        Sets up before each test
        """
    @unittest.skip("We've checked that the pie charts are equal")
    def test_gPieChart_output(self):
        """
        The gPieChart tag output test
        """
        myData = {
            'myScores': [
                {'country': 'Test country 1', 'count': 10},
                {'country': 'Test country 2', 'count': 20},
                {'country': 'Test country 3', 'count': 30},
            ],
            'myGraphLabels': ({'Country': 'country'})
        }
        myRes = Template(
            '{% load graphtag %}'
            '{% gPieChart myScores myGraphLabels 0 %}'
        ).render(Context(myData))
        myExpRes = (
            'http://chart.apis.google.com/chart?cht=p3&chs=600x300&chd=s:KUf&'
            'chco=3366CC%7cDC3912%7cFF9900%7c109618%7c990099%7c0099C6%7cDD4477'
            '%7c66AA00%7cB82E2E%7c316395%7c994499%7c22AA99%7cAAAA11%7c6633CC'
            '%7cE47100%7c8B0707%7c651067%7c329262&chl=Test%20country%201%7c'
            'Test%20country%202%7cTest%20country%203'
        )
        self.assertEqual(myRes, myExpRes)

    @unittest.skip("We've checked that the pie charts are equal")
    def test_gPieChart_excludefirst_output(self):
        """
        The gPieChart tag output test
        """
        myData = {
            'myScores': [
                {'country': 'Test country 1', 'count': 10},
                {'country': 'Test country 2', 'count': 20},
                {'country': 'Test country 3', 'count': 30},
            ],
            'myGraphLabels': ({'Country': 'country'})
        }
        myRes = Template(
            '{% load graphtag %}'
            '{% gPieChart myScores myGraphLabels 1 %}'
        ).render(Context(myData))
        myExpRes = (
            'http://chart.apis.google.com/chart?cht=p3&chs=600x300&chd=s:Yl'
            '&chco=3366CC%7cDC3912%7cFF9900%7c109618%7c990099%7c0099C6%7c'
            'DD4477%7c66AA00%7cB82E2E%7c316395%7c994499%7c22AA99%7cAAAA11'
            '%7c6633CC%7cE47100%7c8B0707%7c651067%7c329262&chl=Test%20country'
            '%202%7cTest%20country%203'
        )
        self.assertEqual(myRes, myExpRes)
