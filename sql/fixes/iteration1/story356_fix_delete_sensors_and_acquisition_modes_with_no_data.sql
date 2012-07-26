BEGIN;
-- Delete any acquisition mode that has no data associated with it
-- first any date ranges
delete from catalogue_searchdaterange where search_id in(select id from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where id not in (select acquisition_mode_id as id from catalogue_genericsensorproduct group by acquisition_mode_id order by acquisition_mode_id)));
-- then any search sensors
delete from catalogue_search_sensors where search_id in(select id from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where id not in (select acquisition_mode_id as id from catalogue_genericsensorproduct group by acquisition_mode_id order by acquisition_mode_id)));
-- then delete searches
delete from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where id not in (select acquisition_mode_id as id from catalogue_genericsensorproduct group by acquisition_mode_id order by acquisition_mode_id));
--  then delete the 49 unrefrences acquistion modes
delete from catalogue_acquisitionmode where id in ( select id from catalogue_acquisitionmode where id not in (select acquisition_mode_id as id from catalogue_genericsensorproduct group by acquisition_mode_id order by acquisition_mode_id) order by id);

-- Delete any sensortype that has no acquisiton mode related to
delete from catalogue_searchdaterange where search_id in (select id from catalogue_search where sensor_type_id not in (select sensor_type_id from catalogue_acquisitionmode));
delete from catalogue_search_sensors where search_id in (select id from catalogue_search where sensor_type_id not in (select sensor_type_id from catalogue_acquisitionmode));
delete from catalogue_search where sensor_type_id not in (select sensor_type_id from catalogue_acquisitionmode);
delete from catalogue_sensortype where id not in (select sensor_type_id from catalogue_acquisitionmode);
COMMIT;
