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
logger = logging.getLogger(__name__)

from django import forms

from .models import (
    OrderStatus,
    Order,
    OrderStatusHistory,
    NonSearchRecord
)


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderStatus


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('order_status',)


class OrderFormNonSearchRecords(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('order_status', 'file_format', 'datum', 'resampling_method', 'delivery_method')


class OrderStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderStatusHistory
        exclude = ('order', 'user', 'order_change_date', 'old_order_status')


class NonSearchRecordForm(forms.ModelForm):
    class Meta:
        model = NonSearchRecord
        exclude = ('download_path',)
