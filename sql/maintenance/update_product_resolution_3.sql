BEGIN;
UPDATE catalogue_genericimageryproduct SET
spatial_resolution = 30,
spatial_resolution_x = 30,
spatial_resolution_y = 30

FROM (SELECT
  catalogue_genericimageryproduct.genericproduct_ptr_id as aqu_id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct
WHERE
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id
  AND acquisition_mode_id = 80) as aqu_table

WHERE catalogue_genericimageryproduct.genericproduct_ptr_id = aqu_id;
COMMIT;