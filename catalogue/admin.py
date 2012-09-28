"""
SANSA-EO Catalogue - Catalogue admin interface

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

from django.contrib.gis import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from offline_messages.models import OfflineMessage

from catalogue.models import (
    OrderNotificationRecipients,
    Mission,
    MissionSensor,
    SensorType,
    Search,
    DeliveryMethod,
    AcquisitionMode,
    TaskingRequest,
    OrderStatus,
    FileFormat,
    ResamplingMethod,
    ProcessingLevel,
    Datum,
    Institution,
    License,
    Projection,
    Quality,
    CreatingSoftware,
    GenericProduct,
    OpticalProduct,
    GeospatialProduct,
    Visit,
    SacUserProfile)


#
# Search and visitors admin
#
class SearchAdmin(admin.GeoModelAdmin):
    list_display = ('search_date', 'user', 'guid', 'search_date')
    list_filter = ('search_date', 'user', )


class VisitAdmin(admin.GeoModelAdmin):
    pass


class SacUserProfileAdmin (admin.GeoModelAdmin):
    list_display = ('user', 'strategic_partner')
    list_filter = ('user', 'strategic_partner')


class OrderStatusAdmin(admin.GeoModelAdmin):
    pass


class OrderNotificationRecipientsAdminForm(forms.ModelForm):
    class Meta:
        model = OrderNotificationRecipients

    def clean(self):
        """
        Validates that at least one of the m2m has values
        """
        if (not self.cleaned_data['classes'] and
                not self.cleaned_data['sensors']):
            raise ValidationError(
                u'Classes and sensors cannot be simultaneously blank')
        return self.cleaned_data


class OrderNotificationRecipientsAdmin(admin.GeoModelAdmin):
    list_display = ('user',)
    form = OrderNotificationRecipientsAdminForm

    # This next method will filter the users list in the admin form
    # so that only staff members can be chosen from the users list
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['user'].queryset = (
            User.objects.filter(is_staff=True))
        return (
            super(OrderNotificationRecipientsAdmin, self)
            .render_change_form(request, context, args, kwargs))

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filters abstract product classes
        """
        if db_field.name == 'classes':
            form_field = (
                super(OrderNotificationRecipientsAdmin, self)
                .formfield_for_manytomany(db_field, request, **kwargs))
            form_field.choices = [
                c for c in form_field.choices
                if getattr(
                    ContentType.objects.get(
                        pk=c[0]).model_class(), 'concrete', False)]
            return form_field
        return (
            super(OrderNotificationRecipientsAdmin, self)
            .formfield_for_manytomany(db_field, request, **kwargs))

#################################################
# Admin models for new generic product model
#################################################


class ProcessingLevelAdmin(admin.GeoModelAdmin):
    pass


class DatumAdmin(admin.GeoModelAdmin):
    pass


class InstitutionAdmin(admin.GeoModelAdmin):
    pass


class LicenseAdmin(admin.GeoModelAdmin):
    pass


class ProjectionAdmin(admin.GeoModelAdmin):
    pass


class QualityAdmin(admin.GeoModelAdmin):
    pass


class CreatingSoftwareAdmin(admin.GeoModelAdmin):
    pass


class GenericProductAdmin(admin.GeoModelAdmin):
    pass


class GeospatialProductAdmin(admin.GeoModelAdmin):
    pass


class OpticalProductAdmin(admin.GeoModelAdmin):
    list_filter = ('acquisition_mode',)


class ResamplingMethodAdmin(admin.GeoModelAdmin):
    pass


class FileFormatAdmin(admin.GeoModelAdmin):
    pass


class DeliveryMethodAdmin(admin.GeoModelAdmin):
    pass


class OrderStatusAdmin(admin.GeoModelAdmin):
    pass


class MissionAdmin(admin.GeoModelAdmin):
    pass


class MissionSensorAdmin(admin.GeoModelAdmin):
    pass


class TaskingRequestAdmin(admin.GeoModelAdmin):
    pass


class SensorTypeAdmin(admin.GeoModelAdmin):
    pass


class AcquisitionModeAdmin(admin.GeoModelAdmin):
    pass


class OfflineMessageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OfflineMessage._meta.fields]

admin.site.register(Mission, MissionAdmin)
admin.site.register(MissionSensor, MissionSensorAdmin)
admin.site.register(SensorType, SensorTypeAdmin)
admin.site.register(AcquisitionMode, AcquisitionModeAdmin)
admin.site.register(TaskingRequest, TaskingRequestAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(FileFormat, FileFormatAdmin)
admin.site.register(ResamplingMethod, ResamplingMethodAdmin)
admin.site.register(ProcessingLevel, ProcessingLevelAdmin)
admin.site.register(Datum, DatumAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Projection, ProjectionAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(CreatingSoftware, CreatingSoftwareAdmin)
admin.site.register(GenericProduct, GenericProductAdmin)
admin.site.register(OpticalProduct, OpticalProductAdmin)
admin.site.register(GeospatialProduct, GeospatialProductAdmin)
admin.site.register(
    OrderNotificationRecipients, OrderNotificationRecipientsAdmin)

#################################################
# End of admin models for new generic product model
#################################################

admin.site.register(Search, SearchAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(SacUserProfile, SacUserProfileAdmin)
admin.site.register(OfflineMessage, OfflineMessageAdmin)
