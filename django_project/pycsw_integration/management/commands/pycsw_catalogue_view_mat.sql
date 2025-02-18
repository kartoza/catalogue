CREATE MATERIALIZED VIEW pycsw_catalogue_view AS
WITH catalogue_extras AS (
    SELECT 
        product_date as date,
        original_product_id as Identifier,
        metadata as metadata,
        spatial_coverage as wkt_geometry,
        op.cloud_cover as cloud_cover,
        dit.keywords as keywords,
        ds.name || ' ' || dit.name as title,
        dinst.name as organization_name,
        ds.launch_date as date_creation,
        ds.description as abstract,
        ds.reference_url as links,
        dl.details as license,
        dit.name as instrument,
        gsp.product_acquisition_start as time_begin,
        gsp.product_acquisition_end as time_end,
        ds.abbreviation as anytext,
        dit.band_type as sensortype,
        dp.epsg_code as projection,
        ds.launch_date as insert_date,
        dpl.description as lineage,
        gip.band_count as band
    FROM public.catalogue_genericproduct gp
        JOIN public.catalogue_genericimageryproduct gip
            ON gp.id = gip.genericproduct_ptr_id
        JOIN public.dictionaries_projection as dp 
            ON gp.projection_id = dp.id
        JOIN public.catalogue_opticalproduct op
            ON gp.id = op.genericsensorproduct_ptr_id
        JOIN public.catalogue_genericsensorproduct gsp
            ON gip.genericproduct_ptr_id = gsp.genericimageryproduct_ptr_id
        JOIN public.dictionaries_opticalproductprofile dop
            ON op.product_profile_id = dop.id
        JOIN public.dictionaries_satelliteinstrument dsi
            ON dop.satellite_instrument_id = dsi.id
        JOIN public.dictionaries_satelliteinstrumentgroup dsig
            ON dsi.satellite_instrument_group_id = dsig.id
        JOIN public.dictionaries_satellite ds
            ON ds.id = dsig.satellite_id
        JOIN public.dictionaries_instrumenttype dit
            ON dsig.instrument_type_id = dit.id
        JOIN public.dictionaries_processinglevel dpl
            ON dit.default_processing_level_id = dpl.id
        JOIN public.dictionaries_collection dc
            ON ds.collection_id = dc.id
        JOIN public.dictionaries_institution dinst
            ON dc.institution_id = dinst.id
        JOIN public.dictionaries_license dl
            ON ds.license_type_id = dl.id
),
latest_catalogue AS (
    SELECT DISTINCT ON (Identifier) *
    FROM catalogue_extras
    ORDER BY Identifier, date DESC
)
SELECT * FROM (
    SELECT 
        c.date as date,
        c.Identifier as Identifier,
        'csw:Record' AS typename,
        'http://www.isotc211.org/2005/gmd' AS schema,
        'local' AS mdsource,
        NULL AS xml,
        NULL AS metadata,
        NULL AS metadata_type,
        'EN' AS language,
        NULL AS keywordstype,
        NULL AS format,
        NULL AS source,
        ST_AsText(c.wkt_geometry) AS wkt_geometry,
        c.wkt_geometry::geometry(Polygon, 4326) AS wkb_geometry,
        c.cloud_cover as cloudcover,
        c.keywords as keywords,
        c.title as title,
        c.date_creation as date_creation,
        c.abstract as abstract,
        NULL as links,
        'Dataset' as type,
        c.license as license,
        concat_ws('', 'EPSG:', c.projection) AS crs,
        c.instrument as instrument,
        c.time_begin as time_begin,
        c.time_end as time_end,
        c.anytext as anytext,
        c.sensortype as sensortype,
        c.insert_date as insert_date,
        concat_ws(' ', c.title, c.Identifier) AS title_alternate,
        NULL AS date_modified,
        NULL AS date_revision,
        NULL AS date_publication,
        c.organization_name AS organization,
        NULL AS securityconstraints,
        NULL AS parentidentifier,
        'imageryBaseMapsEarthCover'::text AS topiccategory,
        'EN' AS resourcelanguage,
        NULL AS geodescode,
        NULL AS denominator,
        NULL AS distancevalue,
        NULL AS distanceuom,
        NULL AS servicetype,
        NULL AS servicetypeversion,
        NULL AS operation,
        NULL AS couplingtype,
        NULL AS operateson,
        NULL AS operatesonidentifier,
        NULL AS operatesonname,
        NULL AS degree,
        NULL AS accessconstraints,
        NULL AS edition,
        NULL AS otherconstraints,
        NULL AS classification,
        NULL AS conditionapplyingtoaccessanduse,
        c.lineage AS lineage,
        NULL AS responsiblepartyrole,
        NULL AS specificationtitle,
        NULL AS specificationdate,
        NULL AS specificationdatetype,
        NULL AS creator,
        NULL AS publisher,
        NULL AS contributor,
        NULL AS relation,
        NULL AS platform,
        c.band AS bands
    FROM latest_catalogue AS c
) sub
ORDER BY sub.date
LIMIT {limit};
