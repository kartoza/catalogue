-- remove all spot products which are not ordered or currently in cart
-- spot will be reingested after the migration

BEGIN;

CREATE TABLE tmp_spot_products AS (

SELECT
  catalogue_opticalproduct.genericsensorproduct_ptr_id as free_spot
FROM
  public.catalogue_opticalproduct,
  public.dictionaries_opticalproductprofile
WHERE
  catalogue_opticalproduct.product_profile_id = dictionaries_opticalproductprofile.id AND
  dictionaries_opticalproductprofile.satellite_instrument_id BETWEEN 1 AND 10

EXCEPT

SELECT
  catalogue_opticalproduct.genericsensorproduct_ptr_id AS ordered_ids
FROM
  public.search_searchrecord,
  public.catalogue_opticalproduct,
  public.dictionaries_opticalproductprofile
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = search_searchrecord.product_id AND
  dictionaries_opticalproductprofile.id = catalogue_opticalproduct.product_profile_id AND
  dictionaries_opticalproductprofile.satellite_instrument_id BETWEEN 1 AND 10
  -- AND search_searchrecord.order_id IS NOT NULL
);


DELETE FROM catalogue_opticalproduct USING tmp_spot_products WHERE genericsensorproduct_ptr_id = free_spot;
DELETE FROM catalogue_genericsensorproduct USING tmp_spot_products WHERE genericimageryproduct_ptr_id = free_spot;
DELETE FROM catalogue_genericimageryproduct USING tmp_spot_products WHERE genericproduct_ptr_id = free_spot;
DELETE FROM catalogue_genericproduct USING tmp_spot_products WHERE id = free_spot;

drop table tmp_spot_products;

COMMIT;
