BEGIN;
delete from catalogue_ordernotificationrecipients_sensors where missionsensor_id in (6,7,8,9);
delete from catalogue_search_sensors where missionsensor_id in (6,7,8,9);
delete from catalogue_taskingrequest where mission_sensor_id in (6,7,8,9);
delete from catalogue_missionsensor where id in (6,7,8,9);
COMMIT;
