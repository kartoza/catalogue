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
import time

from django import forms
from django.forms.models import BaseInlineFormSet
#from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
#from django.core.validators import EMPTY_VALUES
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import (
    Tab,
    TabHolder,
)
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Button,
    Div,
    HTML,
    Field
)
from crispy_forms.bootstrap import (
    FormActions
)

from catalogue.fields import IntegersCSVIntervalsField
from catalogue.datetimewidget import DateTimeWidget
from catalogue.aoigeometry import AOIGeometryField


from .models import Search
from .utils import prepareSelectQuerysets


# Support dmy formats (see
#    http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
    '%d-%m-%Y',               # '25-10-2005'
    '%d/%m/%Y', '%d/%m/%y',   # '25/10/2006', '25/12/06'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)


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
            'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If '
            'the shapefile contains more than one polygon, only the first will'
            ' be used. Complex polygons will increase search time.'))

    aoi_geometry = AOIGeometryField(
        label=u'Bounding Box/Circle',
        widget=forms.TextInput(attrs={'title': (
            'Enter bounding box coordinates separated by comma for Upper '
            'left and Lower right coordinates i.e. (20,-32,22,-34), or '
            'enter single coordinate which defines circle center and '
            'radius in kilometers (20,-32,100). Alternatively, digitise '
            'the clip area in the map.')
        }),
        required=False)

    k_orbit_path = IntegersCSVIntervalsField(
        label=u'Path (K/orbit)',
        required=False,
        help_text=(
            'Insert the orbit path as a list of comma separated values or '
            'ranges (e.g. : "10,20,30" or  "20-40")'))
    j_frame_row = IntegersCSVIntervalsField(
        label=u'Row (J/frame)',
        required=False,
        help_text=(
            'Insert the frame row as a list of comma separated values or '
            'ranges (e.g. : "10,20,30" or "20-40")'))

    cloud_mean = forms.IntegerField(
        label=u'Cloud Percentage',
        min_value=0, max_value=100, initial=100,
        help_text=(
            'Select the maximum cloud cover (range 0-100) when searching for '
            'images. Note that not all sensors support cloud cover filtering.')
    )

    class Meta:
        model = Search
        exclude = (
            'ip_position', 'guid', 'keywords', 'geometry_file', 'user',
            'deleted', 'processing_level')

    # add Media class for this form, rendered specific for this form
    class Media:
        js = (
            "/static/js/date_utils.js",
            "/static/js/widget.sansa-datepicker.js",
            "/staic/js/widget.sansa-daterangecontainer.js",)

    def __init__(self, *args, **kwargs):
        """
        We are using jquery tooltip to show a nice tooltip for each field. To
        ensure that each field has a title set (which is used for the tooltip
        text), this function iterates the fields of a form and sets their
        title text to the help text for that field. If the title is already
        set, its left as is.
        """

        self.helper = FormHelper()
        self.helper.form_class = 'span12 '
        self.helper.form_id = 'search_form'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.form_action = reverse('search', kwargs={})

        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Satellite',
                    HTML(
                        '<div id="reset_dict_selections" '
                        'class="btn btn-info btn-small">Reset selection</div>'
                    ),
                    Field('collection', template='myField.html'),
                    Field('satellite', template='myField.html'),
                    Field('instrumenttype', template='myField.html'),
                    Field('spectral_group', template='myField.html'),
                    Field('license_type', template='myField.html'),
                    css_id="collapseSensors",  # rename this class
                    css_class="in",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Cloud Cover',
                    Field('cloud_mean', template='myField.html'),
                    css_id="collapseCloudCover",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Path & Row',
                    Field('k_orbit_path', template='myField.html'),
                    Field('j_frame_row', template='myField.html'),
                    css_id="collapseRP",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Area of Interest',
                    Field('aoi_geometry', template='myField.html'),
                    Field('geometry_file', template='myField.html'),
                    css_id="collapseGeometry",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'Dates',
                    HTML(
                        '<div><div class="control-group error">{% for error i'
                        'n myFormset.non_form_errors %}<p id="error_date" cla'
                        'ss="help-block"><strong>{{ error }}</strong></p>{% e'
                        'ndfor %}</div></div>'),
                    Field('start_datepicker', template='myField.html'),
                    Field('end_datepicker', template='myField.html'),
                    HTML(
                        '<div class="btn-group" style="margin-left: 50px;">'
                        '<a class="btn btn-info btn-small" id="dr_add" title'
                        '="Select the dates in the calend'
                        'ar and click here to add to the list." href="javascri'
                        'pt:void(0)"><i class="icon-arrow-down"></i></a>'),
                    HTML(
                        '<a class="btn btn-info btn-small" id="dr_del" title'
                        '="Select the ranges in the list '
                        'and click here to remove." href="javascript:void(0)">'
                        '<i class="icon-arrow-up"></i></a>'
                        '</div>'),
                    HTML(
                        '<label for="id_searchdaterange_set">Date range *</lab'
                        'el>'),
                    HTML('{{ myFormset.management_form }}'),
                    Div(
                        HTML(
                            '{% for form in myFormset.forms %}<div class="dr_r'
                            'ow"><div class="dr_input">{{ form }}</div><div cl'
                            'ass="dr_text" title="Click to select."></div></di'
                            'v>{% endfor %}'),
                        id="dr_container",
                        css_class="well well-small"
                    ),
                    css_id="collapseDates",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                Fieldset(
                    'More options...',
                    Field(
                        'sensor_inclination_angle_start',
                        template='myField.html'),
                    Field(
                        'sensor_inclination_angle_end',
                        template='myField.html'),
                    Field('spatial_resolution', template='myField.html'),
                    Field('band_count', template='myField.html'),
                    css_id="collapseImage",
                    data_parent="#accordion-search2",
                    template="crispy-fieldset-accordion.html"
                ),
                css_id="accordion-search2",
                template="crispy-div-accordion.html"
            ),
            'geometry'
        )

        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None:
            myCollectionSet = self.instance.collection.all().values_list('id')
            mySatelliteSet = self.instance.satellite.all().values_list('id')
            myInstTypeSet = self.instance.instrumenttype.all()\
                .values_list('id')
            mySpecGroupSet = self.instance.spectral_group.all()\
                .values_list('id')
            myLicenseTypeSet = self.instance.license_type.all()\
                .values_list('id')

            myQS_data = prepareSelectQuerysets(
                myCollectionSet, mySatelliteSet, myInstTypeSet,
                mySpecGroupSet, myLicenseTypeSet
            )
        else:
            myQS_data = prepareSelectQuerysets()

        # set new querysets
        self.fields['collection'].queryset = myQS_data[0]
        self.fields['satellite'].queryset = myQS_data[1]
        self.fields['instrumenttype'].queryset = myQS_data[2]
        self.fields['spectral_group'].queryset = myQS_data[3]
        self.fields['license_type'].queryset = myQS_data[4]

        for myFieldName, myField in self.fields.items():
            myField.widget.attrs['class'] = 'ui-corner-all'
            if (not 'title' in myField.widget.attrs or
                    myField.widget.attrs['title'] == ''):
                myField.widget.attrs['title'] = myField.help_text

        # calculate initial search_date (today - 1 month)
        # we use a constant -> 1 month = 31 days
        myPrevoiusMonthDate = (
            datetime.date.today() - datetime.timedelta(days=31))
        self.fields['start_datepicker'].initial = myPrevoiusMonthDate

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
        logger.debug('cleaned data: ' + str(myCleanedData))

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

        return self.cleaned_data
