from catalogue.tests import simple_tests, dims_lib_test, \
    misr_command_test, dims_command_test, rapideye_command_test, \
    terrasar_command_test, os4eo_command_test, modis_command_test, os4eo_client_test

#import unittest classes
from catalogue.tests.test_spot_ingestor import SpotIngestorTest
from catalogue.tests.simpleTest import SimpleTest
from catalogue.tests.license_model import LicenseCRUD_Test
from catalogue.tests.missionGroup_model import MissionGroupCRUD_Test
from catalogue.tests.mission_model import MissionCRUD_Test
from catalogue.tests.missionsensor_model import MissionSensorCRUD_Test
from catalogue.tests.sensortype_model import SensorTypeCRUD_Test
from catalogue.tests.acquisitionMode_model import AcquisitionModeCRUD_Test
from catalogue.tests.processingLevel_model import ProcessingLevelCRUD_Test
from catalogue.tests.projection_model import ProjectionCRUD_Test
from catalogue.tests.institution_model import InstitutionCRUD_Test
from catalogue.tests.quality_model import QualityCRUD_Test
from catalogue.tests.creatingSoftware_model import CreatingSoftwareCRUD_Test
from catalogue.tests.topic_model import TopicCRUD_Test
from catalogue.tests.placeType_model import PlaceTypeCRUD_Test
from catalogue.tests.place_model import PlaceCRUD_Test
from catalogue.tests.unit_model import UnitCRUD_Test
from catalogue.tests.products_model_helpermethods import Product_HelperMethods_Test
from catalogue.tests.genericproduct_model import GenericProductCRUD_Test
from catalogue.tests.genericimageryproduct_model import GenericImageryProductCRUD_Test
from catalogue.tests.genericsensorproduct_model import GenericSensorProductCRUD_Test
from catalogue.tests.opticalproduct_model import OpticalProductCRUD_Test
from catalogue.tests.radarproduct_model import RadarProductCRUD_Test
from catalogue.tests.geospatialproduct_model import GeospatialProductCRUD_Test
from catalogue.tests.ordinalproduct_model import OrdinalProductCRUD_Test
from catalogue.tests.continuousproduct_model import ContinuousProductCRUD_Test
from catalogue.tests.datum_model import DatumCRUD_Test
from catalogue.tests.resamplingmethod_model import ResamplingMethodCRUD_Test
from catalogue.tests.fileformat_model import FileFormatCRUD_Test
from catalogue.tests.orderstatus_model import OrderStatusCRUD_Test
from catalogue.tests.deliverymethod_model import DeliveryMethodCRUD_Test
from catalogue.tests.deliverydetail_model import DeliveryDetailCRUD_Test
from catalogue.tests.marketsector_model import MarketSectorCRUD_Test
from catalogue.tests.order_model import OrderCRUD_Test
from catalogue.tests.orderstatushistory_model import OrderStatusHistoryCRUD_Test
from catalogue.tests.taskingrequest_model import TaskingRequestCRUD_Test
from catalogue.tests.featurereaders_return import FeatureReaders_Test
from catalogue.tests.email_notification_test import EmailNotificationTest, EmailTest
from catalogue.tests.integerCSVIntervalsField_return import IntegersCSVIntervalsField_Test
from catalogue.tests.AOIGeometryField_return import AOIGeometryField_Test
from catalogue.tests.visit_model import VisitCRUD_Test
from catalogue.tests.allusersmessage_model import AllUsersMesageCRUD_Test
from catalogue.tests.ordernotificationrecipients_model import OrderNotificationRecipientsCRUD_Test
from catalogue.tests.utmzonecalc_module import utmZoneFromLatLon_Test
from catalogue.tests.rangetag_templatetag import RangeTag_Test
from catalogue.tests.graphtag_templatetag import gPieChart_Test
from catalogue.tests.boxtag_templatetag import BoxTag_Test
from catalogue.tests.messaging_tests import MessagingTests
from catalogue.tests.view_helper_tests import ViewHelperTests
from catalogue.tests.tasking_view_viewTaskingRequest import TaskingViews_viewTaskingRequest_Tests
from catalogue.tests.tasking_view_myTaskingRequests import TaskingViews_myTaskingRequests_Tests
from catalogue.tests.tasking_view_listTaskingRequests import TaskingViews_listTaskingRequests_Tests
from catalogue.tests.tasking_view_downloadTaskingRequest import TaskingViews_downloadTaskingRequest_Tests
from catalogue.tests.tasking_view_addTaskingRequest import TaskingViews_addTaskingRequest_Tests
from catalogue.tests.shopping_cart_view_downloadCart import ShoppingCart_downloadCart_Tests
from catalogue.tests.shopping_cart_view_downloadCartMetadata import ShoppingCart_downloadCartMetadata_Tests
from catalogue.tests.shopping_cart_view_addToCart import ShoppingCart_addToCart_Tests
from catalogue.tests.shopping_cart_view_removeFromCart import ShoppingCart_removeFromCart_Tests
from catalogue.tests.shopping_cart_view_showCartContents import ShoppingCart_showCartContents_Tests
from catalogue.tests.shopping_cart_view_showMiniCartContents import ShoppingCart_showMiniCartContents_Tests
from catalogue.tests.orders_view_myOrders import OrdersViews_myOrders_Tests
from catalogue.tests.orders_view_listOrders import OrdersViews_listOrders_Tests
from catalogue.tests.orders_view_orderMonthlyReport import OrdersViews_orderMonthlyReport_Tests
from catalogue.tests.orders_view_downloadOrder import OrdersViews_downloadOrder_Tests
from catalogue.tests.orders_view_downloadClipGeometry import  OrdersViews_downloadClipGeometry_Tests
from catalogue.tests.orders_view_downloadOrderMetadata import OrdersViews_downloadOrderMetadata_Tests
from catalogue.tests.orders_view_viewOrder import OrdersViews_viewOrder_Tests
from catalogue.tests.orders_view_updateOrderHistory import OrdersViews_updateOrderHistory_Tests
from catalogue.tests.orders_view_createDeliveryDetailForm import OrdersViews_createDeliveryDetailForm_Tests
from catalogue.tests.orders_view_showDeliveryDetail import OrdersViews_showDeliveryDetail_Tests
from catalogue.tests.orders_view_ordersSummary import OrdersViews_ordersSummary_Tests
from catalogue.tests.orders_view_addOrder import OrdersViews_addOrder_Tests
from catalogue.tests.reports_visitorReport import ReportsViews_visitorReport_Tests
from catalogue.tests.reports_visitorMonthlyReport import ReportsViews_visitorMonthlyReport_Tests
from catalogue.tests.reports_visitorList import ReportsViews_visitorList_Tests
from catalogue.tests.reports_searchHistory import ReportsViews_searchHistory_Tests
from catalogue.tests.reports_recentSearches import ReportsViews_recentSearches_Tests
from catalogue.tests.reports_searchMonthlyReport import ReportsViews_searchMonthlyReport_Tests
from catalogue.tests.reports_searchMonthlyReportAOI import ReportsViews_searchMonthlyReportAOI_Tests
from catalogue.tests.reports_dataSummaryTable import ReportsViews_dataSummaryTable_Tests
from catalogue.tests.reports_sensorSummaryTable import ReportsViews_sensorSummaryTable_Tests
from catalogue.tests.reports_dictionaryReport import ReportsViews_dictionaryReport_Tests
from catalogue.tests.others_showProduct import OthersViews_showProduct_Tests
from catalogue.tests.others_visitorMap import OthersViews_visitorMap_Tests
from catalogue.tests.others_showPreview import OthersViews_showPreview_Tests
from catalogue.tests.others_showThumbPage import OthersViews_showThumbPage_Tests

# selenium tests
from catalogue.tests.selenium_login_test import SeleniumLogin
from catalogue.tests.selenium_login_test import SeleniumSearch

#this is only required for doctests
__test__ = {
  #'simple_tests' : simple_tests,
  #'dims_lib_test' : dims_lib_test,
  #'dims_command_test': dims_command_test,
  #'rapideye_command_test': rapideye_command_test,
  #'modis_command_test': modis_command_test,
  #'os4eo_client_test': os4eo_client_test,
  #'os4eo_command_test': os4eo_command_test,
  #'misr_command_test': misr_command_test,
  #'terrasar_command_test': terrasar_command_test,
  }