BEGIN;

-- insert instrument types

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 1 FROM search_search_sensors WHERE missionsensor_id=2;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 2 FROM search_search_sensors WHERE missionsensor_id=13;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT DISTINCT search_id, 3 FROM search_search_sensors WHERE missionsensor_id IN (17,18,19,20);

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 4 FROM search_search_sensors WHERE missionsensor_id=16;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 5 FROM search_search_sensors WHERE missionsensor_id=5;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT DISTINCT search_id, 6 FROM search_search_sensors WHERE missionsensor_id IN (21,22,23);

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 7 FROM search_search_sensors WHERE missionsensor_id=24;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 8 FROM search_search_sensors WHERE missionsensor_id=10;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 9 FROM search_search_sensors WHERE missionsensor_id=14;

INSERT INTO "search_search_instrument_type" (search_id, instrumenttype_id)
    SELECT search_id, 10 FROM search_search_sensors WHERE missionsensor_id=15;


-- update spectral group (was sensor_type)
INSERT INTO "search_search_spectral_group" (search_id, spectralgroup_id)
    SELECT id, 1 FROM search_search where sensor_type_id IN (6, 42, 174, 175, 176, 177, 178, 179, 182, 184, 187, 185);

INSERT INTO "search_search_spectral_group" (search_id, spectralgroup_id)
    SELECT id, 2 FROM search_search where sensor_type_id IN (26, 29, 32, 36, 40, 41, 44);

INSERT INTO "search_search_spectral_group" (search_id, spectralgroup_id)
    SELECT id, 4 FROM search_search where sensor_type_id IN (8);



-- update satellite (was mission)

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 1 FROM search_search WHERE mission_id = 19;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 2 FROM search_search WHERE mission_id = 23;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 3 FROM search_search WHERE mission_id = 12;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 4 FROM search_search WHERE mission_id = 13;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 5 FROM search_search WHERE mission_id = 14;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 6 FROM search_search WHERE mission_id = 10;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 7 FROM search_search WHERE mission_id = 11;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 8 FROM search_search WHERE mission_id = 17;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 9 FROM search_search WHERE mission_id = 15;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 10 FROM search_search WHERE mission_id = 22;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 11 FROM search_search WHERE mission_id = 16;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 12 FROM search_search WHERE mission_id = 18;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 13 FROM search_search WHERE mission_id = 20;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 14 FROM search_search WHERE mission_id = 21;

INSERT INTO "search_search_satellite" (search_id, satellite_id)
    SELECT id, 15 FROM search_search WHERE mission_id = 9;

-- license type
INSERT INTO "search_search_license_type" (search_id, license_id)
    SELECT id, license_type FROM search_search where license_type is not null;

COMMIT;