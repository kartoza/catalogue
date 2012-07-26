BEGIN;
  update catalogue_sensortype set operator_abbreviation = 'I' where id = 34;
COMMIT;
