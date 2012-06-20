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
from featurereaders_return import FeatureReaders_Test
from searcher_object import SearcherObject_Test
from search_bandcount import SearchBandCount_Test
from search_inclinationangle import SearchIncliantionAngle_Test
from search_geometricaccuracy import SearchGeometricAccuracy_Test
from search_cloudcover import SearchCloudCover_Test
from email_notification_test import EmailNotificationTest

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
