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
    order_status = tables.Column()
    user = tables.Column()
    view = tables.URLColumn(
        empty_values=(),
        orderable=False,
        verbose_name='View Order'
    )

    def render_view(self, record):
        """
        We need to add HTML for a link to view the details of each Order
        object

        :param record: The Order object rendered in this row
        """
        return mark_safe(
            '<a href="/vieworder/%s/"><i class="icon-search"></i></a>'
            % record.id
        )