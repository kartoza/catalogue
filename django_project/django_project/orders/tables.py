# coding=utf-8
"""
${NAME}
"""
from django.utils.safestring import mark_safe
import django_tables2 as tables
from reports.tables import SANSADateColumn

__author__ = 'george'


class OrderListTable(tables.Table):
    """
    Renders an Orders table
    """
    id = tables.Column()
    order_date = SANSADateColumn()
    user = tables.Column()
    last_status_changed = tables.Column(accessor='get_recent_history_date',
                                        orderable=False,)
    day_in_process = tables.Column(accessor='day_in_process',
                                   orderable=False,
                                   )
    order_status__name = tables.Column(
        verbose_name='Status'
    )

    view = tables.URLColumn(
        empty_values=(),
        orderable=False,
        verbose_name='View Details'
    )

    def render_view(self, record):
        """
        We need to add HTML for a link to view the details of each Order
        object

        :param record: The Order object rendered in this row
        """
        return mark_safe(
            '<a href="/order/%s/"><button class="btn btn-sm btn-primary">View Details</button></i></a>'
            % record.id
        )
