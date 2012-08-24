"""
SANSA-EO Catalogue - Custom form widget SliderWidget

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

from django import forms
from django.utils.safestring import mark_safe


# Our custom widget inherits from TextInput
class SliderWidget(forms.TextInput):
    # we simply overload the render method with our own version
    def render(self, name, value, attrs=None):
        """
        name - the name for the widget
        value - the value for the widget (e.g. when using the form to edit)
        attrs - the widget attributes as specified in the attrs={}
                   area in the form class
        """
        # Make sure the field value is always valid
        if value is None:
            value = ''
        # Get any attributes the form designer may have specified
        attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # Always ensure there is an id attribute for the field
        if not 'id' in attrs:
            attrs['id'] = '%s_id' % (name)
        # Now we write our widget into a string
        myId = attrs['id']
        myName = attrs['name']
        myResult = """<div id="%sSlider"></div> <input name="%s" type="text"
        id="%s" value="%s"></input>""" % (myId, myName, myId, value)

        # Mark the widget html as safe - e.g. by escaping any special chars etc
        # and then return it
        return mark_safe(myResult)
