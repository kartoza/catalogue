#!/bin/bash
python manage.py dumpdata --indent=4 --database default catalogue.Collection > catalogue/fixtures/test_collection.json
python manage.py dumpdata --indent=4 --database default catalogue.Satellite > catalogue/fixtures/test_satellite.json
python manage.py dumpdata --indent=4 --database default catalogue.ScannerType > catalogue/fixtures/testscanner_type.json_
python manage.py dumpdata --indent=4 --database default catalogue.InstrumentType > catalogue/fixtures/test_instrument_type.json
python manage.py dumpdata --indent=4 --database default catalogue.RadarBeam > catalogue/fixtures/test_radar_beam.json_
python manage.py dumpdata --indent=4 --database default catalogue.ImagingMode > catalogue/fixtures/test_imagingmode.json
python manage.py dumpdata --indent=4 --database default catalogue.SatelliteInstrument > catalogue/fixtures/test_satelliteinstrument.json
python manage.py dumpdata --indent=4 --database default catalogue.Band > catalogue/fixtures/test_band.json
python manage.py dumpdata --indent=4 --database default catalogue.SpectralMode > catalogue/fixtures/test_spectral_mode.json
python manage.py dumpdata --indent=4 --database default catalogue.BandSpectral > catalogue/fixtures/test_band_spectral_mode.json

