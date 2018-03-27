-- Table: public.pycsw_catalogue

-- DROP TABLE public.pycsw_catalogue;

CREATE TABLE public.pycsw_catalogue
(
--  id serial primary key,
--  identifier text NOT NULL references catalogue_pycswcbers(identifier),
  identifier text primary key,
  typename text NOT NULL,
  schema text NOT NULL,
  mdsource text NOT NULL,
  insert_date text NOT NULL,
  xml text NOT NULL,
  anytext text NOT NULL,
  language text,
  title text,
  title_alternate text,
  type text,
  abstract text,
  keywords text,
  keywordstype text,
  parentidentifier text,
  relation text,
  time_begin text,
  time_end text,
  topicategory text,
  resourcelanguage text,
  creator text,
  publisher text,
  contributor text,
  organization text,
  securityconstraints text,
  accessconstraints text,
  otherconstraints text,
  date text,
  date_revision text,
  date_creation text,
  date_publication text,
  date_modified text,
  format text,
  source text,
  crs text,
  geodescode text,
  denominator text,
  distancevalue text,
  distanceuom text,
  wkt_geometry text,
  servicetype text,
  servicetypeversion text,
  operation text,
  couplingtype text,
  operateson text,
  operatesonidentifier text,
  operatesoname text,
  degree text,
  classification text,
  conditionapplyingtoaccessanduse text,
  lineage text,
  responsiblepartyrole text,
  specificationtitle text,
  specificationdate text,
  specificationdatetype text,
  links text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.pycsw_catalogue
  OWNER TO docker;

-- Index: public.ix_pycsw_catalogue_abstract

-- DROP INDEX public.ix_pycsw_catalogue_abstract;

CREATE INDEX ix_pycsw_catalogue_abstract
  ON public.pycsw_catalogue
  USING btree
  (abstract COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_accessconstraints

-- DROP INDEX public.ix_pycsw_catalogue_accessconstraints;

CREATE INDEX ix_pycsw_catalogue_accessconstraints
  ON public.pycsw_catalogue
  USING btree
  (accessconstraints COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_classification

-- DROP INDEX public.ix_pycsw_catalogue_classification;

CREATE INDEX ix_pycsw_catalogue_classification
  ON public.pycsw_catalogue
  USING btree
  (classification COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_conditionapplyingtoaccessanduse

-- DROP INDEX public.ix_pycsw_catalogue_conditionapplyingtoaccessanduse;

CREATE INDEX ix_pycsw_catalogue_conditionapplyingtoaccessanduse
  ON public.pycsw_catalogue
  USING btree
  (conditionapplyingtoaccessanduse COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_contributor

-- DROP INDEX public.ix_pycsw_catalogue_contributor;

CREATE INDEX ix_pycsw_catalogue_contributor
  ON public.pycsw_catalogue
  USING btree
  (contributor COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_couplingtype

-- DROP INDEX public.ix_pycsw_catalogue_couplingtype;

CREATE INDEX ix_pycsw_catalogue_couplingtype
  ON public.pycsw_catalogue
  USING btree
  (couplingtype COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_creator

-- DROP INDEX public.ix_pycsw_catalogue_creator;

CREATE INDEX ix_pycsw_catalogue_creator
  ON public.pycsw_catalogue
  USING btree
  (creator COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_crs

-- DROP INDEX public.ix_pycsw_catalogue_crs;

CREATE INDEX ix_pycsw_catalogue_crs
  ON public.pycsw_catalogue
  USING btree
  (crs COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_date

-- DROP INDEX public.ix_pycsw_catalogue_date;

CREATE INDEX ix_pycsw_catalogue_date
  ON public.pycsw_catalogue
  USING btree
  (date COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_date_creation

-- DROP INDEX public.ix_pycsw_catalogue_date_creation;

CREATE INDEX ix_pycsw_catalogue_date_creation
  ON public.pycsw_catalogue
  USING btree
  (date_creation COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_date_modified

-- DROP INDEX public.ix_pycsw_catalogue_date_modified;

CREATE INDEX ix_pycsw_catalogue_date_modified
  ON public.pycsw_catalogue
  USING btree
  (date_modified COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_date_publication

-- DROP INDEX public.ix_pycsw_catalogue_date_publication;

CREATE INDEX ix_pycsw_catalogue_date_publication
  ON public.pycsw_catalogue
  USING btree
  (date_publication COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_date_revision

-- DROP INDEX public.ix_pycsw_catalogue_date_revision;

CREATE INDEX ix_pycsw_catalogue_date_revision
  ON public.pycsw_catalogue
  USING btree
  (date_revision COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_degree

-- DROP INDEX public.ix_pycsw_catalogue_degree;

CREATE INDEX ix_pycsw_catalogue_degree
  ON public.pycsw_catalogue
  USING btree
  (degree COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_denominator

-- DROP INDEX public.ix_pycsw_catalogue_denominator;

CREATE INDEX ix_pycsw_catalogue_denominator
  ON public.pycsw_catalogue
  USING btree
  (denominator COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_distanceuom

-- DROP INDEX public.ix_pycsw_catalogue_distanceuom;

CREATE INDEX ix_pycsw_catalogue_distanceuom
  ON public.pycsw_catalogue
  USING btree
  (distanceuom COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_distancevalue

-- DROP INDEX public.ix_pycsw_catalogue_distancevalue;

CREATE INDEX ix_pycsw_catalogue_distancevalue
  ON public.pycsw_catalogue
  USING btree
  (distancevalue COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_format

-- DROP INDEX public.ix_pycsw_catalogue_format;

CREATE INDEX ix_pycsw_catalogue_format
  ON public.pycsw_catalogue
  USING btree
  (format COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_geodescode

-- DROP INDEX public.ix_pycsw_catalogue_geodescode;

CREATE INDEX ix_pycsw_catalogue_geodescode
  ON public.pycsw_catalogue
  USING btree
  (geodescode COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_insert_date

-- DROP INDEX public.ix_pycsw_catalogue_insert_date;

CREATE INDEX ix_pycsw_catalogue_insert_date
  ON public.pycsw_catalogue
  USING btree
  (insert_date COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_keywords

-- DROP INDEX public.ix_pycsw_catalogue_keywords;

CREATE INDEX ix_pycsw_catalogue_keywords
  ON public.pycsw_catalogue
  USING btree
  (keywords COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_keywordstype

-- DROP INDEX public.ix_pycsw_catalogue_keywordstype;

CREATE INDEX ix_pycsw_catalogue_keywordstype
  ON public.pycsw_catalogue
  USING btree
  (keywordstype COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_language

-- DROP INDEX public.ix_pycsw_catalogue_language;

CREATE INDEX ix_pycsw_catalogue_language
  ON public.pycsw_catalogue
  USING btree
  (language COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_lineage

-- DROP INDEX public.ix_pycsw_catalogue_lineage;

CREATE INDEX ix_pycsw_catalogue_lineage
  ON public.pycsw_catalogue
  USING btree
  (lineage COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_links

-- DROP INDEX public.ix_pycsw_catalogue_links;

CREATE INDEX ix_pycsw_catalogue_links
  ON public.pycsw_catalogue
  USING btree
  (links COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_mdsource

-- DROP INDEX public.ix_pycsw_catalogue_mdsource;

CREATE INDEX ix_pycsw_catalogue_mdsource
  ON public.pycsw_catalogue
  USING btree
  (mdsource COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_operateson

-- DROP INDEX public.ix_pycsw_catalogue_operateson;

CREATE INDEX ix_pycsw_catalogue_operateson
  ON public.pycsw_catalogue
  USING btree
  (operateson COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_operatesoname

-- DROP INDEX public.ix_pycsw_catalogue_operatesoname;

CREATE INDEX ix_pycsw_catalogue_operatesoname
  ON public.pycsw_catalogue
  USING btree
  (operatesoname COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_operatesonidentifier

-- DROP INDEX public.ix_pycsw_catalogue_operatesonidentifier;

CREATE INDEX ix_pycsw_catalogue_operatesonidentifier
  ON public.pycsw_catalogue
  USING btree
  (operatesonidentifier COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_operation

-- DROP INDEX public.ix_pycsw_catalogue_operation;

CREATE INDEX ix_pycsw_catalogue_operation
  ON public.pycsw_catalogue
  USING btree
  (operation COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_organization

-- DROP INDEX public.ix_pycsw_catalogue_organization;

CREATE INDEX ix_pycsw_catalogue_organization
  ON public.pycsw_catalogue
  USING btree
  (organization COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_otherconstraints

-- DROP INDEX public.ix_pycsw_catalogue_otherconstraints;

CREATE INDEX ix_pycsw_catalogue_otherconstraints
  ON public.pycsw_catalogue
  USING btree
  (otherconstraints COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_parentidentifier

-- DROP INDEX public.ix_pycsw_catalogue_parentidentifier;

CREATE INDEX ix_pycsw_catalogue_parentidentifier
  ON public.pycsw_catalogue
  USING btree
  (parentidentifier COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_publisher

-- DROP INDEX public.ix_pycsw_catalogue_publisher;

CREATE INDEX ix_pycsw_catalogue_publisher
  ON public.pycsw_catalogue
  USING btree
  (publisher COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_relation

-- DROP INDEX public.ix_pycsw_catalogue_relation;

CREATE INDEX ix_pycsw_catalogue_relation
  ON public.pycsw_catalogue
  USING btree
  (relation COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_resourcelanguage

-- DROP INDEX public.ix_pycsw_catalogue_resourcelanguage;

CREATE INDEX ix_pycsw_catalogue_resourcelanguage
  ON public.pycsw_catalogue
  USING btree
  (resourcelanguage COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_responsiblepartyrole

-- DROP INDEX public.ix_pycsw_catalogue_responsiblepartyrole;

CREATE INDEX ix_pycsw_catalogue_responsiblepartyrole
  ON public.pycsw_catalogue
  USING btree
  (responsiblepartyrole COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_schema

-- DROP INDEX public.ix_pycsw_catalogue_schema;

CREATE INDEX ix_pycsw_catalogue_schema
  ON public.pycsw_catalogue
  USING btree
  (schema COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_securityconstraints

-- DROP INDEX public.ix_pycsw_catalogue_securityconstraints;

CREATE INDEX ix_pycsw_catalogue_securityconstraints
  ON public.pycsw_catalogue
  USING btree
  (securityconstraints COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_servicetype

-- DROP INDEX public.ix_pycsw_catalogue_servicetype;

CREATE INDEX ix_pycsw_catalogue_servicetype
  ON public.pycsw_catalogue
  USING btree
  (servicetype COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_servicetypeversion

-- DROP INDEX public.ix_pycsw_catalogue_servicetypeversion;

CREATE INDEX ix_pycsw_catalogue_servicetypeversion
  ON public.pycsw_catalogue
  USING btree
  (servicetypeversion COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_source

-- DROP INDEX public.ix_pycsw_catalogue_source;

CREATE INDEX ix_pycsw_catalogue_source
  ON public.pycsw_catalogue
  USING btree
  (source COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_specificationdate

-- DROP INDEX public.ix_pycsw_catalogue_specificationdate;

CREATE INDEX ix_pycsw_catalogue_specificationdate
  ON public.pycsw_catalogue
  USING btree
  (specificationdate COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_specificationdatetype

-- DROP INDEX public.ix_pycsw_catalogue_specificationdatetype;

CREATE INDEX ix_pycsw_catalogue_specificationdatetype
  ON public.pycsw_catalogue
  USING btree
  (specificationdatetype COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_specificationtitle

-- DROP INDEX public.ix_pycsw_catalogue_specificationtitle;

CREATE INDEX ix_pycsw_catalogue_specificationtitle
  ON public.pycsw_catalogue
  USING btree
  (specificationtitle COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_time_begin

-- DROP INDEX public.ix_pycsw_catalogue_time_begin;

CREATE INDEX ix_pycsw_catalogue_time_begin
  ON public.pycsw_catalogue
  USING btree
  (time_begin COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_time_end

-- DROP INDEX public.ix_pycsw_catalogue_time_end;

CREATE INDEX ix_pycsw_catalogue_time_end
  ON public.pycsw_catalogue
  USING btree
  (time_end COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_title

-- DROP INDEX public.ix_pycsw_catalogue_title;

CREATE INDEX ix_pycsw_catalogue_title
  ON public.pycsw_catalogue
  USING btree
  (title COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_title_alternate

-- DROP INDEX public.ix_pycsw_catalogue_title_alternate;

CREATE INDEX ix_pycsw_catalogue_title_alternate
  ON public.pycsw_catalogue
  USING btree
  (title_alternate COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_topicategory

-- DROP INDEX public.ix_pycsw_catalogue_topicategory;

CREATE INDEX ix_pycsw_catalogue_topicategory
  ON public.pycsw_catalogue
  USING btree
  (topicategory COLLATE pg_catalog."default");

-- Index: public.ix_pycsw_catalogue_type

-- DROP INDEX public.ix_pycsw_catalogue_type;

-- Index: public.ix_pycsw_catalogue_typename

-- DROP INDEX public.ix_pycsw_catalogue_typename;

CREATE INDEX ix_pycsw_catalogue_typename
  ON public.pycsw_catalogue
  USING btree
  (typename COLLATE pg_catalog."default");
