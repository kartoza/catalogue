BEGIN;
-- delete from catalogue_opticalproduct 
delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from catalogue_genericproduct where id in (select genericimageryproduct_ptr_id from catalogue_genericsensorproduct where (acquisition_mode_id = 92 OR acquisition_mode_id = 93)) AND substring (catalogue_genericproduct.product_id from 5 for 3) = 'VMI');

-- delete from catalogue_genericimageryproduct 
delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from catalogue_genericproduct where id in (select genericimageryproduct_ptr_id from catalogue_genericsensorproduct where (acquisition_mode_id = 92 OR acquisition_mode_id = 93)) AND substring (catalogue_genericproduct.product_id from 5 for 3) = 'VMI');

-- delete from catalogue_genericsensorproduct
 delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from catalogue_genericproduct where id in (select genericimageryproduct_ptr_id from catalogue_genericsensorproduct where (acquisition_mode_id = 92 OR acquisition_mode_id = 93)) AND substring (catalogue_genericproduct.product_id from 5 for 3) = 'VMI');

-- delete from catalogue_searchrecord
delete from catalogue_searchrecord where product_id in (select id from catalogue_genericproduct where substring (catalogue_genericproduct.product_id from 5 for 3) = 'VMI');

-- delete from catalogue_genericproduct 
delete from catalogue_genericproduct where substring (catalogue_genericproduct.product_id from 5 for 3) = 'VMI';

COMMIT;
