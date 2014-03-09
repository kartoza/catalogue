BEGIN;

-- old dictionaries
ALTER TABLE dictionaries_projection DROP CONSTRAINT catalogue_projection_name_key1;

COMMIT;