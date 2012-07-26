BEGIN;
  update catalogue_genericproduct set owner_id = 4 where owner_id = 10;
COMMIT;
