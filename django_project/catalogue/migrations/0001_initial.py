# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visit_count', models.IntegerField()),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('country', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['visit_count'],
                'db_table': 'vw_visitor_report',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AllUsersMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='GenericProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_date', models.DateTimeField(db_index=True)),
                ('spatial_coverage', django.contrib.gis.db.models.fields.PolygonField(help_text=b'Image footprint', srid=4326)),
                ('original_product_id', models.CharField(help_text=b'Original id assigned to the product by the vendor/operator', unique=True, max_length=255)),
                ('unique_product_id', models.CharField(help_text=b'A unique identifier for product used internally e.g. for DIMS orders', max_length=255, null=True, blank=True)),
                ('local_storage_path', models.CharField(help_text=b'Location on local storage if this product is offered for immediate download.', max_length=255, null=True, blank=True)),
                ('metadata', models.TextField(help_text=b'An xml document describing all known metadata for this product.')),
                ('ingestion_log', models.TextField(help_text=b'The log of ingestion events (written programmatically to this field by ingestors. Stored in chronological order by appending to the bottom of this text field.')),
                ('remote_thumbnail_url', models.TextField(help_text=b"Location on a remote server where this product's thumbnail resides. The value in this field will be nulled when a local copy is made of the thumbnail.", max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-product_date',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255, verbose_name=b'City')),
                ('country', models.CharField(max_length=255, verbose_name=b'Country')),
                ('ip_address', models.IPAddressField(verbose_name=b'IP Address')),
                ('ip_position', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name=b'IP Lat/Long')),
                ('visit_date', models.DateTimeField(auto_now=True, verbose_name=b'DateAdded')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('visit_date',),
                'verbose_name': 'Visit',
                'verbose_name_plural': 'Visits',
            },
        ),
        migrations.CreateModel(
            name='WorldBorders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso2', models.CharField(max_length=2)),
                ('iso3', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='ContinuousProduct',
            fields=[
                ('genericproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericProduct')),
                ('range_min', models.FloatField(help_text=b'The minimum value in the range of values represented in this dataset.')),
                ('range_max', models.FloatField(help_text=b'The maximum value in the range of values represented in thisdataset.')),
                ('unit', models.ForeignKey(help_text=b'Units for the values represented in this dataset.', to='dictionaries.Unit')),
            ],
            bases=('catalogue.genericproduct',),
        ),
        migrations.CreateModel(
            name='GenericImageryProduct',
            fields=[
                ('genericproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericProduct')),
                ('spatial_resolution', models.FloatField(help_text=b'Spatial resolution in m')),
                ('spatial_resolution_x', models.FloatField(help_text=b'Spatial resolution in m (x direction)')),
                ('spatial_resolution_y', models.FloatField(help_text=b'Spatial resolution in m (y direction)')),
                ('radiometric_resolution', models.IntegerField(help_text=b'Bit depth of image e.g. 16bit Note that this is for the delivered image and not necessarily the same as bit depth at acquisition.')),
                ('band_count', models.IntegerField(help_text=b'Number of spectral bands in product')),
            ],
            bases=('catalogue.genericproduct',),
        ),
        migrations.CreateModel(
            name='GeospatialProduct',
            fields=[
                ('genericproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericProduct')),
                ('name', models.CharField(help_text=b'A descriptive name for this dataset', max_length=255)),
                ('description', models.TextField(help_text=b'Description of the product', null=True, blank=True)),
                ('processing_notes', models.TextField(help_text=b'Description of how the product was created.', null=True, blank=True)),
                ('equivalent_scale', models.IntegerField(default=1000000, help_text=b'The fractional part at the ideal maximum scale for this dataset. For example enter "50000" if it should not be used at scales larger that 1:50 000', null=True, blank=True)),
                ('data_type', models.CharField(blank=True, max_length=2, null=True, help_text=b'Is this a vector or raster dataset?', choices=[(b'RA', b'Raster'), (b'VP', b'Vector - Points'), (b'VL', b'Vector - Lines'), (b'VA', b'Vector - Areas / Polygons')])),
                ('temporal_extent_start', models.DateTimeField(help_text=b'The start of the timespan covered by this dataset. If left blank will default to time of accession.', db_index=True)),
                ('temporal_extent_end', models.DateTimeField(help_text=b'The start of the timespan covered by this dataset. If left blankwill default to start date.', null=True, db_index=True, blank=True)),
                ('place', models.ForeignKey(help_text=b'Nearest place, town, country region etc. to this product', to='dictionaries.Place')),
                ('place_type', models.ForeignKey(help_text=b'Select the type of geographic region covered by this dataset', to='dictionaries.PlaceType')),
                ('primary_topic', models.ForeignKey(help_text=b'Select the most appopriate topic for this dataset. You can add additional keywords in the tags box.', to='dictionaries.Topic')),
            ],
            bases=('catalogue.genericproduct',),
        ),
        migrations.CreateModel(
            name='OrdinalProduct',
            fields=[
                ('genericproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericProduct')),
                ('class_count', models.IntegerField(help_text=b'Number of spectral bands in product')),
                ('confusion_matrix', models.CommaSeparatedIntegerField(help_text=b'Confusion matrix in the format: true positive, false negative, false positive,true negative', max_length=80, null=True, blank=True)),
                ('kappa_score', models.FloatField(help_text=b'Enter a value between 0 and 1 representing the kappa score.', null=True, blank=True)),
            ],
            bases=('catalogue.genericproduct',),
        ),
        migrations.AddField(
            model_name='genericproduct',
            name='projection',
            field=models.ForeignKey(to='dictionaries.Projection'),
        ),
        migrations.AddField(
            model_name='genericproduct',
            name='quality',
            field=models.ForeignKey(help_text=b'A quality assessment describing the amount of dropouts etc.and how usable the entire scene is.', to='dictionaries.Quality'),
        ),
        migrations.CreateModel(
            name='GenericSensorProduct',
            fields=[
                ('genericimageryproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericImageryProduct')),
                ('product_acquisition_start', models.DateTimeField(db_index=True)),
                ('product_acquisition_end', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('geometric_accuracy_mean', models.FloatField(db_index=True, null=True, blank=True)),
                ('geometric_accuracy_1sigma', models.FloatField(null=True, blank=True)),
                ('geometric_accuracy_2sigma', models.FloatField(null=True, blank=True)),
                ('radiometric_signal_to_noise_ratio', models.FloatField(null=True, blank=True)),
                ('radiometric_percentage_error', models.FloatField(null=True, blank=True)),
                ('spectral_accuracy', models.FloatField(help_text=b'Wavelength Deviation - a static figure that normally does not change for a given sensor.', null=True, blank=True)),
                ('orbit_number', models.IntegerField(null=True, blank=True)),
                ('path', models.IntegerField(db_index=True, null=True, blank=True)),
                ('path_offset', models.IntegerField(db_index=True, null=True, blank=True)),
                ('row', models.IntegerField(null=True, blank=True)),
                ('row_offset', models.IntegerField(null=True, blank=True)),
                ('offline_storage_medium_id', models.CharField(help_text=b'Identifier for the offline tape or other medium on which this scene is stored', max_length=12, null=True, blank=True)),
                ('online_storage_medium_id', models.CharField(help_text=b'DIMS Product Id as defined by Werum e.g. S5_G2_J_MX_200902160841252_FG_001822', max_length=36, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('catalogue.genericimageryproduct',),
        ),
        migrations.CreateModel(
            name='OpticalProduct',
            fields=[
                ('genericsensorproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericSensorProduct')),
                ('cloud_cover', models.IntegerField(help_text=b'The maximum cloud cover when searching for images. Note that not all sensors support cloud cover filtering. Range 0-100%', max_length=3, null=True, blank=True)),
                ('sensor_inclination_angle', models.FloatField(help_text=b'Orientation of the vehicle on which the sensor is mounted', null=True, blank=True)),
                ('sensor_viewing_angle', models.FloatField(help_text=b'Angle of acquisition for the image', null=True, blank=True)),
                ('gain_name', models.CharField(max_length=200, null=True, blank=True)),
                ('gain_value_per_channel', models.CharField(help_text=b'Comma separated list of gain values', max_length=200, null=True, blank=True)),
                ('gain_change_per_channel', models.CharField(help_text=b'Comma separated list of gain change values', max_length=200, null=True, blank=True)),
                ('bias_per_channel', models.CharField(help_text=b'Comma separated list of bias values', max_length=200, null=True, blank=True)),
                ('solar_zenith_angle', models.FloatField(null=True, blank=True)),
                ('solar_azimuth_angle', models.FloatField(null=True, blank=True)),
                ('earth_sun_distance', models.FloatField(null=True, blank=True)),
                ('product_profile', models.ForeignKey(to='dictionaries.OpticalProductProfile')),
            ],
            bases=('catalogue.genericsensorproduct',),
        ),
        migrations.CreateModel(
            name='RadarProduct',
            fields=[
                ('genericsensorproduct_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='catalogue.GenericSensorProduct')),
                ('imaging_mode', models.CharField(max_length=200, null=True, blank=True)),
                ('look_direction', models.CharField(blank=True, max_length=1, null=True, choices=[(b'L', b'Left'), (b'R', b'Right')])),
                ('antenna_receive_configuration', models.CharField(blank=True, max_length=1, null=True, choices=[(b'V', b'Vertical'), (b'H', b'Horizontal')])),
                ('polarising_mode', models.CharField(blank=True, max_length=1, null=True, choices=[(b'S', b'Single Pole'), (b'D', b'Dual Pole'), (b'Q', b'Quad Pole')])),
                ('polarising_list', models.CharField(help_text=b'Comma separated list of V/H/VV/VH/HV/HH (vertical and horizontal polarisation.)', max_length=200, null=True, blank=True)),
                ('slant_range_resolution', models.FloatField(null=True, blank=True)),
                ('azimuth_range_resolution', models.FloatField(null=True, blank=True)),
                ('orbit_direction', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'Ascending'), (b'D', b'Descending')])),
                ('calibration', models.CharField(max_length=255, null=True, blank=True)),
                ('incidence_angle', models.FloatField(null=True, blank=True)),
                ('product_profile', models.ForeignKey(to='dictionaries.RadarProductProfile')),
            ],
            bases=('catalogue.genericsensorproduct',),
        ),
    ]
