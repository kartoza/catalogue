import logging
import datetime
import re

from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES

from catalogue.fields import *
from catalogue.models import *
from catalogue.datetimewidget import *
from catalogue.geometrywidget import *
from catalogue.sliderwidget import *
# Used for reading shapefiles etc
#from django.contrib.gis.gdal import DataSource
from catalogue.aoigeometry import AOIGeometryField

# Support dmy formats (see http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
        '%d-%m-%Y',                         # '25-10-2005'
        '%d/%m/%Y', '%d/%m/%y',             # '25/10/2006', '25/12/06'
        '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
        '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
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
            # Don't bother validating the formset unless each form is valid on its own
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
                raise forms.ValidationError, "Start date must be before or equal to end date."
        # Delete empty/deleted forms
        empty_forms.reverse()
        for i in empty_forms:
            del(self.forms[i])
        self.management_form.cleaned_data['TOTAL_FORMS']=len(self.forms)
        if not len(self.forms):
            raise forms.ValidationError, "At least one date range is required."
        #Next line disabled as it causes a crash
        #logging.debug('Date range forms:', self.forms)

    def is_valid(self):
        """
        Returns True if form.errors is empty for every form in self.forms.
        ABP: changed the range to len(self.forms)
        """
        if not self.is_bound:
            return False
        # We loop over every form.errors here rather than short circuiting on the
        # first failure to make sure validation gets triggered for every form.
        forms_valid = True
        err = self.errors
        for i in range(0, len(self.forms)):
            form = self.forms[i]
            if self.can_delete:
                if self._should_delete_form(form):
                    # This form is going to be deleted so any of its errors
                    # should not cause the entire formset to be invalid.
                    continue
            if bool(self.errors[i]):
                forms_valid = False
        return forms_valid and not bool(self.non_form_errors())

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors.
        ABP: changed the range to len(self.forms)
        """
        self._errors = []
        if not self.is_bound: # Stop further processing.
            return
        for i in range(0, len(self.forms)):
            form = self.forms[i]
            self._errors.append(form.errors)
        # Give self.clean() a chance to do cross-form validation.
        try:
            self.clean()
        except ValidationError, e:
            self._non_form_errors = self.error_class(e.messages)


class AdvancedSearchForm(forms.ModelForm):
    """ Let the user perform searches on sensors, by date and/or geometry digitised on map. """
    #keywords = forms.CharField(widget=forms.TextInput(attrs={'cols':'32'}),required=False)
    # Note1: the help_text strings are duplicated from the model help text
    #        since I didnt find a simple way to reuse it if adding custom fields
    # Note2: Only custom fields are added here. Fields that need no tweaking are
    #        pulled by the form generator directly from the model


    POLARISING_MODE_CHOICES = { '': 'All'}
    POLARISING_MODE_CHOICES.update(dict(RadarProduct.POLARISING_MODE_CHOICES))
    # ABP: the common part: will be searched on GenericProducts class only
    start_datepicker = forms.DateField(widget=DateTimeWidget(attrs={'title':"Choose the start date for this date range."}),required=False, label="Start date", input_formats=DATE_FORMATS,
        error_messages={'required': 'Entering a start date for your search is required.'},
        help_text='Start date is required. DD-MM-YYYY.')
    end_datepicker = forms.DateField(widget=DateTimeWidget,required=False, label="End date", input_formats=DATE_FORMATS,
        error_messages={'required': 'Entering an end date for your search is required.'},
        help_text='End date is required. DD-MM-YYYY.'
        )
    geometry = forms.CharField(widget=forms.HiddenInput(), required=False,
        help_text='Digitising an area of interest is not required but is recommended. You can use the help tab in the map area for more information on how to use the map. Draw an area of interest on the map to refine the set of search results to a specific area.')

    geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                    required=False,
                                    help_text = 'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If the shapefile contains\
                                                more than one polygon, only the first will be used. \
                                                Complex polygons will increase search time.')

    isAdvanced = forms.CharField(widget=forms.HiddenInput(), required=False)
    polarising_mode = forms.ChoiceField(choices=POLARISING_MODE_CHOICES, required=False)
    geometry = forms.CharField(widget=forms.HiddenInput(), required=False,
        help_text='Digitising an area of interest is not required but is recommended. You can use the help tab in the map area for more information on how to use the map. Draw an area of interest on the map to refine the set of search results to a specific area.')
    aoi_geometry = AOIGeometryField(widget=forms.TextInput(attrs={'title':"Enter bounding box coordinates separated by comma for West, South, East and North edges i.e. (20,-34,22,-32), or enter single coordinate which defines circle center and radius in kilometers (20,-32,100)"}),required=False)

    k_orbit_path = IntegersCSVIntervalsField(required=False, help_text='Insert the orbit path as a list of comma separated values or ranges (e.g. : "10,20,30" or  "20-40")')
    j_frame_row = IntegersCSVIntervalsField(required=False, help_text='Insert the frame row as a list of comma separated values or ranges (e.g. : "10,20,30" or "20-40")')
    # exclude PRODUCT_SEARCH_GENERIC from Search.PRODUCT_SEARCH_TYPES
    search_type = forms.ChoiceField(choices=Search.PRODUCT_SEARCH_TYPES[1:], required=False)
    cloud_mean = forms.IntegerField(min_value=0, max_value=100, initial=0,
        help_text='Select the maximum cloud cover (range 0-100) when searching \
        for images. Note that not all sensors support cloud cover filtering.')

    class Meta:
        model = Search
        exclude = ('ip_position' ,'guid' ,'keywords' ,'geometry_file' ,'user' ,'deleted', 'processing_level' )

    def __init__(self, *args, **kwargs):
        """We are using jquery tooltip to show a nice tooltip for each field. To
           ensure that each field has a title set (which is used for the tooltip text),
           this function iterates the fields of a form and sets their title text
           to the help text for that field. If the title is already set, its left as is."""

        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        for myFieldName, myField in self.fields.items():
            # Simple way to assign css class to every field
            myField.widget.attrs['class'] = 'ui-corner-all'
            if not myField.widget.attrs.has_key('title') or myField.widget.attrs['title'] == '':
                myField.widget.attrs['title'] = myField.help_text

        # Do not list empty dictionary items (avoid null searches)
        qs = AcquisitionMode.objects.order_by()
        self.fields['sensors'].queryset = MissionSensor.objects.filter(pk__in=qs.distinct().values_list('sensor_type__mission_sensor', flat=True))
        self.fields['mission'].queryset = Mission.objects.filter(pk__in=qs.distinct().values_list('sensor_type__mission_sensor__mission', flat=True))


    def clean_guid(self):
        """Custom validator for guid"""
        myCleanedData = self.cleaned_data
        myGuid = myCleanedData.get('guid')
        if not myGuid:
            myGuid='null'
            # we dont raise an error as we will just generate the guid in the model's save method
        return myGuid

    def clean_ip_position(self):
        myCleanedData = self.cleaned_data
        myPoint = myCleanedData.get('ip_position')
        if not myPoint:
            myPoint="SRID=4326;POINT(0 0)"
        return myPoint

    def clean_end_date(self):
        """End date validator"""
        #Note that required=False fields are not passed to cleaned_data but
        #rather just to self.data
        myData = self.data
        myEndDate = myData.get("end_date")
        if not myEndDate:
            # date is empty which is ok so do nothing
            pass
        else:
            try:
                myEndDate = datetime.datetime(*time.strptime(myEndDate, "%d-%m-%Y")[:6]).date()
            except:
                raise forms.ValidationError( "End date was not valid." )
            #pass
        return myEndDate

    def clean(self):
        myCleanedData = self.cleaned_data
        logging.info('cleaned data: ' + str(myCleanedData))

        # ABP: checks for advanced search only (not in cleaned_data because it does not belong to Search model)
        if self.data.get('isAdvanced') == 'true':
            # ABP: disabled because the DB has NULL in all rows
            #if not myCleanedData.get('geometric_accuracy_mean'):
                #self._errors["geometric_accuracy_mean"] = self.error_class(["Error: Spatial resolution is required for advanced search!"])
                #raise forms.ValidationError('Error: One or more required values are missing!')
            myStartSensorAngle = myCleanedData.get('sensor_inclination_angle_start')
            myEndSensorAngle = myCleanedData.get('sensor_inclination_angle_end')
            if (myStartSensorAngle and myEndSensorAngle) and (myEndSensorAngle < myStartSensorAngle):
                self._errors["sensor_inclination_angle_start"] = self.error_class(["Check values."])
                self._errors["sensor_inclination_angle_end"] = self.error_class(["Check values."])
                raise forms.ValidationError("Error: Start sensor angle can not be greater than the end sensor angle!")

            if int(myCleanedData.get('search_type')) in (Search.PRODUCT_SEARCH_OPTICAL, Search.PRODUCT_SEARCH_RADAR) and not myCleanedData.get('sensors'):
                self._errors["sensors"] = self.error_class(["Please select one or more sensors."])
                raise forms.ValidationError("Error: Sensors are mandatory for sensors-based products search!")

        return self.cleaned_data


class ProductIdSearchForm(forms.ModelForm):
    """
    Form for product id search refine
    """
    k_orbit_path = NoValidationChoiceField((), required=False)
    j_frame_row = NoValidationChoiceField((), required=False)
    date_range = NoValidationChoiceField((),required=False)
    isAdvanced = forms.CharField(widget=forms.HiddenInput(), required=False, initial=True)

    mission = AbbreviationModelChoiceField( None, empty_label="All" , required=False)
    sensors = AbbreviationModelChoiceField(None, empty_label="All", required=False)
    acquisition_mode = AbbreviationModelChoiceField(None, empty_label="All", required=False)
    sensor_type = AbbreviationModelChoiceField(None, empty_label="All", required=False)
    processing_level = AbbreviationModelChoiceField( None, empty_label="All" , required=False)

    class Meta:
        model = Search
        fields = ('acquisition_mode', 'sensors', 'sensor_type', 'mission', 'acquisition_mode', 'sensor_type', 'k_orbit_path', 'j_frame_row', 'processing_level')

    def __init__(self, *args, **kwargs):
        """
        Populate lists and set UI CSS class
        """

        # This form cannot create new objects, only edit existing instances
        assert 'instance' in kwargs

        super(ProductIdSearchForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            try:
                self.fields[myField].widget.attrs['class'] = 'ui-corner-all'
            except AttributeError:
                pass

        search_instance = self.instance

        #self.fields['sensors'].queryset = search_instance.sensors.all()
        #if search_instance.acquisition_mode:
            #self.fields['acquisition_mode'].queryset = AcquisitionMode.objects.filter(pk=search_instance.acquisition_mode.pk)
        #else:
            #self.fields['acquisition_mode'].queryset = AcquisitionMode.objects.filter(sensor_type__mission_sensor__in=search_instance.sensors.all())
        #if search_instance.sensor_type:
            #self.fields['sensor_type'].queryset = SensorType.objects.filter(pk=search_instance.sensor_type.pk)
        #else:
            #self.fields['sensor_type'].queryset = SensorType.objects.filter(mission_sensor__in=search_instance.sensors.all())
        #if search_instance.mission:
            #self.fields['mission'].queryset = Mission.objects.filter(pk=search_instance.mission.pk)
        #else:
            #self.fields['mission'].queryset = Mission.objects.filter(missionsensor__in=search_instance.sensors.all())
        #if search_instance.processing_level:
            #self.fields['processing_level'].queryset = search_instance.processing_level.all()
        #else:
            #self.fields['processing_level'].queryset = ProcessingLevel.objects.all()

        self.fields['acquisition_mode'].queryset = AcquisitionMode.objects.all()
        self.fields['sensor_type'].queryset = SensorType.objects.all()
        self.fields['mission'].queryset = Mission.objects.all()
        self.fields['processing_level'].queryset = ProcessingLevel.objects.all()
        self.fields['sensors'].queryset = MissionSensor.objects.all()

        choices = [('', 'All')]
        choices.extend([(i.local_format(), i.local_format()) for i in  search_instance.searchdaterange_set.all()])
        self.fields['date_range'].choices = choices

        row_choices = [('', 'All')]
        row_choices.extend([(l, l) for l in search_instance.getRowChoices()])
        path_choices = [('', 'All')]
        path_choices.extend([(l, l) for l in search_instance.getPathChoices()])

        self.fields['k_orbit_path'].choices = path_choices
        self.fields['j_frame_row'].choices = row_choices

    def clean_sensors(self):
        """
        Transform
        """
        data = self.cleaned_data['sensors']
        if not data:
            return MissionSensor.objects.all()
        else:
            return MissionSensor.objects.filter(pk=data.pk)

    def clean_date_range(self):
        """
        Transform
        """
        ranges = self.cleaned_data['date_range']
        if not ranges:
            return None

        try:
            start_date, end_date = SearchDateRange.from_local_format(ranges)
        except ValueError, e:
            raise forms.ValidationError ('Error: date is not valid. %s' % e)
        if not start_date <=  end_date:
            raise forms.ValidationError ('Error: date range is not valid.')
        return {'start_date' : start_date, 'end_date' : end_date }

    def clean_processing_level(self):
        """
        Transform
        """
        if not self.cleaned_data['processing_level']:
            return []
        return [self.cleaned_data['processing_level']]


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderStatus

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        #exclude = ('user','order_status')
        exclude = ('user','order_status','delivery_detail')

class DeliveryDetailForm(forms.ModelForm):
    ref_id = forms.CharField(widget=forms.HiddenInput(),required=False)
    aoi_geometry = AOIGeometryField(required=False,help_text='Enter bounding box coordinates separated by comma for West, South, East and North edges i.e. (20,-34,22,-32), or enter single coordinate which defines circle center and radius in kilometers (20,-32,100). Alternatively, digitise the clip area in the map.')
    geometry = forms.CharField(widget=forms.HiddenInput(),required=False)
    geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                    required=False,
                                    help_text = 'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If the shapefile contains more than one polygon, only the first will be used.')
    def __init__(self,theRecords,*args,**kwargs):
        super(DeliveryDetailForm, self).__init__(*args, **kwargs)
        #determine UTM zones for all products
        myProductZones = set()
        for record in theRecords:
            myProductZones=myProductZones.union(record.product.getUTMZones(theBuffer=1))

        myDefaultProjections=set((('4326','EPSG 4326'),('900913','EPSG 900913')))
        self.fields['projection'] =  forms.ModelChoiceField(queryset=Projection.objects.filter(epsg_code__in=[k for k,v in myProductZones | myDefaultProjections]).all(), empty_label=None)

    class Meta:
        model = DeliveryDetail
        exclude = ('user','processing_level',)

    def clean(self):
        myCleanedData = self.cleaned_data
        #if AOIgeometry is defined set it as default geometry
        if myCleanedData.get('aoi_geometry'):
            self.cleaned_data['geometry']=self.cleaned_data['aoi_geometry']

        return self.cleaned_data

class ProductDeliveryDetailForm(forms.ModelForm):
    ref_id = forms.CharField(widget=forms.HiddenInput(),required=False)

    def __init__(self,*args,**kwargs):
        super(ProductDeliveryDetailForm, self).__init__(*args, **kwargs)
        myPK = kwargs.get('prefix')
        myProduct = SearchRecord.objects.filter(pk__exact=myPK).get().product
        myDefaultProjections=set((('4326','EPSG 4326'),('900913','EPSG 900913')))
        self.fields['projection'] =  forms.ModelChoiceField(queryset=Projection.objects.filter(epsg_code__in=[k for k,v in myProduct.getUTMZones(theBuffer=0) | myDefaultProjections]).all(), empty_label=None)

    class Meta:
        model = DeliveryDetail
        exclude = ('user','geometry', 'processing_level')

class TaskingRequestDeliveryDetailForm(forms.ModelForm):
    ref_id = forms.CharField(widget=forms.HiddenInput(),required=False)
    geometry = forms.CharField(widget=forms.HiddenInput(),required=False)
    geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                    required=False,
                                    help_text = 'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If the shapefile contains more than one polygon, only the first will be used.')
    def __init__(self,*args,**kwargs):
        super(TaskingRequestDeliveryDetailForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DeliveryDetail
        exclude = ('user','processing_level','datum','file_format')

class TaskingRequestForm(forms.ModelForm):
    target_date = forms.DateField(widget=DateTimeWidget,required=True,input_formats=DATE_FORMATS,
        error_messages={'required': '''Entering a target date for your tasking request is required.'''},
        help_text='Tasking target date is required. DD-MM-YYYY.'
        )
    class Meta:
        model = TaskingRequest
        exclude = ('user','delivery_detail','order_status')

    def __init__(self, *args, **kwargs):
        super(TaskingRequestForm, self).__init__(*args, **kwargs)
        self.fields['mission_sensor'].queryset = MissionSensor.objects.filter(is_taskable=True)


class OrderStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderStatusHistory
        exclude = ('order','user','order_change_date', 'old_order_status' )


class ClipForm(forms.ModelForm):
    """ Allows the CSIR Partner user to clip one of the Extra Layers by a given geometry. """

    image = forms.ChoiceField(choices = [(0,"zaSpot2mMosaic2009"),
                                         (1,"zaSpot2mMosaic2008"),
                                         (2,"zaSpot2mMosaic2007")] )
    geometry = forms.CharField(widget=GeometryWidget,required=False,
        help_text='You can digitise your clip area directly, or alternatively use the file upload option below to upload the clip shapefile. You can use the help tab in the map area for more information on how to use the map. Draw an area of interest on the map to refine the set of search results to a specific area.')
    geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                    required=False,
                                    help_text = 'Upload a zipped shapefile of less than 1MB. If the shapefile contains\
                                                more than one polygon, only the first will be used. \
                                                The computation time is related to polygon complexity. \
                                                For multipart and non-polygon features the bounding box of the first feature will be used.')

    class Meta:
        model = Clip
        exclude = ('result_url','owner','guid', 'status' )
