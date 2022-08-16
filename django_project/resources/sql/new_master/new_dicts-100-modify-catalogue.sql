BEGIN;

-- we must add NOT NULL constraint after data migration
ALTER TABLE "catalogue_radarproduct" ADD
    "product_profile_id" integer REFERENCES "dictionaries_radarproductprofile" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_opticalproduct" ADD
    "product_profile_id" integer REFERENCES "dictionaries_opticalproductprofile" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "catalogue_radarproduct_product_profile_id" ON "catalogue_radarproduct" ("product_profile_id");
CREATE INDEX "catalogue_opticalproduct_product_profile_id" ON "catalogue_opticalproduct" ("product_profile_id");



COMMIT;
