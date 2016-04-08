# coding=utf-8
"""
SANSA-EO Catalogue - Report application tables and table-helpers

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import django_tables2 as tables

from catalogue.models import Visit


__author__ = 'george@grvhi.com'
__version__ = '0.1'
__date__ = '17/08/2012'
__copyright__ = 'South African National Space Agency'


def table_sort_settings(request):
    """
    Helper function to fetch sort and order from GET and set the consequent
    value for sort_link which is appended to the table sort links in the
    template

    :param request: HttpRequest
    :return: sort_col, sort_order, sort_link :rtype: str
    """
    sort_col = request.GET.get('sort', None)
    sort_order = request.GET.get('order', None)
    if sort_order == 'ASC':
        sort_link = 'DESC'
    elif sort_order == 'DESC':
        sort_link = 'ASC'
    else:
        sort_link = 'DESC'
    return sort_col, sort_order, sort_link


def render_user_names(record):
    """
    A helper function to return a string to represent a User in our tables

    :param record: The record which has a User FK relationship
    :return: user's name representation :rtype: str
    """
    if record.user:
        if record.user.first_name:
            return '%s %s' % (
                record.user.first_name,
                record.user.last_name or None
            )
        else:
            return record.user.username
    else:
        return 'No User Recorded'


class TitleColumn(tables.Column):
    """
    Returns a column with a titled cell value
    (i.e. "South Africa", not "south africa")
    """
    def render(self, value):
        """
        Renders the cell's value
        :param value: cell value
        :return: value.title() :rtype: str
        """
        return value.title()


class SANSADateColumn(tables.DateColumn):
    """
    A subsclass of tables.DateColumn to render a date Column in a consistent
    format
    """
    def render(self, value, **kwargs):
        """
        Render's the cell's value in the defined date format
        """
        return value.strftime('%a %d %b %Y')


class CountryTable(tables.Table):
    """
    Renders a Country/Count table
    """
    country = TitleColumn()
    count = tables.Column()


class SatelliteInstrumentTable(tables.Table):
    """
    Renders a SatelliteInstrumentTable
    """
    sensor = tables.Column(
        accessor='satellite.name',
        verbose_name='Satellite'
    )
    instrument_type = tables.Column(
        accessor='instrument_type.name',
        verbose_name='Sensor'
    )
    abbreviation = tables.Column(accessor='satellite.abbreviation')

    count = tables.Column(
        accessor='id__count',
        verbose_name='Scene Count'
    )

    start_date = tables.Column(accessor='min_year', orderable=False)
    end_date = tables.Column(accessor='max_year', orderable=False)

    info = tables.Column(empty_values=(), orderable=False)

    # noinspection PyMethodMayBeStatic
    def render_info(self, record):
        """
        Render the row's Info column with a link to the Sensor's Summary Fact
            Sheet
        :param record: The record being rendered in this row
        """
        return mark_safe(
            '<a href="%s"><i class="icon-question-sign"></i></a>' % reverse(
                'fact-sheet',
                kwargs={'sat_abbr': record.satellite.operator_abbreviation,
                        'instrument_type': record.instrument_type.operator_abbreviation}
            )
        )



class VisitorTable(tables.Table):
    """
    A table to render a list of Visitors
    """
    user = tables.Column(empty_values=())
    visit_date = SANSADateColumn(verbose_name='Visit Date')

    # noinspection PyMethodMayBeStatic
    def render_user(self, record):
        """
        Render the user's name representation

        :param record: The record being rendered in this row
        :return: User's name representation :rtype: str
        """
        return render_user_names(record)

    class Meta(object):
        """
        Adding CSS classes to the table (required for Bootstrap) and setting
        other Meta attributes
        """
        model = Visit
        exclude = ('ip_position', 'id')
        sequence = (
            'user', 'ip_address', 'country', 'city', 'visit_date'
        )
