import simple_tests #doctest based tests
import dims_lib_test
import dims_command_test
import rapideye_command_test
import modis_command_test
import os4eo_client_test
import os4eo_command_test
import misr_command_test
import terrasar_command_test

#import unittest classes
from simpleTest import SimpleTest
from license_model import LicenseCRUD_Test
from missionGroup_model import MissionGroupCRUD_Test
from mission_model import MissionCRUD_Test
from missionsensor_model import MissionSensorCRUD_Test
from sensortype_model import SensorTypeCRUD_Test
from acquisitionMode_model import AcquisitionModeCRUD_Test
from processingLevel_model import ProcessingLevelCRUD_Test
from projection_model import ProjectionCRUD_Test
from institution_model import InstitutionCRUD_Test
from quality_model import QualityCRUD_Test
from creatingSoftware_model import CreatingSoftwareCRUD_Test
from topic_model import TopicCRUD_Test
from placeType_model import PlaceTypeCRUD_Test
from place_model import PlaceCRUD_Test
from unit_model import UnitCRUD_Test
from genericproduct_model import GenericProductCRUD_Test
from genericimageryproduct_model import GenericImageryProductCRUD_Test
from genericsensorproduct_model import GenericSensorProductCRUD_Test
from opticalproduct_model import OpticalProductCRUD_Test
from radarproduct_model import RadarProductCRUD_Test
from geospatialproduct_model import GeospatialProductCRUD_Test
from ordinalproduct_model import OrdinalProductCRUD_Test
from continuousproduct_model import ContinuousProductCRUD_Test
from searchrecord_model import SearchRecordCRUD_Test
from featurereaders_return import FeatureReaders_Test
from searcher_object import SearcherObject_Test
from search_bandcount import SearchBandCount_Test
from search_inclinationangle import SearchIncliantionAngle_Test
from search_spatialresolution import SearchSpatialResolution_Test
from search_cloudcover import SearchCloudCover_Test
from search_rowpath import SearchRowPath_Test
from email_notification_test import EmailNotificationTest
from integerCSVIntervalsField_return import IntegersCSVIntervalsField_Test

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
