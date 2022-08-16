"""
SANSA-EO Catalogue - Custom form fields

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

###############################################################################
#
# Custom fields
#
###############################################################################
import re
from django import forms


def validateIntegerRange(theValue):
    if not theValue[1] > theValue[0]:
        raise forms.ValidationError(
            'First value in range (%d) must be lower then second (%d)'
            % theValue)


class IntegersCSVIntervalsField(forms.RegexField):
    """
    Accepts ranges: 1-2 3-55, comma separated values and single values
    """
    # The RE used to extract numbers and ranges
    regex = '[1-9]\d*[-][1-9]\d*|[1-9]\d*'

    def __init__(self, *args, **kwargs):
        return super(
            IntegersCSVIntervalsField, self).__init__(
                regex=IntegersCSVIntervalsField.regex, *args, **kwargs)

    @staticmethod
    def to_tuple(value):
        """
        Normalize data to a list of integer single values and tuples for ranges
        """
        # Return an empty list if no input was given.
        values = []
        if value:
            for token in re.findall(IntegersCSVIntervalsField.regex, value):
                values.append(tuple(map(int, token.split('-'))))
        return values

    def validate(self, values):
        """
        Checks the intervals
        """
        # Use the parent's handling of required fields, etc.
        super(IntegersCSVIntervalsField, self).validate(values)
        for value in IntegersCSVIntervalsField.to_tuple(values):
            if len(value) == 2:
                validateIntegerRange(value)


class NoValidationChoiceField(forms.ChoiceField):
    """
    Same as ChoiceField, accepts any choice
    """
    def valid_value(self, value):
        "Skip validation"
        return True


class AbbreviationModelChoiceField(forms.ModelChoiceField):
    """
    Custom model choice field that shows abbreviated name rather than the
    default unicode representation so that we can show compact combo boxes.
    The associated model must have a field called abbreviation.
    """
    def label_from_instance(self, obj):
        return obj.abbreviation


class AbbreviationModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom model choice field that shows abbreviated name rather than the
    default unicode representation so that we can show compact combo boxes.
    The associated model must have a field called abbreviation.
    """
    def label_from_instance(self, obj):
        return obj.abbreviation
