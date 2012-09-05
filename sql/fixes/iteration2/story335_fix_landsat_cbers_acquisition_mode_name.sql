BEGIN;
UPDATE catalogue_acquisitionmode 
SET abbreviation = 'BPSM',
name = 'Bumper (BUMP) or Scan Angle Monitor (SAM) Mode',
operator_abbreviation = 'BPSM'

WHERE catalogue_acquisitionmode.id IN (76,77,78,79,80,81);

UPDATE catalogue_acquisitionmode 
SET abbreviation = 'GRN',
name = 'GRN',
operator_abbreviation = 'GRN'

WHERE catalogue_acquisitionmode.id = 12;
COMMIT;
