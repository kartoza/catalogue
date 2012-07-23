BEGIN;
UPDATE catalogue_genericimageryproduct SET
band_count = 3

FROM (SELECT
  catalogue_genericimageryproduct.genericproduct_ptr_id as aqu_id
FROM
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct
WHERE
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id
  AND acquisition_mode_id IN (4,5,6,7,8,9,10,11,12,14,86,87,88,89,90,91)) as aqu_table

WHERE catalogue_genericimageryproduct.genericproduct_ptr_id = aqu_id;
COMMIT;