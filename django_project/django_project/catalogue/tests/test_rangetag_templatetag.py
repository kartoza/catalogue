"""
SANSA-EO Catalogue - rangetag_templatetag - tests correct output of get_range
    filter

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
__date__ = '07/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from django.template import Template, Context


class RangeTag_Test(TestCase):
    """
    Tests RangeTag filter output
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_get_range_filter(self):
        """
        The get_range filter output test
        """
        myRes = Template(
            "{% load rangetag %}"
            "<ul>{% for i in 3|get_range %}"
            "<li>{{ i }}. Do something</li>"
            "{% endfor %}</ul>"
        ).render(Context())

        myExpRes = (
            '<ul><li>1. Do something</li><li>2. Do something</li><li>3. Do som'
            'ething</li></ul>'
        )
        self.assertEqual(myRes, myExpRes)
