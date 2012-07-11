"""
SANSA-EO Catalogue - boxtag_templatetag - tests correct output of boxtag
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
__version__ = '0.1'
__date__ = '11/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from django.template import Template, Context


class BoxTag_Test(TestCase):
    """
    Tests BoXTag templatetags output
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_box_start_output_no_classes(self):
        """
        The box_start tag output test
        """
        myRes = Template(
            '{% load boxtag %}'
            '{% box_start "box-welcome" %}'
            ).render(Context())
        myExpRes = """
          <div class="ui-widget append-bottom">
            <div class="ui-helper-reset ui-widget-content ui-state-highlight ui-corner-all"  style="min-height: 100px;" id="box-welcome" >"""

        self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes,
            enclose_in='#'))

    def test_box_start_output_with_classes(self):
        """
        The box_start tag output test, using CSS classes (3rd paramter)
        """
        myRes = Template(
            '{% load boxtag %}'
            '{% box_start "box-welcome" "span-22" %}'
            ).render(Context())
        myExpRes = """
          <div class="ui-widget append-bottom">
            <div class="ui-helper-reset ui-widget-content ui-state-highlight ui-corner-all span-22"  style="min-height: 100px;" id="box-welcome" >"""

        self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes,
            enclose_in='#'))

    def test_box_end_output(self):
        """
        The box_end tag output test
        """
        myRes = Template(
            '{% load boxtag %}'
            '{% box_end %}'
            ).render(Context())
        myExpRes = """
        </div>
      </div>
    """
        self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes,
            enclose_in='#'))

    def test_error_message_start_output(self):
        """
        The error_message_start tag output test
        """
        myRes = Template(
            '{% load boxtag %}'
            '{% error_message_start "Test message" %}'
            ).render(Context())
        myExpRes = """
      <div class="ui-widget">
        <div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">
          <p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
          Test message
          </p>
          <div>
          """

        self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes,
            enclose_in='#'))

    def test_error_message_end_output(self):
        """
        The error_message_end tag output test
        """
        myRes = Template(
            '{% load boxtag %}'
            '{% error_message_end %}'
            ).render(Context())
        myExpRes = """
          </div>
        </div>
      </div>
      """

        self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes,
            enclose_in='#'))
