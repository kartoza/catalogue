
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

from django.db import models
from django.contrib.gis import admin
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from offline_messages.models import OfflineMessage

from catalogue.models import (
    GenericProduct,
    OpticalProduct,
    GeospatialProduct,
    Visit,
    AllUsersMessage
)


#
# Visitors admin
#


class VisitAdmin(admin.GeoModelAdmin):
    """Admin model for visitors."""
    search_fields = ['city', 'country', 'user__username']
    list_filter = ['city', 'country', 'user']
    list_display = ('visit_date', 'city', 'country', 'user')


#################################################
# Admin models for new generic product model
#################################################


class GenericProductAdmin(admin.GeoModelAdmin):
    search_fields = ['original_product_id', 'unique_product_id']
    list_filter = ['product_date', ]
    list_display = ('original_product_id', 'unique_product_id')


class GeospatialProductAdmin(admin.GeoModelAdmin):
    search_fields = ['original_product_id', 'unique_product_id']
    list_filter = ['product_date', ]
    list_display = ('original_product_id', 'unique_product_id')


class OpticalProductAdmin(admin.GeoModelAdmin):
    search_fields = ['original_product_id', 'unique_product_id']
    list_filter = ['product_date', ]
    list_display = ('original_product_id', 'unique_product_id')


class OfflineMessageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OfflineMessage._meta.fields]
    ordering = ('message',)
    exclude = ('level',)
    field_options = {
        'fields': ('message', 'user',),
    }
    formfield_overrides = {
        models.CharField: {'widget': widgets.AdminTextareaWidget},
    }
    list_filter = ('user', 'created')

    # This next method will filter the users list in the admin form
    # so that only staff members can be chosen from the users list
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['user'].queryset = (
            User.objects.order_by('username'))
        return (
            super(OfflineMessageAdmin, self)
            .render_change_form(request, context, args, kwargs))


class AllUsersMessageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AllUsersMessage._meta.fields]
    ordering = ('created', 'message')

admin.site.register(GenericProduct, GenericProductAdmin)
admin.site.register(OpticalProduct, OpticalProductAdmin)
admin.site.register(GeospatialProduct, GeospatialProductAdmin)

#################################################
# End of admin models for new generic product model
#################################################

admin.site.register(Visit, VisitAdmin)
# Error : The model OfflineMessage is already registered
# admin.site.register(OfflineMessage, OfflineMessageAdmin)
admin.site.register(AllUsersMessage, AllUsersMessageAdmin)
