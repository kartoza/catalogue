BEGIN;
update catalogue_genericproduct SET owner_id = ic_inst.id
FROM (select id from catalogue_institution where name='CONAE') as ic_inst, (SELECT
  catalogue_genericproduct.id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct,
  public.catalogue_genericproduct
WHERE
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id AND
  catalogue_genericimageryproduct.genericproduct_ptr_id = catalogue_genericproduct.id
  AND catalogue_genericsensorproduct.acquisition_mode_id = 15) AS aq_mode

WHERE catalogue_genericproduct.id = aq_mode.id;
COMMIT;