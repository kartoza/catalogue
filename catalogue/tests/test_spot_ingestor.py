"""
SANSA-EO Catalogue - searcher_object - tests for email functions

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
__date__ = '12/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from django.core.management import call_command
from catalogue.models import Institution
from catalogue.models import GenericProduct
from catalogue.ingestors import spot

class SpotIngestorTest(TestCase):
    """
    Tests Email Notifications (see catalogue.views.helpers)
    """

    fixtures = [
        'test_user.json',
        'test_missiongroup.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_institution.json',
        'test_license.json',
        'test_projection',
        'test_quality',
        'test_orderstatus.json',
        'test_order.json',
        'test_searchrecord.json',
        'test_sacuserprofile.json',
        'test_orderstatus.json',
        'test_marketsector.json',
        'test_creatingsoftware',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json',
        'test_datum.json',
        'test_deliverymethod.json',
        'test_fileformat.json',
        'test_resamplingmethod.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def testImportUsingManagementCommand(self):
        """Test that we can ingest spot using the management command"""
        myOwner = Institution.objects.get(id=3)
        myShapeName = ('/home/web/sac/sac_catalogue/catalogue/tests/'
                      'sample_files/spot-ingestion/Africa_2012_subset.shp')
        call_command('spot_harvest',
                                verbosity=2,
                                shapefile=myShapeName)
        myProduct = GenericProduct.objects.get(
            product_id=('S5-_HRG_T--_S5C2_0100_00_0368_00'
                                '_120510_090310_1B--_ORBIT-'))
        assert myProduct.owner == myOwner


        call_command('spot_harvest',
                     verbosity=2,
                     shapefile=myShapeName,
                     owner='Foobar')
        myProduct = GenericProduct.objects.get(
            product_id=('S5-_HRG_T--_S5C2_0100_00_0368_00'
                        '_120510_090310_1B--_ORBIT-'))
        assert myProduct.owner.name == 'Foobar'

    def testImportDirectly(self):
        """Test that we can ingest spot using the ingestor function"""
        myOwner = Institution.objects.get(id=3)
        myShapeName = ('/home/web/sac/sac_catalogue/catalogue/tests/'
                      'sample_files/spot-ingestion/Africa_2012_subset.shp')
        spot.ingest(shapefile=myShapeName)
        myProduct = GenericProduct.objects.get(
            product_id=('S5-_HRG_T--_S5C2_0100_00_0368_00'
                                '_120510_090310_1B--_ORBIT-'))
        assert myProduct.owner == myOwner
        spot.ingest(shapefile=myShapeName,
                    owner='Foobar')
        myProduct = GenericProduct.objects.get(
            product_id=('S5-_HRG_T--_S5C2_0100_00_0368_00'
                        '_120510_090310_1B--_ORBIT-'))
        assert myProduct.owner.name == 'Foobar'


if __name__ == '__main__':
    unittest.main()
