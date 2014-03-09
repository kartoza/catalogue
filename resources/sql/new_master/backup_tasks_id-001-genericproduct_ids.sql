-- create a temporary copy of products ids
-- this table will be used for thumbnail migration, and similar tasks

BEGIN;

CREATE TABLE temporary_product_mapping AS (
SELECT id, original_product_id, product_id from catalogue_genericproduct
);

COMMIT;
