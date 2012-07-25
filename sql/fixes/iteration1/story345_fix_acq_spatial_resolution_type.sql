BEGIN;
alter table catalogue_acquisitionmode add column tmp float null;
update catalogue_acquisitionmode set tmp = spatial_resolution;
alter table catalogue_acquisitionmode drop column spatial_resolution ;
alter table catalogue_acquisitionmode rename column tmp to "spatial_resolution";
alter table catalogue_acquisitionmode alter column spatial_resolution set not null;
COMMIT;
