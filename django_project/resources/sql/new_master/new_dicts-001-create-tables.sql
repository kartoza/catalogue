BEGIN;
CREATE TABLE "dictionaries_opticalproductprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "satellite_instrument_id" integer NOT NULL,
    "spectral_mode_id" integer NOT NULL
)
;
CREATE TABLE "dictionaries_radarproductprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "satellite_instrument_id" integer NOT NULL,
    "imaging_mode_id" integer NOT NULL
)
;
CREATE TABLE "dictionaries_processinglevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "abbreviation" varchar(4) NOT NULL UNIQUE,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL
)
;
CREATE TABLE "dictionaries_collection" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "institution_id" integer NOT NULL REFERENCES "catalogue_institution" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "dictionaries_satellite" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "collection_id" integer NOT NULL REFERENCES "dictionaries_collection" ("id") DEFERRABLE INITIALLY DEFERRED,
    "launch_date" date,
    "status" text,
    "altitude_km" integer,
    "orbit" text,
    "revisit_time_days" integer,
    "reference_url" varchar(200),
    "license_type_id" integer NOT NULL REFERENCES "catalogue_license" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "dictionaries_scannertype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE
)
;
CREATE TABLE "dictionaries_instrumenttype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "is_radar" boolean NOT NULL,
    "is_taskable" boolean NOT NULL,
    "is_searchable" boolean NOT NULL,
    "scanner_type_id" integer NOT NULL REFERENCES "dictionaries_scannertype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "base_processing_level_id" integer REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "default_processing_level_id" integer REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "reference_system_id" integer,
    "swath_optical_km" integer,
    "band_count" integer,
    "band_type" text,
    "spectral_range_list_nm" varchar(100),
    "pixel_size_list_m" varchar(100),
    "spatial_resolution_range" varchar(255),
    "quantization_bits" integer,
    "image_size_km" varchar(255),
    "processing_software" varchar(255),
    "keywords" varchar(255)
)
;
CREATE TABLE "dictionaries_radarbeam" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL UNIQUE REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "band_name" varchar(50) NOT NULL,
    "wavelength_cm" integer NOT NULL,
    "looking_distance" varchar(50) NOT NULL,
    "azimuth_direction" varchar(50) NOT NULL
)
;
CREATE TABLE "dictionaries_imagingmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "radarbeam_id" integer NOT NULL REFERENCES "dictionaries_radarbeam" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(50) NOT NULL,
    "incidence_angle_min" double precision NOT NULL,
    "incidence_angle_max" double precision NOT NULL,
    "approximate_resolution_m" double precision NOT NULL,
    "swath_width_km" double precision NOT NULL,
    "number_of_looks" integer NOT NULL,
    "polarization" varchar(2) NOT NULL
)
;
ALTER TABLE "dictionaries_radarproductprofile" ADD CONSTRAINT "imaging_mode_id_refs_id_6bd187aa" FOREIGN KEY ("imaging_mode_id") REFERENCES "dictionaries_imagingmode" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "dictionaries_satelliteinstrumentgroup" (
    "id" serial NOT NULL PRIMARY KEY,
    "satellite_id" integer NOT NULL REFERENCES "dictionaries_satellite" ("id") DEFERRABLE INITIALLY DEFERRED,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("satellite_id", "instrument_type_id")
)
;
CREATE TABLE "dictionaries_satelliteinstrument" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "satellite_instrument_group_id" integer NOT NULL REFERENCES "dictionaries_satelliteinstrumentgroup" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "dictionaries_opticalproductprofile" ADD CONSTRAINT "satellite_instrument_id_refs_id_628fdaa7" FOREIGN KEY ("satellite_instrument_id") REFERENCES "dictionaries_satelliteinstrument" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "dictionaries_radarproductprofile" ADD CONSTRAINT "satellite_instrument_id_refs_id_d777b7b1" FOREIGN KEY ("satellite_instrument_id") REFERENCES "dictionaries_satelliteinstrument" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "dictionaries_band" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "band_name" varchar(50) NOT NULL,
    "band_abbr" varchar(20) NOT NULL,
    "band_number" integer NOT NULL,
    "min_wavelength_nm" integer NOT NULL,
    "max_wavelength_nm" integer NOT NULL,
    "pixelsize_resampled_m" double precision NOT NULL,
    "pixelsize_acquired_m" double precision NOT NULL
)
;
CREATE TABLE "dictionaries_spectralgroup" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE
)
;
CREATE TABLE "dictionaries_spectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "spectralgroup_id" integer NOT NULL REFERENCES "dictionaries_spectralgroup" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "dictionaries_opticalproductprofile" ADD CONSTRAINT "spectral_mode_id_refs_id_8e2ff98f" FOREIGN KEY ("spectral_mode_id") REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "dictionaries_bandspectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "band_id" integer NOT NULL REFERENCES "dictionaries_band" ("id") DEFERRABLE INITIALLY DEFERRED,
    "spectral_mode_id" integer NOT NULL REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("band_id", "spectral_mode_id")
)
;
CREATE TABLE "dictionaries_instrumenttypeprocessinglevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "processing_level_id" integer NOT NULL REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "operator_processing_level_name" varchar(50) NOT NULL,
    "operator_processing_level_abbreviation" varchar(4) NOT NULL
)
;
CREATE TABLE "dictionaries_spectralmodeprocessingcosts" (
    "id" serial NOT NULL PRIMARY KEY,
    "spectral_mode_id" integer NOT NULL REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "instrument_type_processing_level_id" integer NOT NULL REFERENCES "dictionaries_instrumenttypeprocessinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cost_per_scene" numeric(10, 2) NOT NULL,
    "currency_id" integer,
    "cost_per_square_km" numeric(10, 2),
    "minimum_square_km" double precision,
    "sales_region_id" integer NOT NULL
)
;
CREATE TABLE "dictionaries_referencesystem" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL
)
;
ALTER TABLE "dictionaries_instrumenttype" ADD CONSTRAINT "reference_system_id_refs_id_4dbfe45f" FOREIGN KEY ("reference_system_id") REFERENCES "dictionaries_referencesystem" ("id") DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE "dictionaries_salesregion" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "abbreviation" varchar(4) NOT NULL
)
;
ALTER TABLE "dictionaries_spectralmodeprocessingcosts" ADD CONSTRAINT "sales_region_id_refs_id_79172456" FOREIGN KEY ("sales_region_id") REFERENCES "dictionaries_salesregion" ("id") DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE "dictionaries_subsidytype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "abbreviation" varchar(10) NOT NULL
)
;
CREATE TABLE "dictionaries_productprocessstate" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(30) NOT NULL
)
;


