CREATE OR REPLACE FUNCTION gen_xml_stub(i_pid IN text, o_xml OUT text) AS
$$
DECLARE
t_text TEXT;
l_corner TEXT;
u_corner TEXT;
BEGIN

SELECT Box2D(spatial_coverage)::text INTO t_text FROM catalogue_genericproduct where original_product_id=i_pid;

l_corner := ltrim(split_part(t_text,',',1),'BOX(');
u_corner := rtrim(split_part(t_text,',',2),')');

o_xml := '<?xml version="1.0" standalone="no"?>
    <csw:GetRecordByIdResponse xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope" xmlns:gml="http://www.opengis.net/gml" xmlns:dif="http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ows="http://www.opengis.net/ows" xmlns:fgdc="http://www.opengis.net/cat/csw/csdgm" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:os="http://a9.com/-/spec/opensearch/1.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:ogc="http://www.opengis.net/ogc" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd">
    <csw:Record>
        <dc:identifier>'||i_pid||'</dc:identifier>
        <dc:title>'||i_pid||'</dc:title>
        <dc:type>dataset</dc:type>
        <dc:subject>image</dc:subject>
        <dct:references scheme="http">http://catalogue.sansa.org.za/showProduct/'||i_pid||'</dct:references>
        <ows:BoundingBox crs="urn:x-ogc:def:crs:EPSG:6.11:4326" dimensions="2">
            <ows:LowerCorner>'||l_corner||'</ows:LowerCorner>
            <ows:UpperCorner>'||u_corner||'</ows:UpperCorner>
        </ows:BoundingBox>
    </csw:Record>
    </csw:GetRecordByIdResponse>';

END;
$$
LANGUAGE 'plpgsql' VOLATILE STRICT;

-- DROP view pycsw_catalogue;
create or replace view pycsw_catalogue as SELECT
    'csw:Record'::text AS csw_typename,
    'http://www.opengis.net/cat/csw/2.0.2'::text AS csw_schema,
    catalogue_genericproduct.original_product_id AS csw_identifier,
    dictionaries_satellite.name||' '||dictionaries_instrumenttype.name as csw_title,
    dictionaries_instrumenttype.band_type as csw_alternatetitle,
    dictionaries_institution.name as csw_organization_name,
    'Earth Observation and Remote Sensing Data'::text as csw_topiccategory,
    dictionaries_satellite.description||E'\n'||dictionaries_instrumenttype.description AS csw_abstract,
    dictionaries_instrumenttype.keywords AS csw_keywords,
    dictionaries_processinglevel.description as csw_lineage,
    dictionaries_license.name as csw_license,
    'EN'::text AS csw_language,
    public.catalogue_genericsensorproduct.product_acquisition_start as csw_temp_begin,
    public.catalogue_genericsensorproduct.product_acquisition_end as csw_temp_end,
    'link,Show Product,http,http://41.74.158.4/showProduct/'::text || catalogue_genericproduct.original_product_id::text AS csw_link,

    catalogue_genericproduct.product_date AS csw_insertdate,
    gen_xml_stub(catalogue_genericproduct.original_product_id) as csw_xml,
    ''::text AS csw_anytext,
    'dataset'::text AS csw_type,
    st_astext(catalogue_genericproduct.spatial_coverage) AS wkt_geometry,
    catalogue_genericproduct.id,
    catalogue_genericproduct.spatial_coverage
FROM
  public.catalogue_genericproduct,
  public.catalogue_genericimageryproduct,
  public.catalogue_opticalproduct,
  public.catalogue_genericsensorproduct,
  public.dictionaries_opticalproductprofile,
  public.dictionaries_satelliteinstrument,
  public.dictionaries_institution,
  public.dictionaries_satelliteinstrumentgroup,
  public.dictionaries_satellite,
  public.dictionaries_collection,
  public.dictionaries_instrumenttype,
  public.dictionaries_processinglevel,
  public.dictionaries_license
WHERE
  catalogue_genericimageryproduct.genericproduct_ptr_id = catalogue_genericproduct.id AND
  catalogue_opticalproduct.product_profile_id = dictionaries_opticalproductprofile.id AND
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id AND
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_opticalproduct.genericsensorproduct_ptr_id AND
  dictionaries_satelliteinstrument.id = dictionaries_opticalproductprofile.satellite_instrument_id AND
  dictionaries_satelliteinstrumentgroup.id = dictionaries_satelliteinstrument.satellite_instrument_group_id AND
  dictionaries_satellite.id = dictionaries_satelliteinstrumentgroup.satellite_id AND
  dictionaries_collection.institution_id = dictionaries_institution.id AND
  dictionaries_collection.id = dictionaries_satellite.collection_id AND
  dictionaries_instrumenttype.id = dictionaries_satelliteinstrumentgroup.instrument_type_id AND
  dictionaries_processinglevel.id = dictionaries_instrumenttype.default_processing_level_id AND
  dictionaries_license.id = dictionaries_satellite.license_type_id
ORDER BY catalogue_genericproduct.id ASC
LIMIT 100;

