BEGIN;
  delete from catalogue_opticalproduct where genericsensorproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%MODE=COLOR%TYPE=T%');
  delete from catalogue_genericsensorproduct where genericimageryproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%MODE=COLOR%TYPE=T%');
  delete from catalogue_genericimageryproduct where genericproduct_ptr_id in (select id from catalogue_genericproduct where metadata like '%MODE=COLOR%TYPE=T%');
  delete from catalogue_searchrecord where product_id in (select id from catalogue_genericproduct where metadata like '%MODE=COLOR%TYPE=T%');
  delete from catalogue_genericproduct where metadata like '%MODE=COLOR%TYPE=T%';
COMMIT;
