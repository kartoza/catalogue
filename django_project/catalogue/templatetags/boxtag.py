"""
SANSA-EO Catalogue - Box element template tags

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
__date__ = '16/08/2012'
__copyright__ = 'South African National Space Agency'

from django import template
from django.utils.safestring import mark_safe
import logging
logger = logging.getLogger(__name__)
register = template.Library()


class BoxStartNode(template.Node):
    def __init__(self, div_id, div_classes=None):
        self.div_id = div_id.replace('\"', '').replace('\'', '')
        self.div_classes = div_classes
        if self.div_classes:
            self.div_classes = (
                self.div_classes.replace('\"', '').replace('\'', ''))
        #logger.info("BoxStartNode init - self.div_id : %s" % self.div_id)
        #logger.info("BoxStartNode init - self.div_classes : %s" % (
        #    self.div_classes,))

    def render(self, context):
        myClasses = (
            'ui-helper-reset ui-widget-content ui-state-highlight '
            'ui-corner-all')
        if self.div_classes:
            myClasses = "%s %s" % (myClasses, self.div_classes)
        myString = '''
          <div class="ui-widget append-bottom">
            <div class="%s"  style="min-height: 100px;" id="%s" >''' % (
            myClasses, self.div_id)
        return myString


@register.tag
def box_start(parser, token):
    # if the tag is like this {% box_start "foo-id" "foo-class barclass" %}
    # or if the tag is like this {% box_start foo-id "foo-class barclass" %}
    # token.split_contents would return 3 elements, box_start (the tag name),
    # "foo-id" and "foo-class...."
    # In our tag, the classes (css classes that will be added to the outer box)
    # is optional. Quotes are mandatory on the classes list param and optional
    # for the div_id
    myArgCount = len(token.split_contents())
    if myArgCount == 2:
        # split_contents() knows not to split quoted strings.
        tag_name, div_id = token.split_contents()
        return BoxStartNode(div_id)
    elif myArgCount == 3:
        # split_contents() knows not to split quoted strings.
        tag_name, div_id, div_classes = token.split_contents()
        # check div_classes is quoted and quoted using matching double or
        # single quotes
        if not (div_classes[0] == div_classes[-1] and
                div_classes[0] in ('"', "'")):
            raise template.TemplateSyntaxError(
                '%r tag\'s classes list argument should be in quotes' % (
                    tag_name,))
        return BoxStartNode(div_id, div_classes)
    else:
        raise template.TemplateSyntaxError(
            '%r tag requires either one or two args.' % (
                token.contents.split()[0],))


@register.simple_tag
def box_end():
    return mark_safe('''
        </div>
      </div>
    ''')


@register.simple_tag
def error_message_start(heading):
    return mark_safe('''
      <div class="ui-widget">
        <div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">
          <p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
          ''' + heading + '''
          </p>
          <div>
          ''')


@register.simple_tag
def error_message_end():
    return mark_safe('''
          </div>
        </div>
      </div>
      ''')
