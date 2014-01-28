#!/bin/bash
python manage.py dumpdata --indent=4 --database default catalogue.Institution > catalogue/fixtures/test_institution.json
python manage.py dumpdata --indent=4 --database default catalogue.Collection > catalogue/fixtures/test_collection.json
python manage.py dumpdata --indent=4 --database default catalogue.Satellite > catalogue/fixtures/test_satellite.json
python manage.py dumpdata --indent=4 --database default catalogue.License > catalogue/fixtures/test_license.json
python manage.py dumpdata --indent=4 --database default catalogue.InstrumentType > catalogue/fixtures/test_instrument_type.json
python manage.py dumpdata --indent=4 --database default catalogue.ScannerType > catalogue/fixtures/testscanner_type.json_
python manage.py dumpdata --indent=4 --database default catalogue.SatelliteInstrumentGroup > catalogue/fixtures/testsatellite_instrument_group.json_
python manage.py dumpdata --indent=4 --database default catalogue.SatelliteInstrument > catalogue/fixtures/test_satelliteinstrument.json
python manage.py dumpdata --indent=4 --database default catalogue.RadarBeam > catalogue/fixtures/test_radar_beam.json_
python manage.py dumpdata --indent=4 --database default catalogue.ImagingMode > catalogue/fixtures/test_imagingmode.json
python manage.py dumpdata --indent=4 --database default catalogue.Band > catalogue/fixtures/test_band.json
python manage.py dumpdata --indent=4 --database default catalogue.SpectralMode > catalogue/fixtures/test_spectral_mode.json
python manage.py dumpdata --indent=4 --database default catalogue.BandSpectral > catalogue/fixtures/test_band_spectral_mode.json
python manage.py dumpdata --indent=4 --database default catalogue.SpectralGroup > catalogue/fixtures/test_spectral_group.json
python manage.py dumpdata --indent=4 --database default catalogue.ReferenceSystem > catalogue/fixtures/test_reference_system.json
python manage.py dumpdata --indent=4 --database default catalogue.ProcessingLevel > catalogue/fixtures/test_processing_level.json
python manage.py dumpdata --indent=4 --database default catalogue.InstrumentTypeProcessingLevel > catalogue/fixtures/test_instrument_type_processing_level.json
python manage.py dumpdata --indent=4 --database default catalogue.SpectralModeProcessingCosts > catalogue/fixtures/test_spectral_mode_processing_costs.json
python manage.py dumpdata --indent=4 --database default catalogue.ForeignCurrency > catalogue/fixtures/test_foreign_currency.json
python manage.py dumpdata --indent=4 --database default catalogue.OpticalProductProfile > catalogue/fixtures/test_optical_product_profile.json

