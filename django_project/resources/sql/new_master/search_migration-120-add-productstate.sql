BEGIN;

ALTER TABLE search_searchrecord ADD "product_process_state_id" integer;

ALTER TABLE "search_searchrecord" ADD CONSTRAINT "productprocessstate_id_refs_id_4af7829f" FOREIGN KEY ("product_process_state_id") REFERENCES "dictionaries_productprocessstate" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "search_searchrecord_productprocessstate_id" ON "search_searchrecord" ("product_process_state_id");

COMMIT;