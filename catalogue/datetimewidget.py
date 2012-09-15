# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - Datetime form widget

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

# widgets.py
#
# To use you have to put calendar/ (
#  from http://www.dynarch.com/projects/calendar/)
# to your MEDIA folder and then include such links on your page:
# <!-- calendar -->
# <link rel="stylesheet" type="text/css"
#   href="{{ MEDIA_URL }}calendar/calendar-win2k-cold-2.css" />
# <script type="text/javascript"
#   src="{{ MEDIA_URL }}calendar/calendar.js"></script>
# <!-- this is translation file - choose your language here -->
# <script type="text/javascript"
#   src="{{ MEDIA_URL }}calendar/lang/calendar-pl.js"></script>
# <script type="text/javascript"
#   src="{{ MEDIA_URL }}calendar/calendar-setup.js"></script>
# <!-- /calendar -->

import datetime
import time
import logging

from django import forms
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

# Support dmy formats
# (see http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
    '%d-%m-%Y',               # '25-10/2006'
    '%d/%m/%Y', '%d/%m/%y',   # '25/10/2006', '25/12/06'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)


# DATETIMEWIDGET
class DateTimeWidget(forms.DateInput):
    dformat = '%d-%m-%Y'

    def render(self, theName, theValue, attrs=None):
        # generate attrs
        myFinal_attrs = self.build_attrs(
            attrs, type=self.input_type, name=theName)
        # IMPORTANT: save form field id, later used in form->object translation
        myId = myFinal_attrs['id']

        # update widget id (append _widget)
        myFinal_attrs['id'] = myFinal_attrs['id'] + '_widget'

        if theValue:
            # logging for Sentry, not really needed, but not sure if there is
            # a case when theValue is actually required
            # TRAP TRIGGER
            logging.error('DateTimeWidget theValue is not None: %s' % theValue)

        myA = u'''
<script type="text/javascript">
$(function() {
    //acivate widget on document ready
    $('#%(id)s_widget').sansa_datepicker();
});
</script>
<div %(attrs)s>
<input type="hidden" name="%(name)s" id="%(id)s"/>
</div>
''' % {'id': myId, 'name': theName, 'attrs': flatatt(myFinal_attrs)}

        return mark_safe(myA)

    def value_from_datadict(self, theData, theFiles, theName):
        logging.info('Getting date value from data dict')
        myEmptyValues = forms.fields.EMPTY_VALUES
        myValue = theData.get(theName, None)
        if myValue in myEmptyValues:
            return None
        if isinstance(myValue, datetime.datetime):
            return myValue
        if isinstance(myValue, datetime.date):
            return datetime.datetime(myValue.year, myValue.month, myValue.day)
        for myDateFormat in DATE_FORMATS:
            try:
                myDate = datetime.datetime(*time.strptime(
                    myValue, myDateFormat)[:6])
                logging.info('Parsed date is: %s' % str(myDate))
                return myDate
            except ValueError:
                continue
        return None
