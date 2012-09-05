BEGIN;
UPDATE catalogue_sensortype 
SET abbreviation = 'VIR',
name = 'Visual, NIR',
operator_abbreviation = 'VIR'

WHERE catalogue_sensortype.id IN (174,175,176,177);

UPDATE catalogue_sensortype 
SET abbreviation = 'HRF',
name = 'Visual, NIR, SWIR and Thermal',
operator_abbreviation = 'HRF'

WHERE catalogue_sensortype.id IN (178,179);

UPDATE catalogue_sensortype 
SET abbreviation = 'STM',
name = 'Strip Map C Band',
operator_abbreviation = 'STM'

WHERE catalogue_sensortype.id IN (2);
COMMIT;
