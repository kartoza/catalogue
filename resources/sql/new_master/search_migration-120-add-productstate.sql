BEGIN;

ALTER TABLE search_searchrecord ADD "productprocessstate_id" integer;

ALTER TABLE "search_searchrecord" ADD CONSTRAINT "productprocessstate_id_refs_id_4af7829f" FOREIGN KEY ("productprocessstate_id") REFERENCES "dictionaries_productprocessstate" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "search_searchrecord_productprocessstate_id" ON "search_searchrecord" ("productprocessstate_id");

COMMIT;