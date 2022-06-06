"""
SANSA-EO Catalogue - Database helper functions

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
__date__ = '21/03/2013'
__copyright__ = 'South African National Space Agency'


from django.db import connection


def executeRAWSQL(theSQL, theParams={}, theDictOutput=True):
    """
    Executes rawSQL query which does not require Object mapping

    params:
        theSQL - actual SQL query
        theParams - optional query parameters
        theDictOutput - map column names to values in a dictionary
    """

    cursor = connection.cursor()
    cursor.execute(theSQL, theParams)

    if theDictOutput:
        return dictfetchall(theCursor=cursor)
    else:
        return cursor.fetchall()


def dictfetchall(theCursor):
    """
    Returns all rows from a cursor as a dict
    """
    desc = theCursor.description
    return [
        dict(list(zip([col[0] for col in desc], row)))
        for row in theCursor.fetchall()
    ]
