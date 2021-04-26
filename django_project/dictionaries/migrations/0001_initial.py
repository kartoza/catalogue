# -*- coding: utf-8 -*-


from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band_name', models.CharField(max_length=50)),
                ('band_abbr', models.CharField(max_length=20, blank=True)),
                ('band_number', models.IntegerField(help_text=b'Instrument specific band number, e.g. 1,2, ...')),
                ('min_wavelength_nm', models.IntegerField(help_text=b'Lower band wavelength in nanometeres')),
                ('max_wavelength_nm', models.IntegerField(help_text=b'Upper band wavelength in nanometeres')),
                ('pixelsize_resampled_m', models.FloatField(help_text=b'Pixel size in m (resolution) resampled')),
                ('pixelsize_acquired_m', models.FloatField(help_text=b'Pixel size in m (resolution) acquired')),
            ],
            options={
                'ordering': ['instrument_type', 'band_name'],
            },
        ),
        migrations.CreateModel(
            name='BandSpectralMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band', models.ForeignKey(to='dictionaries.Band')),
            ],
            options={
                'ordering': ['band', 'spectral_mode'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Collection name as defined by operator.', unique=True, max_length=255, verbose_name=b'Collection name')),
                ('description', models.TextField(help_text=b'Detailed description for this collection', verbose_name=b'Collection description')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ImagingMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'ImagingMode name', max_length=50)),
                ('incidence_angle_min', models.FloatField(help_text=b'Minimum incidence angle')),
                ('incidence_angle_max', models.FloatField(help_text=b'Maximum incidence angle')),
                ('approximate_resolution_m', models.FloatField(help_text=b'Approximate ImagingMode resolution in meters')),
                ('swath_width_km', models.FloatField(help_text=b'Swath width in kilometres')),
                ('number_of_looks', models.IntegerField(help_text=b'REPLACE ME!')),
                ('polarization', models.CharField(help_text=b'Polarization type', max_length=2, choices=[(b'HH', b'Horizontal-Horizontal'), (b'HV', b'Horizontal-Vertical'), (b'VH', b'Vertical-Horizontal'), (b'VV', b'Vertical-Vertical')])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255)),
                ('address3', models.CharField(max_length=255)),
                ('post_code', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the instrument type.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(unique=True, max_length=20)),
                ('operator_abbreviation', models.CharField(help_text=b'Instrument abbreviation as named by satellite owning institution.', unique=True, max_length=255)),
                ('is_radar', models.BooleanField(default=False, help_text=b'Mark true if this sensor captures RADAR data.', verbose_name=b'Is this a RADAR sensor?')),
                ('is_taskable', models.BooleanField(default=False, help_text=b'Can this sensor be tasked?')),
                ('is_searchable', models.BooleanField(default=True, help_text=b'Can this sensor be searched?')),
                ('swath_optical_km', models.IntegerField(help_text=b'On-ground sensor swath width', null=True, blank=True)),
                ('band_count', models.IntegerField(help_text=b'Total number of bands for this Instrument', null=True, blank=True)),
                ('band_type', models.TextField(help_text=b'Semicolon delimited list of Instrument band types', null=True, blank=True)),
                ('spectral_range_list_nm', models.CharField(help_text=b'Semicolon delimited list of Instrument spectral ranges', max_length=100, null=True, blank=True)),
                ('pixel_size_list_m', models.CharField(help_text=b'Semicolon delimited list of Instrument pixel sizes', max_length=100, null=True, blank=True)),
                ('spatial_resolution_range', models.CharField(help_text=b'Semicolon delimited list of Instrument spatial resolutions', max_length=255, null=True, blank=True)),
                ('quantization_bits', models.IntegerField(help_text=b'Quantization bit rate - the aquisition bits per pixel for example 12 bit landsat 8. Note that products are likely delivered with a different bit depth to customers.', null=True, blank=True)),
                ('image_size_km', models.CharField(help_text=b'Human readable representation of image size', max_length=255, null=True, blank=True)),
                ('processing_software', models.CharField(help_text=b'Description of processing software', max_length=255, null=True, blank=True)),
                ('keywords', models.CharField(help_text=b'Keywords describing InstrumentType', max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InstrumentTypeProcessingLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator_processing_level_name', models.CharField(help_text=b'Operator original processing level name', max_length=50)),
                ('operator_processing_level_abbreviation', models.CharField(help_text=b'Operator original processing level abbreviation', max_length=4)),
                ('instrument_type', models.ForeignKey(to='dictionaries.InstrumentType')),
            ],
            options={
                'ordering': ['instrument_type', 'processing_level'],
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('details', models.TextField()),
                ('type', models.IntegerField(default=3, choices=[(1, b'Free'), (2, b'Government'), (3, b'Commercial')])),
            ],
        ),
        migrations.CreateModel(
            name='OpticalProductProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['satellite_instrument', 'spectral_mode'],
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(help_text=b'Place geometry', srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessingLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(unique=True, max_length=4)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the processing level.', verbose_name=b'Detailed description.')),
            ],
            options={
                'ordering': ['abbreviation'],
            },
        ),
        migrations.CreateModel(
            name='ProductProcessState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full name of a product process state', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('epsg_code', models.IntegerField(unique=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name=b'Name')),
            ],
            options={
                'ordering': ('epsg_code', 'name'),
                'verbose_name': 'Projection',
                'verbose_name_plural': 'Projections',
            },
        ),
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=b'255')),
            ],
            options={
                'verbose_name': 'Quality',
                'verbose_name_plural': 'Qualities',
            },
        ),
        migrations.CreateModel(
            name='RadarBeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band_name', models.CharField(help_text=b'RadarBeam band name', max_length=50)),
                ('wavelength_cm', models.IntegerField(help_text=b'Band wavelength in centimetres')),
                ('looking_distance', models.CharField(help_text=b'REPLACE ME!', max_length=50)),
                ('azimuth_direction', models.CharField(help_text=b'REPLACE ME!', max_length=50)),
                ('instrument_type', models.OneToOneField(to='dictionaries.InstrumentType')),
            ],
            options={
                'ordering': ['instrument_type'],
            },
        ),
        migrations.CreateModel(
            name='RadarProductProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imaging_mode', models.ForeignKey(to='dictionaries.ImagingMode')),
            ],
            options={
                'ordering': ['satellite_instrument', 'imaging_mode'],
            },
        ),
        migrations.CreateModel(
            name='ReferenceSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the reference system.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SalesRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full name of a sales region', max_length=50)),
                ('abbreviation', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the satellite.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(unique=True, max_length=20)),
                ('operator_abbreviation', models.CharField(help_text=b'Satellite abbreviation as named by satellite owning institution.', unique=True, max_length=255)),
                ('launch_date', models.DateField(help_text=b'Satellite launch date', null=True, blank=True)),
                ('status', models.TextField(help_text=b'Information about satellite operational status', null=True, blank=True)),
                ('altitude_km', models.IntegerField(help_text=b'Satellite altitude in kilometres', null=True, blank=True)),
                ('orbit', models.TextField(help_text=b'Satellite orbit description', null=True, blank=True)),
                ('revisit_time_days', models.IntegerField(help_text=b'Days elapsed between observations of the same point', null=True, blank=True)),
                ('reference_url', models.URLField(help_text=b'Satellite mission URL', null=True, blank=True)),
                ('collection', models.ForeignKey(to='dictionaries.Collection')),
                ('license_type', models.ForeignKey(help_text=b'Satellite product license type', to='dictionaries.License')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SatelliteInstrument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the satellite instrument.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(unique=True, max_length=20)),
                ('operator_abbreviation', models.CharField(help_text=b'Satellite abbreviation as named by satellite owning institution.', unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SatelliteInstrumentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument_type', models.ForeignKey(to='dictionaries.InstrumentType')),
                ('satellite', models.ForeignKey(to='dictionaries.Satellite')),
            ],
            options={
                'ordering': ['satellite', 'instrument_type'],
            },
        ),
        migrations.CreateModel(
            name='ScannerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the scanner type.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpectralGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the spectral mode.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'ordering': ['abbreviation', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SpectralMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'A detailed description of the spectral mode.', verbose_name=b'Detailed description.')),
                ('abbreviation', models.CharField(max_length=20)),
                ('instrument_type', models.ForeignKey(to='dictionaries.InstrumentType')),
                ('spectralgroup', models.ForeignKey(to='dictionaries.SpectralGroup')),
            ],
            options={
                'ordering': ['abbreviation', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SpectralModeProcessingCosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost_per_scene', models.DecimalField(help_text=b'Cost per scene', max_digits=10, decimal_places=2)),
                ('cost_per_square_km', models.DecimalField(help_text=b'Cost per square kilometre', null=True, max_digits=10, decimal_places=2, blank=True)),
                ('minimum_square_km', models.FloatField(help_text=b'Minimum number of square kilometers that can be ordered for aprice of per kilometer', null=True, blank=True)),
                ('currency', models.ForeignKey(blank=True, to='exchange.Currency', null=True)),
                ('instrument_type_processing_level', models.ForeignKey(to='dictionaries.InstrumentTypeProcessingLevel')),
                ('sales_region', models.ForeignKey(default=1, to='dictionaries.SalesRegion')),
                ('spectral_mode', models.ForeignKey(to='dictionaries.SpectralMode')),
            ],
            options={
                'ordering': ['spectral_mode', 'instrument_type_processing_level'],
            },
        ),
        migrations.CreateModel(
            name='SubsidyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full name of a subsidy type', max_length=50)),
                ('abbreviation', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='satelliteinstrument',
            name='satellite_instrument_group',
            field=models.ForeignKey(to='dictionaries.SatelliteInstrumentGroup'),
        ),
        migrations.AddField(
            model_name='radarproductprofile',
            name='satellite_instrument',
            field=models.ForeignKey(to='dictionaries.SatelliteInstrument'),
        ),
        migrations.AddField(
            model_name='place',
            name='place_type',
            field=models.ForeignKey(help_text=b'Type of place', to='dictionaries.PlaceType'),
        ),
        migrations.AddField(
            model_name='opticalproductprofile',
            name='satellite_instrument',
            field=models.ForeignKey(to='dictionaries.SatelliteInstrument'),
        ),
        migrations.AddField(
            model_name='opticalproductprofile',
            name='spectral_mode',
            field=models.ForeignKey(to='dictionaries.SpectralMode'),
        ),
        migrations.AddField(
            model_name='instrumenttypeprocessinglevel',
            name='processing_level',
            field=models.ForeignKey(to='dictionaries.ProcessingLevel'),
        ),
        migrations.AddField(
            model_name='instrumenttype',
            name='base_processing_level',
            field=models.ForeignKey(related_name='base_processing_level', blank=True, to='dictionaries.ProcessingLevel', help_text=b'Processing level as provided by the ground station as "raw data".', null=True),
        ),
        migrations.AddField(
            model_name='instrumenttype',
            name='default_processing_level',
            field=models.ForeignKey(related_name='default_processing_level', blank=True, to='dictionaries.ProcessingLevel', help_text=b'Default processing level that will be supplied to customers.', null=True),
        ),
        migrations.AddField(
            model_name='instrumenttype',
            name='reference_system',
            field=models.ForeignKey(blank=True, to='dictionaries.ReferenceSystem', null=True),
        ),
        migrations.AddField(
            model_name='instrumenttype',
            name='scanner_type',
            field=models.ForeignKey(to='dictionaries.ScannerType'),
        ),
        migrations.AddField(
            model_name='imagingmode',
            name='radarbeam',
            field=models.ForeignKey(to='dictionaries.RadarBeam'),
        ),
        migrations.AddField(
            model_name='collection',
            name='institution',
            field=models.ForeignKey(help_text=b'Organisation that owns this satellite collection.', to='dictionaries.Institution'),
        ),
        migrations.AddField(
            model_name='bandspectralmode',
            name='spectral_mode',
            field=models.ForeignKey(to='dictionaries.SpectralMode'),
        ),
        migrations.AddField(
            model_name='band',
            name='instrument_type',
            field=models.ForeignKey(to='dictionaries.InstrumentType'),
        ),
        migrations.AlterUniqueTogether(
            name='satelliteinstrumentgroup',
            unique_together=set([('satellite', 'instrument_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='bandspectralmode',
            unique_together=set([('band', 'spectral_mode')]),
        ),
    ]
