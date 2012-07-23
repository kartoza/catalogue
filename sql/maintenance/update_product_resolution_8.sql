BEGIN;
UPDATE catalogue_genericimageryproduct SET
geometric_resolution = 20,
geometric_resolution_x = 20,
geometric_resolution_y = 20

FROM (SELECT
  catalogue_genericimageryproduct.genericproduct_ptr_id as aqu_id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct
WHERE
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id
  AND acquisition_mode_id BETWEEN 4 AND 10) as aqu_table

WHERE catalogue_genericimageryproduct.genericproduct_ptr_id = aqu_id;
COMMIT;