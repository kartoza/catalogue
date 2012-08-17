BEGIN;
delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in  (select genericimageryproduct_ptr_id from catalogue_genericsensorproduct where acquisition_mode_id = 1);
delete from catalogue_genericsensorproduct where acquisition_mode_id = 1;
delete from catalogue_acquisitionmode where id = 1;
delete from catalogue_sensortype where id = 1;
delete from catalogue_ordernotificationrecipients_sensors where missionsensor_id in (select mission_id from catalogue_missionsensor where id = 1);
delete from catalogue_search_sensors where missionsensor_id in (select mission_id from catalogue_missionsensor where id = 1);
delete from catalogue_missionsensor where id = 1;
COMMIT;