CREATE INDEX "dictionaries_opticalproductprofile_satellite_instrument_id" ON "dictionaries_opticalproductprofile" ("satellite_instrument_id");
CREATE INDEX "dictionaries_opticalproductprofile_spectral_mode_id" ON "dictionaries_opticalproductprofile" ("spectral_mode_id");
CREATE INDEX "dictionaries_radarproductprofile_satellite_instrument_id" ON "dictionaries_radarproductprofile" ("satellite_instrument_id");
CREATE INDEX "dictionaries_radarproductprofile_imaging_mode_id" ON "dictionaries_radarproductprofile" ("imaging_mode_id");
CREATE INDEX "dictionaries_processinglevel_abbreviation_like" ON "dictionaries_processinglevel" ("abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_processinglevel_name_like" ON "dictionaries_processinglevel" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_collection_name_like" ON "dictionaries_collection" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_collection_institution_id" ON "dictionaries_collection" ("institution_id");
CREATE INDEX "dictionaries_satellite_name_like" ON "dictionaries_satellite" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_satellite_abbreviation_like" ON "dictionaries_satellite" ("abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_satellite_operator_abbreviation_like" ON "dictionaries_satellite" ("operator_abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_satellite_collection_id" ON "dictionaries_satellite" ("collection_id");
CREATE INDEX "dictionaries_satellite_license_type_id" ON "dictionaries_satellite" ("license_type_id");
CREATE INDEX "dictionaries_scannertype_name_like" ON "dictionaries_scannertype" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_scannertype_abbreviation_like" ON "dictionaries_scannertype" ("abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_instrumenttype_name_like" ON "dictionaries_instrumenttype" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_instrumenttype_abbreviation_like" ON "dictionaries_instrumenttype" ("abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_instrumenttype_operator_abbreviation_like" ON "dictionaries_instrumenttype" ("operator_abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_instrumenttype_scanner_type_id" ON "dictionaries_instrumenttype" ("scanner_type_id");
CREATE INDEX "dictionaries_instrumenttype_base_processing_level_id" ON "dictionaries_instrumenttype" ("base_processing_level_id");
CREATE INDEX "dictionaries_instrumenttype_default_processing_level_id" ON "dictionaries_instrumenttype" ("default_processing_level_id");
CREATE INDEX "dictionaries_instrumenttype_reference_system_id" ON "dictionaries_instrumenttype" ("reference_system_id");
CREATE INDEX "dictionaries_imagingmode_radarbeam_id" ON "dictionaries_imagingmode" ("radarbeam_id");
CREATE INDEX "dictionaries_satelliteinstrumentgroup_satellite_id" ON "dictionaries_satelliteinstrumentgroup" ("satellite_id");
CREATE INDEX "dictionaries_satelliteinstrumentgroup_instrument_type_id" ON "dictionaries_satelliteinstrumentgroup" ("instrument_type_id");
CREATE INDEX "dictionaries_satelliteinstrument_name_like" ON "dictionaries_satelliteinstrument" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_satelliteinstrument_abbreviation_like" ON "dictionaries_satelliteinstrument" ("abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_satelliteinstrument_operator_abbreviation_like" ON "dictionaries_satelliteinstrument" ("operator_abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_satelliteinstrument_satellite_instrument_group_id" ON "dictionaries_satelliteinstrument" ("satellite_instrument_group_id");
CREATE INDEX "dictionaries_band_instrument_type_id" ON "dictionaries_band" ("instrument_type_id");
CREATE INDEX "dictionaries_spectralgroup_name_like" ON "dictionaries_spectralgroup" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_spectralgroup_abbreviation_like" ON "dictionaries_spectralgroup" ("abbreviation" varchar_pattern_ops);
CREATE INDEX "dictionaries_spectralmode_name_like" ON "dictionaries_spectralmode" ("name" varchar_pattern_ops);
CREATE INDEX "dictionaries_spectralmode_instrument_type_id" ON "dictionaries_spectralmode" ("instrument_type_id");
CREATE INDEX "dictionaries_spectralmode_spectralgroup_id" ON "dictionaries_spectralmode" ("spectralgroup_id");
CREATE INDEX "dictionaries_bandspectralmode_band_id" ON "dictionaries_bandspectralmode" ("band_id");
CREATE INDEX "dictionaries_bandspectralmode_spectral_mode_id" ON "dictionaries_bandspectralmode" ("spectral_mode_id");
CREATE INDEX "dictionaries_instrumenttypeprocessinglevel_instrument_type_id" ON "dictionaries_instrumenttypeprocessinglevel" ("instrument_type_id");
CREATE INDEX "dictionaries_instrumenttypeprocessinglevel_processinglevel_id" ON "dictionaries_instrumenttypeprocessinglevel" ("processing_level_id");
CREATE INDEX "dictionaries_spectralmodeprocessingcosts_spectral_mode_id" ON "dictionaries_spectralmodeprocessingcosts" ("spectral_mode_id");
CREATE INDEX "dictionaries_spectralmodeprocessingcosts_instrumenttypeprocb4fb" ON "dictionaries_spectralmodeprocessingcosts" ("instrument_type_processing_level_id");
CREATE INDEX "dictionaries_spectralmodeprocessingcosts_currency_id" ON "dictionaries_spectralmodeprocessingcosts" ("currency_id");
CREATE INDEX "dictionaries_referencesystem_name_like" ON "dictionaries_referencesystem" ("name" varchar_pattern_ops);

COMMIT;
