BEGIN;
UPDATE public.catalogue_opticalproduct SET cloud_cover=-1
FROM
(SELECT
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id as aqu_id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_opticalproduct
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericsensorproduct.genericimageryproduct_ptr_id
  AND acquisition_mode_id IN (12,13,14,1,11,15)) as aqu_table

WHERE catalogue_opticalproduct.genericsensorproduct_ptr_id = aqu_table.aqu_id;
COMMIT;