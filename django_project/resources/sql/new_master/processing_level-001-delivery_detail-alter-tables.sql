BEGIN;

ALTER TABLE catalogue_deliverydetail
    ADD new_processing_level_id integer REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;

BEGIN;

UPDATE catalogue_deliverydetail SET new_processing_level_id = 5 WHERE processing_level_id=1;
UPDATE catalogue_deliverydetail SET new_processing_level_id = 2 WHERE processing_level_id=2;
UPDATE catalogue_deliverydetail SET new_processing_level_id = 2 WHERE processing_level_id=3;
UPDATE catalogue_deliverydetail SET new_processing_level_id = 2 WHERE processing_level_id=4;
UPDATE catalogue_deliverydetail SET new_processing_level_id = 8 WHERE processing_level_id=12;
UPDATE catalogue_deliverydetail SET new_processing_level_id = 9 WHERE processing_level_id=13;
UPDATE catalogue_deliverydetail SET new_processing_level_id = 13 WHERE processing_level_id=18;

COMMIT;

BEGIN;

ALTER TABLE catalogue_deliverydetail DROP processing_level_id CASCADE;
ALTER TABLE catalogue_deliverydetail RENAME new_processing_level_id TO processing_level_id;
ALTER TABLE catalogue_deliverydetail ALTER processing_level_id SET NOT NULL;

COMMIT;