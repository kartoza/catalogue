begin;
create table tmp_sharpened_products AS
SELECT
  catalogue_genericimageryproduct.genericproduct_ptr_id as aqu_id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct
WHERE
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id
  AND acquisition_mode_id IN (94, 95);

delete from catalogue_opticalproduct using tmp_sharpened_products where genericsensorproduct_ptr_id=tmp_sharpened_products.aqu_id;
delete from catalogue_genericsensorproduct using tmp_sharpened_products where genericimageryproduct_ptr_id=tmp_sharpened_products.aqu_id;
delete from catalogue_genericimageryproduct using tmp_sharpened_products where genericproduct_ptr_id=tmp_sharpened_products.aqu_id;
delete from catalogue_searchrecord using tmp_sharpened_products where catalogue_searchrecord.product_id=tmp_sharpened_products.aqu_id;
delete from catalogue_genericproduct using tmp_sharpened_products where catalogue_genericproduct.id=tmp_sharpened_products.aqu_id;

drop table tmp_sharpened_products;


delete from catalogue_searchdaterange USING (SELECT id from catalogue_search where acquisition_mode_id in (94,95)) as searches where search_id = searches.id;
delete from catalogue_search_sensors USING (SELECT id from catalogue_search where acquisition_mode_id in (94,95)) as searches where search_id = searches.id;

delete from catalogue_search where acquisition_mode_id IN (94,95);
DELETE FROM catalogue_acquisitionmode where id in (94,95);
delete from catalogue_sensortype where id = 186;

commit;