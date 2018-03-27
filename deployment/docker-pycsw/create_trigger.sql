CREATE OR REPLACE FUNCTION insert_pycsw_catalogue_on_cbers()
RETURNS TRIGGER AS $pycsw_cbers_inserted$
DECLARE
	_keywords	varchar(255);
	_name		varchar(255);
	_launch_date	varchar(255);
	_description	varchar(255);
	_ref_url	varchar(255);
BEGIN
	SELECT
		dit.keywords, ds.name, ds.launch_date, ds.description, ds.reference_url
	INTO
		_keywords, _name, _launch_date, _description, _ref_url
	FROM
		dictionaries_satellite ds
	JOIN
		dictionaries_satelliteinstrumentgroup dsig
		ON ds.id = dsig.satellite_id
	JOIN
		dictionaries_instrumenttype dit
		ON dit.id = dsig.instrument_type_id
	WHERE
		dit.abbreviation = NEW.sensor_abbreviation
		AND
		ds.abbreviation = NEW.satellite_abbreviation;

    IF (TG_OP = 'INSERT') THEN
	INSERT INTO pycsw_catalogue
		(identifier, typename, schema,  mdsource, insert_date,
		xml, anytext, language, title_alternate,
		type, keywordstype, parentidentifier,
		relation, time_begin, time_end, topicategory, resourcelanguage,
		creator, publisher, contributor, organization, securityconstraints,
		accessconstraints, otherconstraints, date, date_revision,
		date_publication, date_modified, format, source, crs,
		geodescode, denominator, distancevalue, distanceuom, wkt_geometry,
		servicetype, servicetypeversion, operation, couplingtype, operateson,
		operatesonidentifier, operatesoname, degree, classification, conditionapplyingtoaccessanduse,
		lineage, responsiblepartyrole, specificationtitle, specificationdate, specificationdatetype,
		keywords, title, date_creation, abstract, links)
	VALUES
		(NEW.identifier, NEW.type_name, NEW.schema, NEW.mdsource, NEW.insert_date,
		NEW.xml, NEW.any_text, NEW.language, NEW.alternate_title,
		NEW.any_text, NEW.keyword_type, NEW.parent_identifier,
		NEW.relation, NEW.temp_extent_begin, NEW.temp_extent_end, NEW.topic_category, NEW.resource_language,
		NEW.creator, NEW.publisher, NEW.contributor, NEW.organization_name, NEW.security_constraints,
		NEW.access_constraints, NEW.other_constraints, NEW.date, NEW.revision_date,
		to_char(now(), 'YYYY-MM-DD'), NEW.modified_date, NEW.format, NEW.source, NEW.crs,
		NEW.geographic_description_code, NEW.denominator, NEW.distance_value, NEW.distance_uom, NEW.bounding_box,
		NEW.service_type, NEW.service_type_version, NEW.operation, NEW.coupling_type, NEW.operates_on,
		NEW.operates_on_identifier, NEW.operates_on_name, NEW.degree, NEW.classification, NEW.condition_applying_to_access_and_use,
		NEW.lineage, NEW.responsible_party_role, NEW.specification_title, '', NEW.specification_date_type,
		_keywords, _name, _launch_date, _description, _ref_url);
   END IF;
   if (TG_OP='UPDATE') THEN
	UPDATE pycsw_catalogue
	SET
		(typename, schema,  mdsource, insert_date,
		xml, anytext, language, title, title_alternate,
		type, abstract, keywords, keywordstype, parentidentifier,
		relation, time_begin, time_end, topicategory, resourcelanguage,
		creator, publisher, contributor, organization, securityconstraints,
		accessconstraints, otherconstraints, date, date_revision, date_creation,
		date_publication, date_modified, format, source, crs,
		geodescode, denominator, distancevalue, distanceuom, wkt_geometry,
		servicetype, servicetypeversion, operation, couplingtype, operateson,
		operatesonidentifier, operatesoname, degree, classification, conditionapplyingtoaccessanduse,
		lineage, responsiblepartyrole, specificationtitle, specificationdate, specificationdatetype, links)
	=
		(NEW.type_name, NEW.schema, NEW.mdsource, NEW.insert_date,
		NEW.xml, NEW.any_text, NEW.language, _name, NEW.alternate_title,
		NEW.any_text, _description, _keywords, NEW.keyword_type, NEW.parent_identifier,
		NEW.relation, NEW.temp_extent_begin, NEW.temp_extent_end, NEW.topic_category, NEW.resource_language,
		NEW.creator, NEW.publisher, NEW.contributor, NEW.organization_name, NEW.security_constraints,
		NEW.access_constraints, NEW.other_constraints, NEW.date, NEW.revision_date, _launch_date,
		NEW.publication_date, NEW.modified_date, NEW.format, NEW.source, NEW.crs,
		NEW.geographic_description_code, NEW.denominator, NEW.distance_value, NEW.distance_uom, NEW.bounding_box,
		NEW.service_type, NEW.service_type_version, NEW.operation, NEW.coupling_type, NEW.operates_on,
		NEW.operates_on_identifier, NEW.operates_on_name, NEW.degree, NEW.classification, NEW.condition_applying_to_access_and_use,
		NEW.lineage, NEW.responsible_party_role, NEW.specification_title, '', NEW.specification_date_type, _ref_url)
		where identifier = NEW.identifier;
   END IF;
   RETURN new;
END;
$pycsw_cbers_inserted$ LANGUAGE plpgsql;


CREATE TRIGGER insert_pycsw_catalogue_cbers
	AFTER INSERT OR UPDATE on catalogue_pycswextrafields
	FOR EACH ROW EXECUTE PROCEDURE insert_pycsw_catalogue_on_cbers();