BEGIN;
CREATE TABLE "exchange_currency" (
    "id" serial NOT NULL PRIMARY KEY,
    "code" varchar(3) NOT NULL UNIQUE,
    "name" varchar(64) NOT NULL
)
;
CREATE TABLE "exchange_exchangerate" (
    "id" serial NOT NULL PRIMARY KEY,
    "source_id" integer NOT NULL REFERENCES "exchange_currency" ("id") DEFERRABLE INITIALLY DEFERRED,
    "target_id" integer NOT NULL REFERENCES "exchange_currency" ("id") DEFERRABLE INITIALLY DEFERRED,
    "rate" numeric(17, 8) NOT NULL
)
;
CREATE INDEX "exchange_currency_code_like" ON "exchange_currency" ("code" varchar_pattern_ops);
CREATE INDEX "exchange_exchangerate_source_id" ON "exchange_exchangerate" ("source_id");
CREATE INDEX "exchange_exchangerate_target_id" ON "exchange_exchangerate" ("target_id");

COMMIT;
