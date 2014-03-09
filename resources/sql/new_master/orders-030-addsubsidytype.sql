BEGIN;

ALTER TABLE orders_order ADD "subsidy_type_requested_id" integer;
ALTER TABLE orders_order ADD "subsidy_type_assigned_id" integer;

ALTER TABLE "orders_order" ADD CONSTRAINT "subsidy_type_requested_id_refs_id_7f91e0b4" FOREIGN KEY ("subsidy_type_requested_id") REFERENCES "dictionaries_subsidytype" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "orders_order" ADD CONSTRAINT "subsidy_type_assigned_id_refs_id_7f91e0b4" FOREIGN KEY ("subsidy_type_assigned_id") REFERENCES "dictionaries_subsidytype" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "orders_order_subsidy_type_requested_id" ON "orders_order" ("subsidy_type_requested_id");
CREATE INDEX "orders_order_subsidy_type_assigned_id" ON "orders_order" ("subsidy_type_assigned_id");

COMMIT;
