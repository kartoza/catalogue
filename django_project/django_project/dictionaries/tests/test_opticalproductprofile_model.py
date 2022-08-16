"""
SANSA-EO Catalogue - Dictionaries OpticalProductProfile - basic CRUD
unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '23/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from ..models import (
    OpticalProductProfile, Collection, InstrumentType, Satellite,
    SpectralGroup, License
)

from .model_factories import (
    OpticalProductProfileF, SatelliteInstrumentF, SpectralModeF,
    InstrumentTypeF, ProcessingLevelF, SatelliteInstrumentGroupF, SatelliteF,
    CollectionF, SpectralGroupF, LicenseF
)


class TestOpticalProductProfileCRUD(TestCase):
    """
    Tests OpticalProductProfile model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_OpticalProductProfile_create(self):
        """
        Tests OpticalProductProfile model creation
        """
        myModel = OpticalProductProfileF.create()

        self.assertTrue(myModel.pk is not None)

    def test_OpticalProductProfile_delete(self):
        """
        Tests OpticalProductProfile model delete
        """
        myModel = OpticalProductProfileF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_OpticalProductProfile_read(self):
        """
        Tests OpticalProductProfile model read
        """

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode'
        })

        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'spectral_mode': mySpecMode
        })

        self.assertEqual(
            myModel.satellite_instrument.operator_abbreviation, 'SATIN 1')

        self.assertEqual(myModel.spectral_mode.name, 'Temp Spectral mode')

    def test_OpticalProductProfile_update(self):
        """
        Tests OpticalProductProfile model update
        """

        myModel = OpticalProductProfileF.create()

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })
        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode'
        })

        myModel.satellite_instrument = mySatInst
        myModel.spectral_mode = mySpecMode

        myModel.save()

        self.assertEqual(
            myModel.satellite_instrument.operator_abbreviation, 'SATIN 1')

        self.assertEqual(myModel.spectral_mode.name, 'Temp Spectral mode')

    def test_OpticalProductProfile_repr(self):
        """
        Tests OpticalProductProfile model repr
        """

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'spectral_mode': mySpecMode
        })

        self.assertEqual(
            str(myModel), 'SATIN 1 -- Temp Spectral mode - INSTYPE1')

    def test_OpticalProductProfile_baseProcessingLevel(self):
        """
        Tests OpticalProductProfile model baseProcessingLevel
        """

        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'BPL1',
            'name': 'BaseProcLevel 1'
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1',
            'base_processing_level': myProcLevel
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'instrument_type': myInstType
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'spectral_mode': mySpecMode
        })

        self.assertEqual(
            myModel.baseProcessingLevel(), myProcLevel)

    def test_OpticalProductProfile_bandCount(self):
        """
        Tests OpticalProductProfile model bandCount
        """

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1',
            'band_count': 10
        })

        mySatInstGroup = SatelliteInstrumentGroupF.create(**{
            'instrument_type': myInstType
        })

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1',
            'satellite_instrument_group': mySatInstGroup
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'spectral_mode': mySpecMode
        })

        self.assertEqual(myModel.bandCount(), 10)

    def test_OpticalProductProfile_QuerySet_for_license_type(self):
        """
        Tests OpticalProductProfile model QuerySet for_license_type
        """
        license_1 = LicenseF(**{
            'id': 1, 'type': 3, 'name': 'SANSA Commercial License',
            'details': 'SANSA Commercial License'
        })
        satellite_1 = SatelliteF(**{'id': 1, 'license_type': license_1})
        satelliteinstrumentgroup_1 = SatelliteInstrumentGroupF(**{
            'id': 1, 'satellite': satellite_1
        })
        satelliteinstrument_1 = SatelliteInstrumentF(**{
            'id': 1, 'satellite_instrument_group': satelliteinstrumentgroup_1
        })

        OpticalProductProfileF(**{
            'id': 1, 'satellite_instrument': satelliteinstrument_1
        })

        myLicense = License.objects.filter(pk=1)

        myResult = OpticalProductProfile.objects.for_licence_type(myLicense)

        self.assertEqual(myResult.count(), 1)

    def test_OpticalProductProfile_QuerySet_for_collection(self):
        """
        Tests OpticalProductProfile model QuerySet for_collection
        """
        collection_1 = CollectionF(**{'id': 1})
        satellite_1 = SatelliteF(**{'id': 1, 'collection': collection_1})
        satelliteinstrumentgroup_1 = SatelliteInstrumentGroupF(**{
            'id': 1, 'satellite': satellite_1
        })
        satelliteinstrument_1 = SatelliteInstrumentF(**{
            'id': 1, 'satellite_instrument_group': satelliteinstrumentgroup_1
        })

        OpticalProductProfileF(**{
            'id': 1, 'satellite_instrument': satelliteinstrument_1
        })

        myCollection = Collection.objects.filter(pk=1)

        myResult = OpticalProductProfile.objects.for_collection(myCollection)

        self.assertEqual(myResult.count(), 1)

    def test_OpticalProductProfile_QuerySet_for_instrumenttypes(self):
        """
        Tests OpticalProductProfile model QuerySet for_instrumenttypes
        """
        instrumenttype_1 = InstrumentTypeF(**{'id': 1})
        satelliteinstrumentgroup_1 = SatelliteInstrumentGroupF(**{
            'id': 1, 'instrument_type': instrumenttype_1
        })
        satelliteinstrument_1 = SatelliteInstrumentF(**{
            'id': 1, 'satellite_instrument_group': satelliteinstrumentgroup_1
        })

        OpticalProductProfileF(**{
            'id': 1, 'satellite_instrument': satelliteinstrument_1
        })

        myInsType = InstrumentType.objects.filter(pk=1)

        myResult = OpticalProductProfile.objects.for_instrumenttypes(myInsType)

        self.assertEqual(myResult.count(), 1)

    def test_OpticalProductProfile_QuerySet_for_satellite(self):
        """
        Tests OpticalProductProfile model QuerySet for_satellite
        """
        satellite_1 = SatelliteF(**{'id': 1})
        satelliteinstrumentgroup_1 = SatelliteInstrumentGroupF(**{
            'id': 1, 'satellite': satellite_1
        })
        satelliteinstrument_1 = SatelliteInstrumentF(**{
            'id': 1, 'satellite_instrument_group': satelliteinstrumentgroup_1
        })

        OpticalProductProfileF(**{
            'id': 1, 'satellite_instrument': satelliteinstrument_1
        })

        mySatellite = Satellite.objects.filter(pk=1)

        myResult = OpticalProductProfile.objects.for_satellite(mySatellite)

        self.assertEqual(myResult.count(), 1)

    def test_OpticalProductProfile_QuerySet_for_spectralgroup(self):
        """
        Tests OpticalProductProfile model QuerySet for_spectralgroup
        """
        spectralgroup_1 = SpectralGroupF(**{'id': 1})
        spectralmode_1 = SpectralModeF(**{
            'id': 1, 'spectralgroup': spectralgroup_1
        })

        OpticalProductProfileF(**{
            'id': 1, 'spectral_mode': spectralmode_1
        })

        mySpecGroup = SpectralGroup.objects.filter(pk=1)

        myResult = OpticalProductProfile.objects.for_spectralgroup(mySpecGroup)

        self.assertEqual(myResult.count(), 1)

    def test_OpticalProductProfile_QuerySet_only_searchable(self):
        """
        Tests OpticalProductProfile model QuerySet only_searchable
        """

        # is_searchable is by default True, so we can create a random OPP
        OpticalProductProfileF()

        # prepare a control object, which should not be included in results
        instrumenttype_1 = InstrumentTypeF(**{
            'id': 1,
            'is_searchable': False
        })

        satelliteinstrumentgroup_1 = SatelliteInstrumentGroupF(**{
            'id': 1, 'instrument_type': instrumenttype_1
        })
        satelliteinstrument_1 = SatelliteInstrumentF(**{
            'id': 1, 'satellite_instrument_group': satelliteinstrumentgroup_1
        })

        OpticalProductProfileF(**{
            'id': 2, 'satellite_instrument': satelliteinstrument_1
        })

        myResult = OpticalProductProfile.objects.only_searchable()

        self.assertEqual(myResult.count(), 1)
