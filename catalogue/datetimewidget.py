# -*- coding: utf-8 -*-
# widgets.py
#
# To use you have to put calendar/ (from http://www.dynarch.com/projects/calendar/)
# to your MEDIA folder and then include such links on your page:
# <!-- calendar -->
# <link rel="stylesheet" type="text/css" href="{{ MEDIA_URL }}calendar/calendar-win2k-cold-2.css" />
#<script type="text/javascript" src="{{ MEDIA_URL }}calendar/calendar.js"></script>
# <!-- this is translation file - choose your language here -->
#<script type="text/javascript" src="{{ MEDIA_URL }}calendar/lang/calendar-pl.js"></script>
#<script type="text/javascript" src="{{ MEDIA_URL }}calendar/calendar-setup.js"></script>
#<!-- /calendar -->

from django.utils.encoding import force_unicode
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
import datetime, time
import logging
from dateutil.relativedelta import relativedelta

# Support dmy formats (see http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
        '%d-%m-%Y',                         # '25-10/2006'
        '%d/%m/%Y', '%d/%m/%y',             # '25/10/2006', '25/12/06'
        '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
        '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
        )
# DATETIMEWIDGET

class DateTimeWidget(forms.DateInput):
    dformat = '%d-%m-%Y'
    def render(self, name, value, attrs=None):
        myDefaultDateProperty = ""
        myDefaultDate = ""
        logging.info("Rendering date widget with %s" % value)
        if value is None: 
          logging.info("Value is none - setting to empty string")
          value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
          logging.info("Value is not none : %s" % value)
          try:
            final_attrs['value'] = \
                                   force_unicode(value.strftime(self.dformat))
          except:
            final_attrs['value'] = \
                                   force_unicode(value)
          myDefaultDate = "%s" % value.strftime(self.dformat)
          logging.info("MyDefaultDate is not none : %s" % myDefaultDate )
          myDefaultDateProperty = ", defaultDate: '%s'" % value.strftime(self.dformat)
          logging.info("MyDefaultDateProperty is : %s" % myDefaultDateProperty )
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']

        #set defaults to start and end days of month if not set explicitly
        myDate = datetime.date.today()
        if "start" in name and not myDefaultDate:
          myDefaultDate = "01-%s-%s" % ( str(myDate.month), str(myDate.year))
        elif "end" in name and not myDefaultDate:
          # work out the last day of the current month
          #myEndDate = datetime.date.today() + relativedelta(months=+1)
          #myEndDate = datetime.date( myFutureDate.year(), myFutureDate.month(), 1) - relativedelta(days=-1)

          # work out yesterdays date
          myEndDate = datetime.date.today() + relativedelta(days=-1)
          myDefaultDate = "%s-%s-%s" % ( myEndDate.day, myEndDate.month, myEndDate.year )
        #elif not myDefaultDate or myDefaultDate == '':
        #  myDefaultDate = datetime.date.today() + relativedelta(days=-1)
        else:
          myDefaultDate = "%s-%s-%s" % ( myDefaultDate.day, myDefaultDate.month, myDefaultDate.year )


        a = u'''
        <script type="text/javascript">
          $(function() {
              $("#%s-widget").datepicker({
                minDate: new Date(1970, 1, 1),
                yearRange: "1972:+1",
                dateFormat: 'dd-m-yy',
                maxDate: '+1Y',
                changeMonth: true,
                changeYear: true,
                onChangeMonthYear: function(year, month, inst) { 
                  try {
                    if (changingDate) {
                      return;
                    }
                  } catch(e) {
                    //do nothing - handler for undefined reference to changingDate
                  }
                  changingDate = true;
                  myId = "%s";
                  if ( myId.substring(0,8) == "id_start")
                  {
                    $("#%s-widget").datepicker("setDate", "01-" + month + "-" + year);
                  }
                  else if ( myId.substring(0,6) == "id_end")
                  {
                    //calculate the last day of the month - see http://javascript.about.com/library/bllday.htm
                    var myLastDay = new Date(year, month, 0).getDate();
                    $("#%s-widget").datepicker("setDate", myLastDay + "-" + month + "-" + year);
                  }
                  var myDate = $("#%s-widget").datepicker("getDate"); //returns a js date object
                  var myDay = myDate.getDate();
                  if ( myDay < 10 ) //zero pad the day
                  {
                    myDay = "0" + myDay;
                  }
                  //+1 below because js months start at 0
                  var myMonth = myDate.getMonth() + 1;
                  if ( myMonth < 10 ) //zero pad the day
                  {
                    myMonth = "0" + myMonth;
                  }
                  var myYear  = myDate.getFullYear();
                  var myTextDate = myDay + "-" + myMonth + "-" + myYear;
                  $('#%s').val( myTextDate );
                  changingDate = false;
                },
                onSelect: function( theDate, inst)
                  {
                    check_search_dates();
                    $('#%s').val( theDate );
                  }
                %s
                });
            $("#%s-widget").datepicker("setDate", "%s");
          });
        </script>
        <div id="%s-widget"></div>
        <input type="hidden" name="%s" id="%s" value="%s" />''' % (id, id, id, id, id, id, id, myDefaultDateProperty, id, myDefaultDate, id, name, id, myDefaultDate)
        return mark_safe(a)


    def value_from_datadict(self, data, files, name):
        logging.info("Getting date value from data dict")
        empty_values = forms.fields.EMPTY_VALUES
        value = data.get(name, None)
        if value in empty_values:
          return None
        if isinstance(value, datetime.datetime):
          return value
        if isinstance(value, datetime.date):
          return datetime.datetime(value.year, value.month, value.day)
        for format in DATE_FORMATS:
          try:
            myDate = datetime.datetime(*time.strptime(value, format)[:6])
            logging.info("Parsed date is: " + str(myDate))
            return myDate
          except ValueError:
            continue
        return None


