"""
SANSA-EO Catalogue - get_range template filter

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

from django.template import Library

register = Library()


@register.filter
def get_range(value):
    """
    From http://djangosnippets.org/snippets/1357/
    Filter - returns a list containing range made from given value
    Usage (in template):
    <ul>{% for i in 3|get_range %}
    <li>{{ i }}. Do something</li>
    {% endfor %}</ul>
    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>
    Instead of 3 one may use the variable set in the views
    """
    return [v + 1 for v in range(value)]
