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
from featurereaders_return import FeatureReaders_Test
from searcher_object import BandCountSearches_Test

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
