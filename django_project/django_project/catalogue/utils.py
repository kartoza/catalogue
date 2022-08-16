# coding=utf-8
"""
SANSA-EO Catalogue - Uncategorized models

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""
__author__ = 'george@linfiniti.com'
__version__ = '0.1'
__date__ = '09/08/2012'
__copyright__ = 'South African National Space Agency'


from django.conf import settings


def validate_params(sort_col, sort_order,
                    default_column, default_sort,
                    acceptable_columns=None,
                    acceptable_sorts=None):

    """
    This method validates sort_col and sort_order in order to avoid
    SQL injection attacks

    Django's raw sql execution params option is only an option to replace
    SQL variables, not column names, so we have to use a standard str
    replace, which is insecure. We therefore validate that sort_col and
    sort_order are one of our predefined options only.

    :param default_sort: The sort order to which valid_sort_order defaults
    :param default_column: The column name to which valid_sort_col defaults
    :param acceptable_sorts: Optional list of acceptable sorting options.
        Defaults to settings.ACCEPTABLE_SORTS
    :param acceptable_columns: Optional list of acceptable sort column
        names. Defaults to settings.ACCEPTABLE_COLUMNS
    :param sort_col: 'country' or 'count'
    :param sort_order: 'ASC' or 'DESC'
    :return: valid_sort_col and valid_sort_order :rtype: str
    """
    valid_sort_order = default_sort
    valid_sort_col = default_column
    if not acceptable_columns:
        acceptable_columns = settings.ACCEPTABLE_COLUMNS
    if not acceptable_sorts:
        acceptable_sorts = settings.ACCEPTABLE_SORTS
    if sort_col in acceptable_columns:
        valid_sort_col = sort_col
    if sort_order in acceptable_sorts:
        valid_sort_order = sort_order
    return valid_sort_col, valid_sort_order
