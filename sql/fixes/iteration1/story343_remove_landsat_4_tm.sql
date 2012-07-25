-- delete associated search date ranges
delete from catalogue_searchdaterange where search_id in (select id from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where sensor_type_id in (11, 12, 3)));

-- Delete associated search date ranges
delete from catalogue_searchdaterange where search_id in (select id from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where sensor_type_id in (11, 12, 3)));

-- Delete associated search sensors
delete from catalogue_search_sensors where missionsensor_id in (select id from catalogue_missionsensor where name = 'Landsat 4 TM');
delete from  catalogue_search_sensors where search_id in (select id from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where sensor_type_id in ( select id from catalogue_sensortype where mission_sensor_id in (select id from catalogue_missionsensor where name = 'Landsat 4 TM'))));

-- delete the associated catalogue search records
delete from catalogue_search where acquisition_mode_id in (select id from catalogue_acquisitionmode where sensor_type_id in ( select id from catalogue_sensortype where mission_sensor_id in (select id from catalogue_missionsensor where name = 'Landsat 4 TM')));


-- Delete the associated acquisition mode
delete from catalogue_acquisitionmode where sensor_type_id in (select id from catalogue_sensortype where mission_sensor_id in (select id from catalogue_missionsensor where name = 'Landsat 4 TM'));

-- Delete associated sensor types (11,12,3)
delete from catalogue_sensortype where mission_sensor_id in (select id from catalogue_missionsensor where name = 'Landsat 4 TM');

-- Delete associated order notification sensors
delete from catalogue_ordernotificationrecipients_sensors where missionsensor_id in (select id from catalogue_missionsensor where name = 'Landsat 4 TM');

-- Delete the bogus mission sensor
delete from catalogue_missionsensor where name = 'Landsat 4 TM'
