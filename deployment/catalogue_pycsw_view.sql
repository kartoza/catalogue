
CREATE MATERIALIZED VIEW IF NOT EXISTS catalogue_pycsw_view AS
    WITH catalogue_extras AS (
    SELECT product_date as date,
    original_product_id as Identifier,
    metadata as metadata,
    spatial_coverage as wkt_geometry,
    op.cloud_cover as cloud_cover,
	dit.keywords as keywords,
	ds.name as title,
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
	GIP.band_count as band
	FROM public.catalogue_genericproduct as GP
	join public.dictionaries_projection as dp on gp.projection_id = dp.id
	join public.catalogue_genericimageryproduct as GIP on gp.id = gip.genericproduct_ptr_id
	join public.catalogue_opticalproduct as OP on gp.id = op.genericsensorproduct_ptr_id
	join public.catalogue_genericsensorproduct as GSP on gsp.genericimageryproduct_ptr_id = gp.id
	join public.dictionaries_opticalproductprofile OPP on opp.id = op.product_profile_id
	join public.dictionaries_instrumenttype as dit ON dit.id = opp.satellite_instrument_id
	join public.dictionaries_satelliteinstrumentgroup as dsig ON dit.id = dsig.instrument_type_id
	join public.dictionaries_satellite as ds on ds.id = dsig.satellite_id
	join public.dictionaries_license as dl on ds.license_type_id = dl.id
	)
	c.id AS identifier,
           ds.name AS dataset_name,
           'csw:Record' AS typename,
           'http://www.isotc211.org/2005/gmd' AS schema,
           'local' AS mdsource,
           c.insert_date AS insert_date,
           NULL AS xml,
           NULL AS metadata,
           NULL AS metadata_type,
           dit.keywords AS anytext,
           'EN' AS language,
           c.title AS title,
           c.abstract AS abstract,
           c.keywords AS keywords,
           NULL AS keywordstype,
        --    NULL AS format,
           NULL AS source,
           c.date_creation AS date_modified,
           'http://purl.org/dc/dcmitype/Dataset' AS type,

           ST_AsText(ST_GeomFromGeoJSON(c.wkt_geometry)) AS wkt_geometry,
           c.wkt_geometry::geometry(Polygon, 4326) AS wkb_geometry,
           concat_ws('', 'EPSG:', c.projection) AS crs,
           concat_ws(' ', c.title, c.identifier) AS title_alternate,
           c.extras->>'doi' AS doi,
           NULL as date_revision,
           c.date_creation AS date_creation,
           NULL AS date_publication,
           'South African National Space Agency (SANSA)' AS organisation,
           NULL AS securityconstraints,
           NULL AS parentidentifier,
           'Imagery, Basemaps, Earth Cover' AS topiccategory,
           'Satellite Imagery' AS sasditheme,
           c.extras->>'dataset_language' AS resourcelanguage,
           NULL AS geodescode,
           NULL AS denominator,
           NULL AS distancevalue,
           NULL AS distanceuom,
           c.date_creation AS date,
           c.time_begin as time_begin,
	       c.time_end as time_end,
           'Creation' AS reference_date_type,
           'SANS1878' AS metadata_standard,
           '1' AS metadata_standard_version,
           'utf8' AS dataset_character_set,
           'utf8' AS metadata_character_set,
           c.date_creation AS stamp_date,
           'Creation' AS stamp_date_type,
           NULL AS servicetype,
           NULL AS servicetypeversion,
           NULL AS operation,
           NULL AS couplingtype,
           NULL AS operateson,
           NULL AS operatesonidentifier,
           NULL AS operatesonname,
           NULL AS degree,
           NULL AS accessconstraints,
           NULL AS otherconstraints,
           NULL AS classification,
           NULL AS conditionapplyingtoaccessanduse,
	       NULL AS edition,
           '' AS lineage_statement,
           NULL AS responsiblepartyrole,
           NULL AS specificationtitle,
           NULL AS specificationdate,
           NULL AS specificationdatetype,
           c.author AS creator,
           c.maintainer AS publisher,
           NULL AS contributor,
           NULL AS relation,
           NULL AS platform,
           c.instrument as instrument,
           c.sensortype as sensortype,
           c.cloud_cover as cloudcover,
           c.band AS bands
           -- contact
           'SANSA Earth Observation' AS contact_individual_name,
           'SANSA Team' AS contact_position_name,
           'Customer Services' AS contact_organisational_role,
           NULL AS contact_delivery_point,
           'Pretoria' AS contact_address_city,
           'Gauteng' AS contact_address_administrative_area,
           '0127' AS contact_postal_code,
           'earthobservation@sansa.org.za' AS contact_electronic_mail_address,
           '012 844-0500' AS contact_phone,
           '012 844-0396' AS contact_facsimile,
            -- responsible party
           NULL AS responsible_party_individual_name,
           NULL AS responsible_party_position_name,
           NULL AS responsible_party_organisational_role,
           NULL AS responsible_party_contact_delivery_point,
           NULL AS responsible_party_contact_address_city,
           NULL AS responsible_party_contact_address_administrative_area,
           NULL AS responsible_party_contact_postal_code,
           NULL AS responsible_party_contact_electronic_mail_address,
           NULL AS responsible_party_contact_phone,
           NULL AS responsible_party_contact_facsimile,
           -- distribution_format
           NULL AS format,
           '1' AS version,

           -- metadata online resource
           NULL AS online_resource_linkage,
           NULL AS online_resource_name,
           NULL AS online_resource_application_profile,
           NULL AS online_resource_description,


           -- spatial and equivalent scale
           cast(c.wkt_geometry as json) AS bounding_geojson,
           NULL AS equivalent_scale,
           NULL AS reference_systems_additional_info
           --links
	FROM catalogue_extras AS c
	WITH DATA;
