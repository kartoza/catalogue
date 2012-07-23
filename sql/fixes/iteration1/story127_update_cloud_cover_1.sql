BEGIN;
UPDATE public.catalogue_opticalproduct SET cloud_cover=cloud_cover*10
FROM
(SELECT
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id as aqu_id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_opticalproduct
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericsensorproduct.genericimageryproduct_ptr_id
  AND (acquisition_mode_id BETWEEN 76 AND 81 OR acquisition_mode_id BETWEEN 4 AND 7) AND cloud_cover != -1) as aqu_table

WHERE catalogue_opticalproduct.genericsensorproduct_ptr_id = aqu_table.aqu_id;
COMMIT;