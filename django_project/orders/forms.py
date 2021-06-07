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

from dictionaries.models import SubsidyType
from django.contrib.auth.models import User
from django import forms

from orders.models import (
    Order,
    OrderStatusHistory,
    NonSearchRecord,
    OrderStatus,
    MarketSector,
    Datum,
    DeliveryMethod,
    FileFormat
)

logger = logging.getLogger(__name__)


class OrderStatusForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = OrderStatus


class OrderForm(forms.ModelForm):
    market_sector = forms.ModelChoiceField(
        queryset=MarketSector.objects.order_by('name'),
        label='Market sector'
    )
    subsidy_type_assigned = forms.ModelChoiceField(
        queryset=SubsidyType.objects.order_by('name'),
        empty_label=None
    )

    subsidy_type_requested = forms.ModelChoiceField(
        queryset=SubsidyType.objects.order_by('name'),
        empty_label=None
    )
    datum = forms.ModelChoiceField(
        queryset=Datum.objects.order_by('name'),
        empty_label=None
    )
    file_format = forms.ModelChoiceField(
        queryset=FileFormat.objects.order_by('name'),
        empty_label=None
    )
    delivery_method = forms.ModelChoiceField(
        queryset=DeliveryMethod.objects.order_by('name'),
        empty_label=None,
        to_field_name='name',
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by('username'),
        # label='User'
        empty_label='Select user'
    )

    class Meta:
        model = Order
        exclude = ('order_status',)
        fields = (
            'datum',
            'market_sector',
            'subsidy_type_assigned',
            'subsidy_type_requested',
            'user',
            'file_format',
            'delivery_method',
            'notes'
        )


class OrderFormNonSearchRecords(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('order_status', 'file_format', 'datum', 'resampling_method', 'delivery_method')

    def __init__(self, *args, **kwargs):
        super(OrderFormNonSearchRecords, self).__init__(*args, **kwargs)
        self.fields['subsidy_type_assigned'].empty_label = "--- Please select ---"
        self.fields['subsidy_type_requested'].empty_label = "--- Please select ---"
        users = User.objects.all()
        User._meta.ordering = ['first_name', 'last_name', 'username']
        self.fields['user'].choices = [
            (user.pk, (user.username if user.get_full_name() == "" else user.get_full_name())) for user in users]


class OrderStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderStatusHistory
        exclude = ('order', 'user', 'order_change_date', 'old_order_status')


class NonSearchRecordForm(forms.ModelForm):
    class Meta:
        model = NonSearchRecord
        exclude = ('download_path',)
