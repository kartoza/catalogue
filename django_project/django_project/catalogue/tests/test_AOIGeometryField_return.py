"""
SANSA-EO Catalogue - AOIGeometryField_return - tests correct parsing of
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
__date__ = '31/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from django import forms

from catalogue.aoigeometry import AOIGeometryField


class AOIGeometryFieldForm(forms.Form):
    aoigeometryField = AOIGeometryField()


class TestAOIGeometryField(TestCase):
    """
    Tests AOIGeometryField output
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_formValidation_true(self):
        """
        Tests validation of AOIGeometryField input successes
        """
        myTestValues = [
            {'aoigeometryField': '20,-32,100'},
            {'aoigeometryField': '140,89,10'},
            {'aoigeometryField': '20,-32,22,-34'},
            {'aoigeometryField': '15,-80,35,-85'},
            {'aoigeometryField': '-120,40,120,30'}
        ]

        for myTestVal in myTestValues:
            myForm = AOIGeometryFieldForm(myTestVal)
            myRes = myForm.is_valid()
            myExpRes = True
            self.assertEqual(myRes, myExpRes)

    def test_formValidation_false(self):
        """
        Tests validation of AOIGeometryField input
        """
        myTestValues = [
            {'aoigeometryField': '500,-32,100'},
            {'aoigeometryField': '140,190,10'},
            {'aoigeometryField': '20,-34,22,-32'},
            {'aoigeometryField': '500,-80,35,-85'},
            {'aoigeometryField': '-120,190,120,30'}
        ]

        for myTestVal in myTestValues:
            myForm = AOIGeometryFieldForm(myTestVal)
            myRes = myForm.is_valid()
            myExpRes = False
            self.assertEqual(myRes, myExpRes)

    def test_AOIGeometry_value(self):
        """
        Tests AOIGeometryField return value
        """
        myTestValues = [
            {'aoigeometryField': '20,-32,1'},
            {'aoigeometryField': '140,89,1'},
            {'aoigeometryField': '20,-32,22,-34'},
            {'aoigeometryField': '15,-80,35,-85'},
            {'aoigeometryField': '-120,40,120,30'}
        ]

        myExpRes = [
            'SRID=4326;POLYGON ((20.0090090090090094 -32.0000000000000000, '
            '20.0088359034270553 -32.0017575704686124, 20.0083232390316326 '
            '-32.0034475984897782, 20.0074907172279524 -32.0050051372344129, '
            '20.0063703313620422 -32.0063703313620422, 20.0050051372344093 '
            '-32.0074907172279524, 20.0034475984897746 -32.0083232390316326, '
            '20.0017575704686124 -32.0088359034270553, 20.0000000000000000 '
            '-32.0090090090090058, 19.9982424295313876 -32.0088359034270553, '
            '19.9965524015102254 -32.0083232390316326, 19.9949948627655907 '
            '-32.0074907172279524, 19.9936296686379578 -32.0063703313620422, '
            '19.9925092827720476 -32.0050051372344129, 19.9916767609683674 '
            '-32.0034475984897782, 19.9911640965729447 -32.0017575704686124, '
            '19.9909909909909906 -32.0000000000000000, 19.9911640965729447 '
            '-31.9982424295313876, 19.9916767609683674 -31.9965524015102254, '
            '19.9925092827720476 -31.9949948627655907, 19.9936296686379578 '
            '-31.9936296686379578, 19.9949948627655907 -31.9925092827720476, '
            '19.9965524015102254 -31.9916767609683674, 19.9982424295313876 '
            '-31.9911640965729447, 20.0000000000000000 -31.9909909909909906, '
            '20.0017575704686124 -31.9911640965729447, 20.0034475984897746 '
            '-31.9916767609683674, 20.0050051372344093 -31.9925092827720476, '
            '20.0063703313620422 -31.9936296686379578, 20.0074907172279524 '
            '-31.9949948627655907, 20.0083232390316326 -31.9965524015102254, '
            '20.0088359034270553 -31.9982424295313876, 20.0090090090090094 '
            '-32.0000000000000000))',
            'SRID=4326;POLYGON ((140.0090090090090200 89.0000000000000000, '
            '140.0088359034270695 88.9982424295313876, 140.0083232390316255 '
            '88.9965524015102289, 140.0074907172279381 88.9949948627655942, '
            '140.0063703313620351 88.9936296686379649, 140.0050051372344058 '
            '88.9925092827720476, 140.0034475984897711 88.9916767609683603, '
            '140.0017575704686124 88.9911640965729447, 140.0000000000000000 '
            '88.9909909909909942, 139.9982424295313876 88.9911640965729447, '
            '139.9965524015102289 88.9916767609683603, 139.9949948627655942 '
            '88.9925092827720476, 139.9936296686379649 88.9936296686379649, '
            '139.9925092827720619 88.9949948627655942, 139.9916767609683745 '
            '88.9965524015102289, 139.9911640965729305 88.9982424295313876, '
            '139.9909909909909800 89.0000000000000000, 139.9911640965729305 '
            '89.0017575704686124, 139.9916767609683745 89.0034475984897711, '
            '139.9925092827720619 89.0050051372344058, 139.9936296686379649 '
            '89.0063703313620351, 139.9949948627655942 89.0074907172279524, '
            '139.9965524015102289 89.0083232390316397, 139.9982424295313876 '
            '89.0088359034270553, 140.0000000000000000 89.0090090090090058, '
            '140.0017575704686124 89.0088359034270553, 140.0034475984897711 '
            '89.0083232390316397, 140.0050051372344058 89.0074907172279524, '
            '140.0063703313620351 89.0063703313620351, 140.0074907172279381 '
            '89.0050051372344058, 140.0083232390316255 89.0034475984897711, '
            '140.0088359034270695 89.0017575704686124, 140.0090090090090200 '
            '89.0000000000000000))',
            'SRID=4326;POLYGON ((20.0000000000000000 -32.0000000000000000, '
            '20.0000000000000000 -34.0000000000000000, 22.0000000000000000 '
            '-34.0000000000000000, 22.0000000000000000 -32.0000000000000000, '
            '20.0000000000000000 -32.0000000000000000))',
            'SRID=4326;POLYGON ((15.0000000000000000 -80.0000000000000000, '
            '15.0000000000000000 -85.0000000000000000, 35.0000000000000000 '
            '-85.0000000000000000, 35.0000000000000000 -80.0000000000000000, '
            '15.0000000000000000 -80.0000000000000000))',
            'SRID=4326;POLYGON ((-120.0000000000000000 40.0000000000000000, '
            '-120.0000000000000000 30.0000000000000000, 120.0000000000000000 '
            '30.0000000000000000, 120.0000000000000000 40.0000000000000000, '
            '-120.0000000000000000 40.0000000000000000))']

        for idx, myTestVal in enumerate(myTestValues):
            myForm = AOIGeometryFieldForm(myTestVal)
            myValidForm = myForm.is_valid()  # validate form
            myRes = myForm.cleaned_data.get('aoigeometryField')
            self.assertEqual(myRes, myExpRes[idx])
