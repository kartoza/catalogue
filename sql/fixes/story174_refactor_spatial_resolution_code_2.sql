BEGIN;
ALTER TABLE catalogue_acquisitionmode RENAME geometric_resolution TO spatial_resolution;
COMMIT;