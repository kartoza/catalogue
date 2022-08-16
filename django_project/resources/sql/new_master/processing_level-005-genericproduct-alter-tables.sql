BEGIN;

ALTER TABLE catalogue_genericproduct
    ADD new_processing_level_id integer REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;

BEGIN;

-- update optical products

UPDATE catalogue_genericproduct SET new_processing_level_id = dictionaries_instrumenttype.base_processing_level_id
FROM
  catalogue_opticalproduct,
  dictionaries_opticalproductprofile,
  dictionaries_satelliteinstrument,
  dictionaries_satelliteinstrumentgroup,
  dictionaries_instrumenttype
WHERE
  catalogue_genericproduct.id = catalogue_opticalproduct.genericsensorproduct_ptr_id AND
  dictionaries_opticalproductprofile.id = catalogue_opticalproduct.product_profile_id AND
  dictionaries_satelliteinstrument.id = dictionaries_opticalproductprofile.satellite_instrument_id AND
  dictionaries_satelliteinstrumentgroup.id = dictionaries_satelliteinstrument.satellite_instrument_group_id AND
  dictionaries_instrumenttype.id = dictionaries_satelliteinstrumentgroup.instrument_type_id;


-- update radar products
UPDATE catalogue_genericproduct SET new_processing_level_id = dictionaries_instrumenttype.base_processing_level_id
FROM
  dictionaries_satelliteinstrument,
  dictionaries_satelliteinstrumentgroup,
  dictionaries_instrumenttype,
  dictionaries_radarproductprofile,
  catalogue_radarproduct
WHERE
  catalogue_genericproduct.id = catalogue_radarproduct.genericsensorproduct_ptr_id AND
  dictionaries_satelliteinstrument.id = dictionaries_radarproductprofile.satellite_instrument_id AND
  dictionaries_satelliteinstrumentgroup.id = dictionaries_satelliteinstrument.satellite_instrument_group_id AND
  dictionaries_instrumenttype.id = dictionaries_satelliteinstrumentgroup.instrument_type_id AND
  catalogue_radarproduct.product_profile_id = dictionaries_radarproductprofile.id;

COMMIT;

BEGIN;

ALTER TABLE catalogue_genericproduct DROP processing_level_id CASCADE;
ALTER TABLE catalogue_genericproduct RENAME new_processing_level_id TO processing_level_id;
ALTER TABLE catalogue_genericproduct ALTER processing_level_id SET NOT NULL;

COMMIT;