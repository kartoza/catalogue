BEGIN;
ALTER TABLE catalogue_search RENAME geometric_accuracy_mean TO spatial_resolution;
COMMIT;