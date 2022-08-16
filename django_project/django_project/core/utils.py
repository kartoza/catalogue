"""
SANSA-EO Catalogue - Generic helper utils

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
__date__ = '16/07/2013'
__copyright__ = 'South African National Space Agency'


def pad(theString, theLength):
    myLength = len(theString)
    myString = theString + "-" * (theLength - myLength)
    return myString


def zeroPad(theString, theLength):
    myLength = len(theString)
    myString = "0" * (theLength - myLength) + theString
    return myString
