BEGIN;
-- 434375 records - keep ids of products to be deleted in a temp table
select genericimageryproduct_ptr_id as id into tmp from catalogue_genericsensorproduct where acquisition_mode_id in (
select id from catalogue_acquisitionmode where sensor_type_id  in ( select id from catalogue_sensortype where mission_sensor_id = 6));
delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from tmp);
delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from tmp);
delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from tmp);
delete from catalogue_searchrecord where product_id in (select id from tmp);
delete from catalogue_genericproduct where id in (select id from tmp);
delete from catalogue_acquisitionmode where sensor_type_id  in ( select id from catalogue_sensortype where mission_sensor_id = 6));
delete from catalogue_sensortype where mission_sensor_id = 6;
delete from catalogue_missionsensor where id = 6;
drop table tmp;
COMMIT;
