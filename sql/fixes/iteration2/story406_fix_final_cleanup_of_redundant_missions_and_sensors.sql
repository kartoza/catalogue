BEGIN;
delete from catalogue_ordernotificationrecipients_sensors where missionsensor_id in (select id from catalogue_missionsensor where (mission_id  > 0 AND mission_id < 9) OR (mission_id >23 and mission_id < 49) OR (id=4) OR (id > 24 AND id < 40));
delete from catalogue_search_sensors where missionsensor_id in (select id from catalogue_missionsensor where (mission_id  > 0 AND mission_id < 9) OR (mission_id >23 and mission_id < 49) OR (id=4) OR (id > 24 AND id < 40));
delete from catalogue_taskingrequest where mission_sensor_id in (select id from catalogue_missionsensor where (mission_id  > 0 AND mission_id < 9) OR (mission_id >23 and mission_id < 49) OR (id=4) OR (id > 24 AND id < 40));
delete from catalogue_missionsensor where (mission_id  > 0 and mission_id < 9) OR (mission_id >23 and mission_id < 49) or (id=4) or (id > 24 and id < 40);
delete from catalogue_mission where (id > 0 and id < 9) OR (id >23 and id < 49);
COMMIT;
