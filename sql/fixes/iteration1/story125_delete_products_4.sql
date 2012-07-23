BEGIN;
create table delete_landsat_row AS
SELECT
   public.catalogue_genericproduct.id
FROM
  public.catalogue_opticalproduct,
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct,
  public.catalogue_genericproduct,
-- landsat products subquery
(SELECT catalogue_acquisitionmode.id as id
FROM
  public.catalogue_mission,
  public.catalogue_missionsensor,
  public.catalogue_sensortype,
  public.catalogue_acquisitionmode
WHERE
  catalogue_missionsensor.mission_id = catalogue_mission.id AND
  catalogue_sensortype.mission_sensor_id = catalogue_missionsensor.id AND
  catalogue_acquisitionmode.sensor_type_id = catalogue_sensortype.id AND
  catalogue_mission.operator_abbreviation ILIKE 'LS%') AS landsat_prod
-- landsat products subquery
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericsensorproduct.genericimageryproduct_ptr_id AND
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id AND
  catalogue_genericimageryproduct.genericproduct_ptr_id = catalogue_genericproduct.id AND
--landsat
  catalogue_genericsensorproduct.acquisition_mode_id = landsat_prod.id AND
  catalogue_genericsensorproduct.path = 188;

delete from catalogue_opticalproduct using delete_landsat_row where genericsensorproduct_ptr_id=delete_landsat_row.id;
delete from catalogue_genericsensorproduct using delete_landsat_row where genericimageryproduct_ptr_id=delete_landsat_row.id;
delete from catalogue_genericimageryproduct using delete_landsat_row where genericproduct_ptr_id=delete_landsat_row.id;
delete from catalogue_searchrecord using delete_landsat_row where catalogue_searchrecord.product_id=delete_landsat_row.id;
delete from catalogue_genericproduct using delete_landsat_row where catalogue_genericproduct.id=delete_landsat_row.id;

--
drop table delete_landsat_row;
COMMIT;