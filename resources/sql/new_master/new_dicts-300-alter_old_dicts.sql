BEGIN;

ALTER TABLE catalogue_projection RENAME TO dictionaries_projection;
ALTER TABLE catalogue_institution RENAME TO dictionaries_institution;
ALTER TABLE catalogue_license RENAME to dictionaries_license;
ALTER TABLE catalogue_quality RENAME to dictionaries_quality;
ALTER TABLE catalogue_topic RENAME TO dictionaries_topic;
ALTER TABLE catalogue_placetype RENAME TO dictionaries_placetype;
ALTER TABLE catalogue_place RENAME TO dictionaries_place;
ALTER TABLE catalogue_unit RENAME TO dictionaries_unit;

COMMIT;
