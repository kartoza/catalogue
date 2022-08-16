BEGIN;

CREATE TABLE "catalogue_ordernotificationrecipients_satellite_instrument_2e0d" (
    "id" serial NOT NULL PRIMARY KEY,
    "ordernotificationrecipients_id" integer NOT NULL,
    "satelliteinstrumentgroup_id" integer NOT NULL REFERENCES "dictionaries_satelliteinstrumentgroup" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("ordernotificationrecipients_id", "satelliteinstrumentgroup_id")
)
;

ALTER TABLE "catalogue_ordernotificationrecipients_satellite_instrument_2e0d" ADD CONSTRAINT "ordernotificationrecipients_id_refs_id_ce6d9225" FOREIGN KEY ("ordernotificationrecipients_id") REFERENCES "catalogue_ordernotificationrecipients" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;



BEGIN;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 3
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=2;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 1
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=5;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 4
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=10;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 17
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=13;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 11
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=14;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 2
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=15;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 7
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=16;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 21
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=17;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 20
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=18;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 13
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=19;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 14
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=20;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 15
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=21;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 8
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=22;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 18
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=23;

INSERT INTO catalogue_ordernotificationrecipients_satellite_instrument_2e0d (ordernotificationrecipients_id, satelliteinstrumentgroup_id)
    SELECT ordernotificationrecipients_id, 12
    FROM catalogue_ordernotificationrecipients_sensors WHERE missionsensor_id=24;

COMMIT;


BEGIN;
-- remove old table
DROP TABLE catalogue_ordernotificationrecipients_sensors ;

-- add unique constraint
ALTER TABLE "catalogue_ordernotificationrecipients_satellite_instrument_2e0d" ADD CONSTRAINT
    "catalogue_ordernotificationre_ordernotificationrecipients_i_key" UNIQUE ("ordernotificationrecipients_id", "satelliteinstrumentgroup_id");
COMMIT;
