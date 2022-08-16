# coding=utf-8
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


from .models import (
    OrderNotificationRecipients,
    DeliveryMethod,
    OrderStatus,
    FileFormat,
    ResamplingMethod,
    Datum
)


class OrderStatusAdmin(admin.GeoModelAdmin):
    """Admin model for order status."""
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
admin.site.register(OrderStatus, OrderStatusAdmin)


class OrderNotificationRecipientsAdminForm(forms.ModelForm):
    """Admin form for order notification recipients."""
    class Meta:
        """Meta class implementation."""
        model = OrderNotificationRecipients
        fields = '__all__'

    def clean(self):
        """
        Validates that at least one of the m2m has values
        """
        if (not self.cleaned_data['classes'] and
                not self.cleaned_data['satellites']):
            raise ValidationError(
                'Classes and sensors cannot be simultaneously blank')
        return self.cleaned_data


class OrderNotificationRecipientsAdmin(admin.GeoModelAdmin):
    """Admin for order notification recipients."""
    search_fields = [
        'user_username',
        'satellite_instrument_group__satellite__name']
    list_filter = ['user', 'satellite_instrument_group']
    list_display = ('user',)

    form = OrderNotificationRecipientsAdminForm

    def render_change_form(self, request, context, *args, **kwargs):
        """This next method will filter the users list in the admin form.

        :param request:
        :param context:
        :param args:
        :param kwargs:
        So that only staff members can be chosen from the users list."""
        context['adminform'].form.fields['user'].queryset = (
            User.objects.filter(is_staff=True))
        return (
            super(OrderNotificationRecipientsAdmin, self)
            .render_change_form(request, context, args, kwargs))

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filters abstract product classes
        :param db_field:
        :param request:
        :param kwargs:
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
admin.site.register(
    OrderNotificationRecipients, OrderNotificationRecipientsAdmin)


class DatumAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
admin.site.register(Datum, DatumAdmin)


class ResamplingMethodAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
admin.site.register(ResamplingMethod, ResamplingMethodAdmin)


class FileFormatAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
admin.site.register(FileFormat, FileFormatAdmin)


class DeliveryMethodAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
