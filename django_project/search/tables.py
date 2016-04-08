# coding=utf-8
"""
${NAME}
"""
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import django_tables2 as tables
from reports.tables import SANSADateColumn, render_user_names

__author__ = 'george'


# noinspection PyMethodMayBeStatic
class SearchesTable(tables.Table):
    """
    Renders a table of Search objects
    """
    searched_by = tables.Column(empty_values=(), orderable=False)
    search_date = SANSADateColumn()
    satellites = tables.Column(empty_values=(), orderable=False)
    sensors = tables.Column(empty_values=(), orderable=False)
    date_ranges = tables.Column(empty_values=(), orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)

    def render_searched_by(self, record):
        """
        We need to render the User's first and last names

        :param record: The SearchRecord being rendered
        :return: User's first_name and last_name
        :rtype: str
        """
        return render_user_names(record)

    def render_satellites(self, record):
        """
        Render a list of instrument types used in the search

        :param record: The SearchRecord object being rendered
        :return: satellite_string
        :rtype: str
        """
        satellites = record.satellites_as_list()
        if len(satellites) > 0:
            satellite_string = ', '.join(satellites)
        else:
            satellite_string = None
        return satellite_string

    def render_sensors(self, record):
        """
        Render a list of instrument types used in the search

        :param record: The SearchRecord object being rendered
        :return: sensor_string
        :rtype: str
        """
        sensors = record.sensors_as_list()
        if len(sensors) > 0:
            sensor_string = ', '.join(sensors)
        else:
            sensor_string = None
        return sensor_string

    def render_date_ranges(self, record):
        """
        We need to render record.dates_as_string in date_ranges column
        :param record: The SearchRecord object rendered in this row
        """
        return record.dates_as_string

    def render_actions(self, record):
        """
        Render the appropriate links for each record's action cell

        :param record: The object being rendered in this row
        :return: unescaped HTML :rtype: str
        """
        return mark_safe(
            '<a href="%(guid_url)s" class="view-btn">'
            '<i class="icon-search"></i></a> '
            '<a href="%(delete_url)s" '
            'onclick="%(delete_url)s?xhr\');'
            '$(this).parent().parent().remove();return false;\' '
            'class="remove-btn"><i class="icon-remove"></i></a>' % {
                'guid_url': reverse('searchGuid', args={record.guid}),
                'delete_url': reverse('deleteSearch', args={record.id})
            }
        )