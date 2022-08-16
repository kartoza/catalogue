BEGIN;

ALTER TABLE catalogue_genericproduct ADD unique_product_id varchar(255);

COMMIT;



BEGIN;

UPDATE catalogue_genericproduct SET unique_product_id = original_product_id;

-- update Sumbandilasat, ERS, SACC, CBERS to SAC_ID

UPDATE catalogue_genericproduct SET
    unique_product_id = product_id
FROM
  dictionaries_opticalproductprofile,
  catalogue_opticalproduct,
  dictionaries_spectralmode
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericproduct.id AND
  catalogue_opticalproduct.product_profile_id = dictionaries_opticalproductprofile.id AND
  dictionaries_spectralmode.id = dictionaries_opticalproductprofile.spectral_mode_id AND
  catalogue_opticalproduct.product_profile_id IN (2,3,4,5,6);


-- update SPOT5 products
UPDATE catalogue_genericproduct SET
    unique_product_id = substring(
        original_product_id from 0 for length(original_product_id)
    )||dictionaries_spectralmode.abbreviation
FROM
  dictionaries_opticalproductprofile,
  catalogue_opticalproduct,
  dictionaries_spectralmode
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericproduct.id AND
  catalogue_opticalproduct.product_profile_id = dictionaries_opticalproductprofile.id AND
  dictionaries_spectralmode.id = dictionaries_opticalproductprofile.spectral_mode_id AND
  catalogue_opticalproduct.product_profile_id IN (13,14,15,16,17,18,19,20);

-- update lansat5

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id IN (
  SELECT unique_product_id
  from catalogue_genericproduct
  group by unique_product_id
  having count(*)>1) AND substring(product_id from length(product_id)) = 'N'
)
DELETE FROM catalogue_opticalproduct USING tmp_gen_prod_id
  WHERE genericsensorproduct_ptr_id= tmp_gen_prod_id.id;

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id IN (
  SELECT unique_product_id
  from catalogue_genericproduct
  group by unique_product_id
  having count(*)>1) AND substring(product_id from length(product_id)) = 'N'
)
DELETE FROM catalogue_genericsensorproduct USING tmp_gen_prod_id
  WHERE genericimageryproduct_ptr_id = tmp_gen_prod_id.id;

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id IN (
  SELECT unique_product_id
  from catalogue_genericproduct
  group by unique_product_id
  having count(*)>1) AND substring(product_id from length(product_id)) = 'N'
)
DELETE FROM catalogue_genericimageryproduct USING tmp_gen_prod_id
  WHERE genericproduct_ptr_id = tmp_gen_prod_id.id;

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id IN (
  SELECT unique_product_id
  from catalogue_genericproduct
  group by unique_product_id
  having count(*)>1) AND substring(product_id from length(product_id)) = 'N'
)
DELETE FROM catalogue_genericproduct USING tmp_gen_prod_id
  WHERE catalogue_genericproduct.id = tmp_gen_prod_id.id;

-- delete all remaining duplicate leftover L5 products

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id = '534539'
)
DELETE FROM catalogue_opticalproduct USING tmp_gen_prod_id
  WHERE genericsensorproduct_ptr_id= tmp_gen_prod_id.id;

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id = '534539'
)
DELETE FROM catalogue_genericsensorproduct USING tmp_gen_prod_id
  WHERE genericimageryproduct_ptr_id = tmp_gen_prod_id.id;

WITH tmp_gen_prod_id AS (
select id FROM catalogue_genericproduct
WHERE unique_product_id = '534539'
)
DELETE FROM catalogue_genericimageryproduct USING tmp_gen_prod_id
  WHERE genericproduct_ptr_id = tmp_gen_prod_id.id;


DELETE FROM catalogue_genericproduct WHERE unique_product_id = '534539';

-- copy unique_product_id to original_product_id and set unique_product_id to null
UPDATE catalogue_genericproduct SET original_product_id = unique_product_id, unique_product_id=NULL;

COMMIT;



BEGIN;
ALTER TABLE catalogue_genericproduct ALTER original_product_id SET NOT NULL;
ALTER TABLE catalogue_genericproduct
    ADD CONSTRAINT original_product_id UNIQUE (original_product_id);

-- drop product_id column
ALTER TABLE catalogue_genericproduct DROP product_id CASCADE;

-- recreate dropped views
create view vw_usercart as SELECT
  search_searchrecord.id, search_searchrecord.order_id,
  auth_user.username,
  catalogue_genericproduct."original_product_id",
  catalogue_genericproduct.spatial_coverage
FROM
  public.search_searchrecord,
  public.catalogue_genericproduct,
  public.auth_user
WHERE
  search_searchrecord.user_id = auth_user.id AND
  search_searchrecord.product_id = catalogue_genericproduct.id AND
  search_searchrecord.order_id isnull;
grant select on vw_usercart to readonly;
COMMIT;