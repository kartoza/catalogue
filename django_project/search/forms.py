"""
SANSA-EO Catalogue - Catalogue forms

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
# Get an instance of a logger
logger = logging.getLogger(__name__)

import datetime

from django import forms
from django.forms.models import BaseInlineFormSet


from django.forms import HiddenInput

from catalogue.fields import IntegersCSVIntervalsField
from catalogue.datetimewidget import DateTimeWidget
from catalogue.aoigeometry import AOIGeometryField


from .models import Search


# Support dmy formats (see
#    http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
    '%d-%m-%Y',               # '25-10-2005'
    '%d/%m/%Y', '%d/%m/%y',   # '25/10/2006', '25/12/06'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)


class DateRangeForm(forms.ModelForm):
    class Meta:
        widgets = {
            'start_date': HiddenInput,
            'end_date': HiddenInput
        }


class DateRangeFormSet(BaseInlineFormSet):
    """
    Date range search formsets with validation

    This class needs some override to handle the case of
    missing (deleted) forms.

    """
    def clean(self):
        """
        Delete incomplete forms
        TODO: simplify overlapping ranges (or raise exception), priority: low
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on
            # its own
            return
        empty_forms = []
        for i in range(0, len(self.forms)):
            form = self.forms[i]
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            # Checks for empty forms
            if not(start_date and end_date) or self._should_delete_form(form):
                empty_forms.append(i)
            elif start_date > end_date:
                raise forms.ValidationError, (
                    'Start date must be before or equal to end date.')
        # Delete empty/deleted forms
        empty_forms.reverse()
        for i in empty_forms:
            del(self.forms[i])
        self.management_form.cleaned_data['TOTAL_FORMS'] = len(self.forms)
        if not len(self.forms):
            raise forms.ValidationError, 'At least one date range is required.'


class AdvancedSearchForm(forms.ModelForm):
    """
    Let the user perform searches on sensors, by date and/or geometry
    digitised on map.
    """
    # keywords = forms.CharField(widget=forms.TextInput(
    #    attrs={'cols':'32'}),required=False)
    # Note1: the help_text strings are duplicated from the model help text
    #        since I didnt find a simple way to reuse it if adding custom
    #        fields
    # Note2: Only custom fields are added here. Fields that need no tweaking
    #        are pulled by the form generator directly from the model

    # ABP: the common part: will be searched on GenericProducts class only
    start_datepicker = forms.DateField(
        widget=DateTimeWidget(
            attrs={
                'title': 'Choose the start date for this date range.',
                'data-date_focus': 'start'}),
        required=False, label='Start date', input_formats=DATE_FORMATS,
        error_messages={
            'required': 'Entering a start date for your search is required.'},
        help_text='Start date is required. DD-MM-YYYY.')

    end_datepicker = forms.DateField(
        widget=DateTimeWidget(
            attrs={
                'title': 'Choose the end date for this date range.',
                'data-date_focus': 'end'}),
        required=False, label='End date', input_formats=DATE_FORMATS,
        error_messages={
            'required': 'Entering an end date for your search is required.'},
        help_text='End date is required. DD-MM-YYYY.',
        initial=datetime.date.today)
    geometry = forms.CharField(
        widget=forms.HiddenInput(), required=False,
        help_text=(
            'Digitising an area of interest is not required but is recommended'
            '. You can use the help tab in the map area for more information '
            'on how to use the map. Draw an area of interest on the map to '
            'refine the set of search results to a specific area.'))

    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'KML/KMZ file less than 1MB.'))

    aoi_geometry = AOIGeometryField(
        label=u'Bounding Box/Circle',
        widget=forms.TextInput(attrs={'title': (
            'Upper left and lower right coordinates e.g. (20,-32,22,-34). Or '
            'circle center and radius e.g. (20,-32,100000).')
        }),
        required=False)

    k_orbit_path = IntegersCSVIntervalsField(
        label=u'Path (K/orbit)',
        required=False,
        help_text=(
            'e.g."10,20,30" or  "20-40"'))
    j_frame_row = IntegersCSVIntervalsField(
        label=u'Row (J/frame)',
        required=False,
        help_text=(
            'e.g. "10,20,30" or "20-40"'))

    cloud_max = forms.IntegerField(
        label=u'Cloud Max Percentage',
        min_value=0, max_value=100, initial=100,
        help_text=(
            'Range 0 - 100')
    )

    cloud_min = forms.IntegerField(
        label=u'Cloud Min Percentage',
        min_value=0, max_value=100, initial=0,
        help_text=(
            'Range 0 - 100'
        )
    )

    selected_sensors = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )

    free_imagery = forms.BooleanField(
        required=False, label="Free images only")
    panchromatic_imagery = forms.BooleanField(
        required=False, label="Panchromatic images only")

    class Meta:
        model = Search
        exclude = (
            'ip_position', 'guid', 'keywords', 'geometry_file', 'user',
            'deleted', 'processing_level')

    def __init__(self, *args, **kwargs):
        """
        SearchForm
        """
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)

        # calculate initial search_date (today - 1 month)
        # we use a constant -> 1 month = 31 days
        myPreviousMonthDate = (
            datetime.date.today() - datetime.timedelta(days=31))
        self.fields['start_datepicker'].initial = myPreviousMonthDate

    def clean_guid(self):
        """Custom validator for guid"""
        myCleanedData = self.cleaned_data
        myGuid = myCleanedData.get('guid')
        if not myGuid:
            myGuid = 'null'
            # we dont raise an error as we will just generate the guid in the
            # model's save method
        return myGuid

    def clean_ip_position(self):
        myCleanedData = self.cleaned_data
        myPoint = myCleanedData.get('ip_position')
        if not myPoint:
            myPoint = 'SRID=4326;POINT(0 0)'
        return myPoint

    def clean(self):
        myCleanedData = self.cleaned_data

        myStartSensorAngle = myCleanedData.get(
            'sensor_inclination_angle_start')
        myEndSensorAngle = myCleanedData.get(
            'sensor_inclination_angle_end')
        if ((myStartSensorAngle and myEndSensorAngle) and
                (myEndSensorAngle < myStartSensorAngle)):
            self._errors['sensor_inclination_angle_start'] = (
                self.error_class(['Check values.']))
            self._errors['sensor_inclination_angle_end'] = (
                self.error_class(['Check values.']))
            raise forms.ValidationError(
                'Error: Start sensor angle can not be greater than the end'
                ' sensor angle!')
        if myCleanedData.get('selected_sensors'):
            # we use the list unpack operatror to make a reverse zip
            mySatellites, myInstTypes = zip(
                *[[
                    int(b) for b in a.split('|')
                ] for a in myCleanedData.get('selected_sensors').split(',')])
            self.cleaned_data['satellite'] = mySatellites
            self.cleaned_data['instrumenttype'] = myInstTypes

        # check free_imagery
        if myCleanedData.get('free_imagery'):
            # HARD CODED value
            self.cleaned_data['license_type'] = [2]
        # check panchromatic_imagery
        if myCleanedData.get('panchromatic_imagery'):
            self.cleaned_data['spectral_group'] = [2]

        logger.debug('cleaned data: ' + str(self.cleaned_data))
        return self.cleaned_data
