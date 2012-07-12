"""
SANSA-EO Catalogue - integerCVSIntervalsField_return - tests correct parsing of
    user input

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '12/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue.fields import IntegersCSVIntervalsField
from django import forms


class IntegersCSVIntervalsForm(forms.Form):
    integerfield = IntegersCSVIntervalsField()


class IntegersCSVIntervalsField_Test(TestCase):
    """
    Tests IntegersCVSIntervalsField output
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_singleValueInput(self):
        """
        Tests parsing of single input value
        """
        myTestValues = ('12', '-123', 'blah')
        myExpResults = ([(12,)], [(123,)], [])

        for idx, testVal in enumerate(myTestValues):
            myField = IntegersCSVIntervalsField()
            myResult = myField.to_tuple(testVal)
            self.assertEqual(myResult, myExpResults[idx],
                simpleMessage(myResult, myExpResults[idx]))

    def test_rangeValueInput(self):
        """
        Tests parsing of ranged input values
        """
        myTestValues = ('42-52', '34- -123', '34--123')
        myExpResults = ([(42, 52)], [(34,), (123,)], [(34,), (123,)])

        for idx, testVal in enumerate(myTestValues):
            myField = IntegersCSVIntervalsField()
            myResult = myField.to_tuple(testVal)
            self.assertEqual(myResult, myExpResults[idx],
                simpleMessage(myResult, myExpResults[idx]))

    def test_mixedValueInput(self):
        """
        Tests parsing of mixed/multiple input values
        """
        myTestValues = ('45-52, 12, 65-98',)
        myExpResults = ([(45, 52), (12,), (65, 98)],)

        for idx, testVal in enumerate(myTestValues):
            myField = IntegersCSVIntervalsField()
            myResult = myField.to_tuple(testVal)
            self.assertEqual(myResult, myExpResults[idx],
                simpleMessage(myResult, myExpResults[idx]))

    def test_formValidation_true(self):
        """
        Tests validation of IntegersCSVIntervalsField input successes
        """
        #test searches pk
        myTestValues = [{'integerfield': '1-2'}, {'integerfield': '1,2,4-10'},
        {'integerfield': '1-5, 0, 6-10'}]

        for myTestVal in myTestValues:
            myForm = IntegersCSVIntervalsForm(myTestVal)

            myRes = myForm.is_valid()
            myExpRes = True
            self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes))

    def test_formValidation_false(self):
        """
        Tests validation of IntegersCSVIntervalsField input
        """
        #test searches pk
        myTestValues = [{'integerfield': '10-4'}, {'integerfield': '99-0'}]

        for myTestVal in myTestValues:
            myForm = IntegersCSVIntervalsForm(myTestVal)

            myRes = myForm.is_valid()
            myExpRes = False
            self.assertEqual(myRes, myExpRes, simpleMessage(myRes, myExpRes))
