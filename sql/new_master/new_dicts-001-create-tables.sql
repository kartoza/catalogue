BEGIN;
CREATE TABLE "dictionaries_productprofile_spectral_mode" (
    "id" serial NOT NULL PRIMARY KEY,
    "productprofile_id" integer NOT NULL,
    "spectralmode_id" integer NOT NULL,
    UNIQUE ("productprofile_id", "spectralmode_id")
)
;
CREATE TABLE "dictionaries_productprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "satellite_instrument_id" integer NOT NULL
)
;
ALTER TABLE "dictionaries_productprofile_spectral_mode" ADD CONSTRAINT "productprofile_id_refs_id_6754253a" FOREIGN KEY ("productprofile_id") REFERENCES "dictionaries_productprofile" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "dictionaries_processinglevel" (
    "id" serial NOT NULL PRIMARY KEY,
    "abbreviation" varchar(4) NOT NULL UNIQUE,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "precursor_processing_level_id" integer
)
;
ALTER TABLE "dictionaries_processinglevel" ADD CONSTRAINT "precursor_processing_level_id_refs_id_53b80553" FOREIGN KEY ("precursor_processing_level_id") REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED;
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
    "revist_time_days" integer,
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
    "scanner_type_id" integer NOT NULL REFERENCES "dictionaries_scannertype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "base_processing_level_id" integer NOT NULL REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "reference_system" varchar(255),
    "swath_optical_km" integer,
    "band_number_total" integer,
    "band_type" text,
    "spectral_range" varchar(100),
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
    "wavelength" integer NOT NULL,
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
    "approximate_resolution" double precision NOT NULL,
    "swath_width_km" double precision NOT NULL,
    "number_of_looks" integer NOT NULL,
    "polarization" varchar(2) NOT NULL
)
;
CREATE TABLE "dictionaries_satelliteinstrument" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "satellite_id" integer NOT NULL REFERENCES "dictionaries_satellite" ("id") DEFERRABLE INITIALLY DEFERRED,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("operator_abbreviation", "satellite_id", "instrument_type_id")
)
;
ALTER TABLE "dictionaries_productprofile" ADD CONSTRAINT "satellite_instrument_id_refs_id_450b0348" FOREIGN KEY ("satellite_instrument_id") REFERENCES "dictionaries_satelliteinstrument" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "dictionaries_band" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "band_name" varchar(50) NOT NULL,
    "band_abbr" varchar(20) NOT NULL,
    "band_number" integer NOT NULL,
    "min_wavelength" integer NOT NULL,
    "max_wavelength" integer NOT NULL,
    "pixelsize_resampled" double precision NOT NULL,
    "pixelsize_acquired" double precision NOT NULL
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
ALTER TABLE "dictionaries_productprofile_spectral_mode" ADD CONSTRAINT "spectralmode_id_refs_id_f1507601" FOREIGN KEY ("spectralmode_id") REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED;
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
    "processinglevel_id" integer NOT NULL REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "operator_processing_level_name" varchar(50) NOT NULL,
    "operator_processing_level_abbreviation" varchar(4) NOT NULL
)
;
CREATE TABLE "dictionaries_spectralmodeprocessingcosts" (
    "id" serial NOT NULL PRIMARY KEY,
    "spectral_mode_id" integer NOT NULL REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "instrumenttypeprocessinglevel_id" integer NOT NULL REFERENCES "dictionaries_instrumenttypeprocessinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cost_per_scene" integer NOT NULL,
    "currency_abbr" varchar(12) NOT NULL
)
;
CREATE INDEX "dictionaries_productprofile_satellite_instrument_id" ON "dictionaries_productprofile" ("satellite_instrument_id");
CREATE INDEX "dictionaries_processinglevel_precursor_processing_level_id" ON "dictionaries_processinglevel" ("precursor_processing_level_id");
CREATE INDEX "dictionaries_collection_institution_id" ON "dictionaries_collection" ("institution_id");
CREATE INDEX "dictionaries_satellite_collection_id" ON "dictionaries_satellite" ("collection_id");
CREATE INDEX "dictionaries_satellite_license_type_id" ON "dictionaries_satellite" ("license_type_id");
CREATE INDEX "dictionaries_instrumenttype_scanner_type_id" ON "dictionaries_instrumenttype" ("scanner_type_id");
CREATE INDEX "dictionaries_instrumenttype_base_processing_level_id" ON "dictionaries_instrumenttype" ("base_processing_level_id");
CREATE INDEX "dictionaries_imagingmode_radarbeam_id" ON "dictionaries_imagingmode" ("radarbeam_id");
CREATE INDEX "dictionaries_satelliteinstrument_satellite_id" ON "dictionaries_satelliteinstrument" ("satellite_id");
CREATE INDEX "dictionaries_satelliteinstrument_instrument_type_id" ON "dictionaries_satelliteinstrument" ("instrument_type_id");
CREATE INDEX "dictionaries_band_instrument_type_id" ON "dictionaries_band" ("instrument_type_id");
CREATE INDEX "dictionaries_spectralmode_instrument_type_id" ON "dictionaries_spectralmode" ("instrument_type_id");
CREATE INDEX "dictionaries_spectralmode_spectralgroup_id" ON "dictionaries_spectralmode" ("spectralgroup_id");
CREATE INDEX "dictionaries_bandspectralmode_band_id" ON "dictionaries_bandspectralmode" ("band_id");
CREATE INDEX "dictionaries_bandspectralmode_spectral_mode_id" ON "dictionaries_bandspectralmode" ("spectral_mode_id");
CREATE INDEX "dictionaries_instrumenttypeprocessinglevel_instrument_type_id" ON "dictionaries_instrumenttypeprocessinglevel" ("instrument_type_id");
CREATE INDEX "dictionaries_instrumenttypeprocessinglevel_processinglevel_id" ON "dictionaries_instrumenttypeprocessinglevel" ("processinglevel_id");
CREATE INDEX "dictionaries_spectralmodeprocessingcosts_spectral_mode_id" ON "dictionaries_spectralmodeprocessingcosts" ("spectral_mode_id");
CREATE INDEX "dictionaries_spectralmodeprocessingcosts_instrumenttypeprocb4fb" ON "dictionaries_spectralmodeprocessingcosts" ("instrumenttypeprocessinglevel_id");
COMMIT;