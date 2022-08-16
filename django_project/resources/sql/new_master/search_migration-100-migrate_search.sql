BEGIN;

DROP TABLE search_search_processing_level CASCADE;

CREATE TABLE "search_search_instrument_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "instrumenttype_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "instrumenttype_id")
)
;
CREATE TABLE "search_search_spectral_group" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "spectralgroup_id" integer NOT NULL REFERENCES "dictionaries_spectralgroup" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "spectralgroup_id")
)
;
CREATE TABLE "search_search_processing_level" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "processinglevel_id" integer NOT NULL REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "processinglevel_id")
)
;
CREATE TABLE "search_search_satellite" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "satellite_id" integer NOT NULL REFERENCES "dictionaries_satellite" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "satellite_id")
)
;
CREATE TABLE "search_search_collection" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "collection_id" integer NOT NULL REFERENCES "dictionaries_collection" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "collection_id")
)
;
CREATE TABLE "search_search_license_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "license_id" integer NOT NULL REFERENCES "dictionaries_license" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "license_id")
)
;


ALTER TABLE "search_search_instrument_type" ADD CONSTRAINT "search_id_refs_id_8a552118" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search_spectral_group" ADD CONSTRAINT "search_id_refs_id_9f61c8db" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search_processing_level" ADD CONSTRAINT "search_id_refs_id_2503a17" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search_satellite" ADD CONSTRAINT "search_id_refs_id_d04b6631" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search_collection" ADD CONSTRAINT "search_id_refs_id_69cf5df7" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search_license_type" ADD CONSTRAINT "search_id_refs_id_a2233b6f" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;
