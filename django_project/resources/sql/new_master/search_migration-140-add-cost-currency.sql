BEGIN;

ALTER TABLE search_searchrecord ADD "cost_per_scene" numeric(10, 2);
ALTER TABLE search_searchrecord ADD "rand_cost_per_scene" numeric(10, 2);
ALTER TABLE search_searchrecord ADD "currency_id" integer;

CREATE INDEX "search_searchrecord_currency_id" ON "search_searchrecord" ("currency_id");

COMMIT;