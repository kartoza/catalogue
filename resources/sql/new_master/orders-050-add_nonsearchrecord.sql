BEGIN;

CREATE TABLE "orders_nonsearchrecord" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "order_id" integer REFERENCES "orders_order" ("id") DEFERRABLE INITIALLY DEFERRED,
    "product_description" varchar(100) NOT NULL,
    "download_path" varchar(512) NOT NULL,
    "cost_per_scene" numeric(10, 2),
    "rand_cost_per_scene" numeric(10, 2),
    "currency_id" integer
)
;

CREATE INDEX "orders_nonsearchrecord_user_id" ON "orders_nonsearchrecord" ("user_id");
CREATE INDEX "orders_nonsearchrecord_order_id" ON "orders_nonsearchrecord" ("order_id");
CREATE INDEX "orders_nonsearchrecord_currency_id" ON "orders_nonsearchrecord" ("currency_id");

COMMIT;
