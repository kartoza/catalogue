BEGIN;

ALTER TABLE "catalogue_taskingrequest" ADD
    "satellite_instrument_group_id" integer REFERENCES "dictionaries_satelliteinstrumentgroup" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;



BEGIN;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 3
    WHERE mission_sensor_id = 2;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 1
    WHERE mission_sensor_id = 5;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 4
    WHERE mission_sensor_id = 10;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 17
    WHERE mission_sensor_id = 13;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 11
    WHERE mission_sensor_id = 14;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 2
    WHERE mission_sensor_id = 15;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 7
    WHERE mission_sensor_id = 16;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 21
    WHERE mission_sensor_id = 17;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 20
    WHERE mission_sensor_id = 18;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 13
    WHERE mission_sensor_id = 19;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 14
    WHERE mission_sensor_id = 20;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 15
    WHERE mission_sensor_id = 21;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 8
    WHERE mission_sensor_id = 22;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 18
    WHERE mission_sensor_id = 23;

UPDATE "catalogue_taskingrequest" SET satellite_instrument_group_id = 12
    WHERE mission_sensor_id = 24;

COMMIT;


BEGIN;


ALTER TABLE "catalogue_taskingrequest"
    ALTER "satellite_instrument_group_id" SET NOT NULL;

ALTER TABLE "catalogue_taskingrequest" DROP mission_sensor_id CASCADE;

COMMIT;
