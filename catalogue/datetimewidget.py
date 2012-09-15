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
from dateutil.relativedelta import relativedelta

from django.utils.encoding import force_unicode
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
        myDefaultDateProperty = ''
        myDefaultDate = ''
        logging.info('Rendering date widget with %s' % theValue)
        if theValue is None:
            logging.info('Value is none - setting to empty string')
            theValue = ''
        final_attrs = self.build_attrs(
            attrs, type=self.input_type, name=theName)
        if theValue != '':
            logging.info('Value is not none : %s' % theValue)
            try:
                final_attrs['value'] = (
                    force_unicode(theValue.strftime(self.dformat)))
            except:
                final_attrs['value'] = force_unicode(theValue)
            myDefaultDate = '%s' % theValue.strftime(self.dformat)
            logging.info('MyDefaultDate is not none : %s' % myDefaultDate)
            myDefaultDateProperty = ', defaultDate: \'%s\'' % (
                theValue.strftime(self.dformat,))
            logging.info('MyDefaultDateProperty is : %s' % (
                myDefaultDateProperty,))
        if not 'id' in final_attrs:
            final_attrs['id'] = u'%s_id' % (theName)
        myId = final_attrs['id']
        #set defaults to start and end days of month if not set explicitly
        myDate = datetime.date.today()
        if 'start' in theName and not myDefaultDate:
            myDefaultDate = '01-%s-%s' % (
                str(myDate.month), str(myDate.year))
        elif 'end' in theName and not myDefaultDate:
            # work out the last day of the current month
            #myEndDate = datetime.date.today() + relativedelta(months=+1)
            #myEndDate = datetime.date( myFutureDate.year(),
            #    myFutureDate.month(), 1) - relativedelta(days=-1)

            # work out yesterdays date
            myEndDate = datetime.date.today() + relativedelta(days=-1)
            myDefaultDate = '%s-%s-%s' % (
                myEndDate.day, myEndDate.month, myEndDate.year)
        elif not myDefaultDate or myDefaultDate == '':
            myDefaultDate = datetime.date.today() + relativedelta(days=-1)
            myDefaultDate = '%s-%s-%s' % (
                myDefaultDate.day, myDefaultDate.month, myDefaultDate.year)

        myA = u'''
<script type="text/javascript">
    $(function() {
        //acivate widget on document ready
        $('#%(id)s').sansa_datepicker();
    });
</script>
<div %(attrs)s ></div>
<input type="hidden" name="%(name)s" id="%(id)s" value="%(defaultDate)s" />''' % {
            'id': myId, 'defaultDatePropery': myDefaultDateProperty,
            'defaultDate': myDefaultDate, 'name': theName, 'attrs':flatatt(final_attrs)}

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
