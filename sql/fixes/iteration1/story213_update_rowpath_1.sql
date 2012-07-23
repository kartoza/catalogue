BEGIN;
UPDATE catalogue_genericsensorproduct SET row=null, path=null WHERE acquisition_mode_id IN (1,2,11,15);
COMMIT;