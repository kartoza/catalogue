BEGIN;

-- orders
ALTER TABLE orders_order ADD "datum_id" integer REFERENCES "orders_datum" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE orders_order ADD "resampling_method_id" integer REFERENCES "orders_resamplingmethod" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE orders_order ADD "file_format_id" integer REFERENCES "orders_fileformat" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "orders_order_datum_id" ON "orders_order" ("datum_id");
CREATE INDEX "orders_order_resampling_method_id" ON "orders_order" ("resampling_method_id");
CREATE INDEX "orders_order_file_format_id" ON "orders_order" ("file_format_id");

-- update orders

UPDATE orders_order SET datum_id = dd.datum_id,resampling_method_id = dd.resampling_method_id, file_format_id = dd.file_format_id FROM orders_order oo INNER JOIN orders_deliverydetail dd ON oo.delivery_detail_id = dd.id WHERE orders_order.id=oo.id;


-- search records (cart)

ALTER TABLE search_searchrecord ADD "processing_level_id" integer REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE search_searchrecord ADD "projection_id" integer REFERENCES "dictionaries_projection" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "search_searchrecord_processing_level_id" ON "search_searchrecord" ("processing_level_id");
CREATE INDEX "search_searchrecord_projection_id" ON "search_searchrecord" ("projection_id");

-- update searchrecord

WITH sr_dd AS (select sr.id as id, dd.processing_level_id, dd.projection_id FROM search_searchrecord sr INNER JOIN orders_deliverydetail dd ON sr.delivery_detail_id = dd.id)
UPDATE search_searchrecord SET projection_id = sr_dd.projection_id,processing_level_id = sr_dd.processing_level_id FROM sr_dd where search_searchrecord.id=sr_dd.id;

COMMIT;


BEGIN;

-- Add not null after the migration

ALTER TABLE orders_order ALTER "datum_id" SET NOT NULL;
ALTER TABLE orders_order ALTER "resampling_method_id" SET NOT NULL;
ALTER TABLE orders_order ALTER "file_format_id" SET NOT NULL;

-- drop delivery_details FK
ALTER TABLE search_searchrecord DROP delivery_detail_id;
ALTER TABLE orders_order DROP delivery_detail_id;
COMMIT;
