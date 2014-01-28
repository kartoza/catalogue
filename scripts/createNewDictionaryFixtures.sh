#!/bin/bash
python manage.py dumpdata --indent=4 --database default catalogue.Institution > catalogue/fixtures/institution.json
python manage.py dumpdata --indent=4 --database default catalogue.ProcessingLevel > catalogue/fixtures/processing_level.json
python manage.py dumpdata --indent=4 --database default catalogue.License > catalogue/fixtures/license.json
python manage.py dumpdata --indent=4 --database default dictionaries.Collection > dictionaries/fixtures/collection.json
python manage.py dumpdata --indent=4 --database default dictionaries.Satellite > dictionaries/fixtures/satellite.json
python manage.py dumpdata --indent=4 --database default dictionaries.InstrumentType > dictionaries/fixtures/instrument_type.json
python manage.py dumpdata --indent=4 --database default dictionaries.ScannerType > dictionaries/fixtures/scanner_type.json_
python manage.py dumpdata --indent=4 --database default dictionaries.SatelliteInstrumentGroup > dictionaries/fixtures/satellite_instrument_group.json_
python manage.py dumpdata --indent=4 --database default dictionaries.SatelliteInstrument > dictionaries/fixtures/satelliteinstrument.json
python manage.py dumpdata --indent=4 --database default dictionaries.RadarBeam > dictionaries/fixtures/radar_beam.json_
python manage.py dumpdata --indent=4 --database default dictionaries.ImagingMode > dictionaries/fixtures/imagingmode.json
python manage.py dumpdata --indent=4 --database default dictionaries.Band > dictionaries/fixtures/band.json
python manage.py dumpdata --indent=4 --database default dictionaries.SpectralMode > dictionaries/fixtures/spectral_mode.json
python manage.py dumpdata --indent=4 --database default dictionaries.BandSpectral > dictionaries/fixtures/band_spectral_mode.json
python manage.py dumpdata --indent=4 --database default dictionaries.SpectralGroup > dictionaries/fixtures/spectral_group.json
python manage.py dumpdata --indent=4 --database default dictionaries.ReferenceSystem > dictionaries/fixtures/reference_system.json
python manage.py dumpdata --indent=4 --database default dictionaries.InstrumentTypeProcessingLevel > dictionaries/fixtures/instrument_type_processing_level.json
python manage.py dumpdata --indent=4 --database default dictionaries.SpectralModeProcessingCosts > dictionaries/fixtures/spectral_mode_processing_costs.json
python manage.py dumpdata --indent=4 --database default dictionaries.ForeignCurrency > dictionaries/fixtures/foreign_currency.json
python manage.py dumpdata --indent=4 --database default dictionaries.OpticalProductProfile > dictionaries/fixtures/optical_product_profile.json

