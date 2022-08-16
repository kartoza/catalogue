BEGIN;
CREATE OR REPLACE VIEW pycsw_catalogue AS
SELECT
  catalogue_genericproduct.unique_product_id as product_id,
  'csw:Record'::text as typename,
  'http://www.opengis.net/cat/csw/2.0.2'::text as csw_schema,
  catalogue_genericproduct.product_date as insertdate,
  ''::text as csw_xml,
  ''::text as csw_anytext,
  ''::text as csw_creator,
  ''::text as csw_identifier,
  ''::text as csw_language,
  ''::text as csw_type,
  st_astext(spatial_coverage) as wkt_geometry,
  ''::text as accessconstraints,
  metadata as csw_metadata,
  ''::text as relation,
  catalogue_genericproduct.id as id,
  spatial_coverage,
  'image'::text as csw_keywords,
  'test,test_desc,http,http://catalogue.sansa.org.za/showProduct/'||unique_product_id::text as csw_links
FROM
  public.catalogue_genericproduct;

COMMIT;