BEGIN;

ALTER TABLE "catalogue_clip" RENAME TO "search_clip";

ALTER TABLE "catalogue_search" RENAME TO "search_search";

ALTER TABLE "catalogue_search_processing_level" RENAME TO "search_search_processing_level";

ALTER TABLE "catalogue_search_sensors" RENAME TO "search_search_sensors";

ALTER TABLE "catalogue_searchdaterange" RENAME TO "search_searchdaterange";

ALTER TABLE "catalogue_searchrecord" RENAME TO "search_searchrecord";

COMMIT;
