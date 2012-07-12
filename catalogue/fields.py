###############################################################################
#
# Custom fields
#
###############################################################################
import re
from django import forms

class IntegersCSVIntervalsField(forms.RegexField):
    """
    Accepts ranges: 1-2 3-55, comma separated values and single values
    """
    # The RE used to extract numbers and ranges
    regex='[1-9]\d*[-][1-9]\d*|[1-9]\d*'

    def __init__(self, *args, **kwargs):
        return super(IntegersCSVIntervalsField, self).__init__(regex=IntegersCSVIntervalsField.regex, *args, **kwargs)

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
                if not value[1] > value[0]:
                    raise forms.ValidationError, 'The range values are not correct: %d %d' % value


class NoValidationChoiceField(forms.ChoiceField):
    """
    Same as ChoiceField, accepts any choice
    """
    def valid_value(self, value):
        "Skip validation"
        return True

class AbbreviationModelChoiceField(forms.ModelChoiceField):
    """Custom model choice field that shows abbreviated name rather than the default unicode representation
    so that we can show compact combo boxes. The associated model must have a field called abbreviation."""
    def label_from_instance(self, obj):
        return obj.abbreviation


class AbbreviationModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Custom model choice field that shows abbreviated name rather than the default unicode representation
    so that we can show compact combo boxes. The associated model must have a field called abbreviation."""
    def label_from_instance(self, obj):
        return obj.abbreviation
