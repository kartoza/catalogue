"""
SANSA-EO Catalogue - others_metadata - Others views
    unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.2'
__date__ = '07/08/2013'
__copyright__ = 'South African National Space Agency'

from datetime import datetime
import difflib

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


from core.model_factories import UserF
from dictionaries.tests.model_factories import (
    ProcessingLevelF, SatelliteInstrumentF, InstrumentTypeF, SpectralModeF,
    OpticalProductProfileF, SatelliteF, SatelliteInstrumentGroupF
)
from .model_factories import (
    OpticalProductF, InstitutionF, ProjectionF, QualityF, LicenseF,
    CreatingSoftwareF
)


class OthersViews_metadata(TestCase):
    """
    Tests others.py metadata method/view
    """

    def setUp(self):
        """
        Set up before each test
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

    def test_metadata_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'metadata',
                kwargs=myKwargTest)

    def test_metadata_nologin_badproductid(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'metadata',
                kwargs={'theId': '1'}))
        self.assertEqual(myResp.status_code, 404)

    def test_metadata_nologin(self):
        """
        Test view if user is not logged in
        """
        myInstitution = InstitutionF.create(**{
            u'address1': u'Hartebeeshoek', u'address2': u'Gauteng',
            u'address3': u'South Africa', u'name': u'SANSA',
            u'post_code': u'0000'
        })

        myProjection = ProjectionF.create(**{
            u'name': u'UTM37S', u'epsg_code': 32737
        })

        myProcessingLevel = ProcessingLevelF.create(**{
            u'abbreviation': u'L1A',
            u'name': 'L1A Proc level'
        })

        myLicense = LicenseF.create(**{
            'name': 'SAC License'
        })
        mySatellite = SatelliteF.create(**{
            'license_type': myLicense
        })

        mySatInsGroup = SatelliteInstrumentGroupF.create(**{
            'satellite': mySatellite
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInsGroup
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myOPP = OpticalProductProfileF.create(**{
            u'spectral_mode': mySpecMode, u'satellite_instrument': mySatInst
        })

        myQuality = QualityF.create(**{'name': 'SuperQuality'})
        myCreatingSoftware = CreatingSoftwareF.create(**{
            'name': 'FreeSoftware'
        })

        OpticalProductF.create(**{
            'id': 1,
            'unique_product_id': '123 Product ID 123',
            'original_product_id': '123 Product ID 123',
            'creating_software': myCreatingSoftware,
            'owner': myInstitution,
            'projection': myProjection,
            'processing_level': myProcessingLevel,
            'product_profile': myOPP,
            'quality': myQuality,
            'license': myLicense,
            'product_acquisition_start': datetime(2012, 12, 12, 12, 00),
            'product_acquisition_end': datetime(2012, 12, 12, 14, 00),
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        })

        myClient = Client()
        myResp = myClient.get(reverse('metadata', kwargs={'theId': '1'}))

        self.assertEqual(myResp.status_code, 200)
        expString = open(
            'catalogue/tests/others_metadata_output.txt', 'rb+').read()

        self.assertEqual(
            ''.join(difflib.unified_diff(
                myResp.content, expString, lineterm='')),
            '')
        # check used templates
        myExpTemplates = [
            'productTypes/opticalProduct.html',
            u'productTypes/genericSensorProduct.html',
            u'productTypes/genericImageryProduct.html',
            u'productTypes/genericProduct.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_metadata_userlogin(self):
        """
        Test view if user is logged as user
        """

        myInstitution = InstitutionF.create(**{
            u'address1': u'Hartebeeshoek', u'address2': u'Gauteng',
            u'address3': u'South Africa', u'name': u'SANSA',
            u'post_code': u'0000'
        })

        myProjection = ProjectionF.create(**{
            u'name': u'UTM37S', u'epsg_code': 32737
        })

        myProcessingLevel = ProcessingLevelF.create(**{
            u'abbreviation': u'L1A',
            u'name': 'L1A Proc level'
        })

        myLicense = LicenseF.create(**{
            'name': 'SAC License'
        })
        mySatellite = SatelliteF.create(**{
            'license_type': myLicense
        })

        mySatInsGroup = SatelliteInstrumentGroupF.create(**{
            'satellite': mySatellite
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInsGroup
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myOPP = OpticalProductProfileF.create(**{
            u'spectral_mode': mySpecMode, u'satellite_instrument': mySatInst
        })

        myQuality = QualityF.create(**{'name': 'SuperQuality'})
        myCreatingSoftware = CreatingSoftwareF.create(**{
            'name': 'FreeSoftware'
        })

        OpticalProductF.create(**{
            'id': 1,
            'unique_product_id': '123 Product ID 123',
            'original_product_id': '123 Product ID 123',
            'creating_software': myCreatingSoftware,
            'owner': myInstitution,
            'projection': myProjection,
            'processing_level': myProcessingLevel,
            'product_profile': myOPP,
            'quality': myQuality,
            'license': myLicense,
            'product_acquisition_start': datetime(2012, 12, 12, 12, 00),
            'product_acquisition_end': datetime(2012, 12, 12, 14, 00),
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'metadata',
                kwargs={'theId': '1'}))
        self.assertEqual(myResp.status_code, 200)

        expString = open(
            'catalogue/tests/others_metadata_output.txt', 'rb+').read()

        self.assertEqual(
            ''.join(difflib.unified_diff(
                myResp.content, expString, lineterm='')),
            '')
        # check used templates
        myExpTemplates = [
            'productTypes/opticalProduct.html',
            u'productTypes/genericSensorProduct.html',
            u'productTypes/genericImageryProduct.html',
            u'productTypes/genericProduct.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
