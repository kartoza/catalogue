BEGIN;

-- drop old unsed table

DROP TABLE search_search_sensors CASCADE;

-- delete radar searches

delete from search_search_instrument_type where search_id IN (SELECT DISTINCT id from search_search where acquisition_mode_id = 2);
delete from search_searchdaterange where search_id IN (SELECT DISTINCT id from search_search where acquisition_mode_id = 2);
DELETE FROM search_search_satellite where search_id = (SELECT DISTINCT id from search_search where acquisition_mode_id = 2);
DELETE FROM search_search_license_type where search_id = (SELECT DISTINCT id from search_search where acquisition_mode_id = 2);
delete from search_search where  acquisition_mode_id = 2;

COMMIT;

BEGIN;

-- drop unused attributes

ALTER TABLE "search_search" DROP COLUMN search_type;
ALTER TABLE "search_search" DROP COLUMN keywords;
ALTER TABLE "search_search" DROP COLUMN polarising_mode;
ALTER TABLE "search_search" DROP COLUMN mission_id CASCADE;
ALTER TABLE "search_search" DROP COLUMN sensor_type_id CASCADE;
ALTER TABLE "search_search" DROP COLUMN acquisition_mode_id CASCADE;
ALTER TABLE "search_search" DROP COLUMN license_type CASCADE;


COMMIT;
