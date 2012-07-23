BEGIN;
update catalogue_institution set name = 'SANSA' where id = 1;
update catalogue_institution set name = 'Astrium' where id = 4;
commit;