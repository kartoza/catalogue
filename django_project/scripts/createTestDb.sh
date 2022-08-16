#!/bin/bash
source ../python/bin/activate
python manage.py testserver \
  catalogue/fixtures/test_user.json\
  catalogue/fixtures/test_missiongroup.json\
  catalogue/fixtures/test_mission.json\
  catalogue/fixtures/test_missionsensor.json\
  catalogue/fixtures/test_search.json\
  catalogue/fixtures/test_searchdaterange.json\
  catalogue/fixtures/test_processinglevel.json\
  catalogue/fixtures/test_sensortype.json\
  catalogue/fixtures/test_acquisitionmode.json\
  catalogue/fixtures/test_institution.json\
  catalogue/fixtures/test_license.json\
  catalogue/fixtures/test_projection\
  catalogue/fixtures/test_quality\
  catalogue/fixtures/test_order.json\
  catalogue/fixtures/test_searchrecord.json\
  catalogue/fixtures/test_sacuserprofile.json\
  catalogue/fixtures/test_orderstatus.json\
  catalogue/fixtures/test_creatingsoftware\
  catalogue/fixtures/test_genericproduct.json\
  catalogue/fixtures/test_genericimageryproduct.json\
  catalogue/fixtures/test_genericsensorproduct.json\
  catalogue/fixtures/test_opticalproduct.json\
  catalogue/fixtures/test_radarproduct.json\
  catalogue/fixtures/test_datum.json\
  catalogue/fixtures/test_marketsector.json\
  catalogue/fixtures/test_deliverymethod.json\
  catalogue/fixtures/test_fileformat.json\
  catalogue/fixtures/test_resamplingmethod.json\
  catalogue/fixtures/test_taskingrequest.json\
  catalogue/fixtures/test_ordernotificationrecipients.json
  
  #catalogue/fixtures/test_contenttypes.json\


dropdb 'sac-testbed'
psql -c 'alter database "sac-unittest" rename to "sac-testbed"' template1
deactivate
