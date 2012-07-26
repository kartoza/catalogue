BEGIN;
  update catalogue_sensortype set operator_abbreviation = 'X' where id = 28;
COMMIT;
