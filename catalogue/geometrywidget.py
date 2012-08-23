# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - Custom form geometry widget
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
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import logging

from django import forms
from django.utils.safestring import mark_safe


class GeometryWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        """
        name - the name for the widget
        value - the value for the widget (e.g. when using the form to edit)
        attrs - the widget attributes as specified in the attrs={}
        area in the form class
        """
        logging.info('GeometryWidget started')
        # Make sure the field value is always valid
        if value is None:
            value = ''
        # Get any attributes the form designer may have specified
        attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # Always ensure there is an id attribute for the field
        attrs['type'] = 'hidden'
        if not 'id' in attrs:
            attrs['id'] = 'id_%s' % (name)
            # Lets customise the css a little now - with a big bold font
            # We append any user specified attributes to our custom ones
        if 'style' in attrs:
            attrs['style'] = (
                'font-weight: bold; font-size: 30px; height: 50px; %s'
                % attrs['style'])
        else:
            attrs['style'] = ''
            # Now we write our widget into a string
        myResult = '''<input %s value="%s"><div id="map" class="span-19 last">
        </div>
        <div id="map-panel" class="span-19 last">
            <div id="map-navigation-panel" class="span-7 append-1"></div>
            <div id="map-location"  class="span-4 append-1 small"></div>
            <div class="olControlScalebar span-6" id="map-scale"></div>
          </div>''' % (forms.util.flatatt(attrs), value)
        # Mark the widget html as safe - e.g. by escaping any special chars etc
        # and then return it
        return mark_safe(myResult)
