# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
        ('dictionaries', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '__first__'),
        ('orders', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=40)),
                ('date', models.DateTimeField(help_text=b'Not shown to users', verbose_name=b'Date', auto_now_add=True)),
                ('image', models.CharField(max_length=20, choices=[(0, b'zaSpot2mMosaic2009'), (1, b'zaSpot2mMosaic2008'), (2, b'zaSpot2mMosaic2007')])),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('status', models.CharField(max_length=20, choices=[(0, b'submitted'), (1, b'in process'), (2, b'completed')])),
                ('result_url', models.URLField(max_length=1024)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Clip',
                'verbose_name_plural': 'Clips',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(help_text=b'Digitising an area of interest is not required but is recommended.', srid=4326, null=True, blank=True)),
                ('ip_position', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('search_date', models.DateTimeField(help_text=b'When the search was made - not shown to users', verbose_name=b'Search Date', auto_now_add=True)),
                ('guid', models.CharField(unique=True, max_length=40)),
                ('deleted', models.NullBooleanField(default=True, help_text=b'Mark this search as deleted so the user does not see it', verbose_name=b'Deleted?')),
                ('record_count', models.IntegerField(null=True, editable=False, blank=True)),
                ('k_orbit_path', models.CharField(help_text=b'Path (K) value. If specified here, geometry will be ignored. Must be a value between 1 and 233. Can also be specified as a comma separated list of values or a range. Will be ignored if sensor type does not include J/K metadata.', max_length=255, null=True, blank=True)),
                ('j_frame_row', models.CharField(help_text=b'Row (J) value. If specified here, geometry will be ignored. Must be a value between 1 and 248. Can also be specified as a comma separated list of values or a range. Will be ignored if sensor type does not include J/K metadata.', max_length=255, null=True, blank=True)),
                ('use_cloud_cover', models.BooleanField(default=False, help_text=b'If you want to limit searches to optical products with a certain cloud cover, enable this.', verbose_name=b'Use cloud cover?')),
                ('cloud_mean', models.IntegerField(max_length=3, null=True, verbose_name=b'Max Clouds', blank=True)),
                ('band_count', models.IntegerField(blank=True, help_text=b'Select the spectral resolution.', null=True, choices=[(0, b'Panchromatic'), (1, b'True colour (3 bands RGB)'), (2, b'Multispectral (4 - 8 bands)'), (3, b'Superspectral (9 - 40 bands)'), (4, b'Hyperspectral (> 41 bands)')])),
                ('spatial_resolution', models.IntegerField(blank=True, help_text=b'Select mean spatial resolution class.', null=True, verbose_name=b'Spatial resolution', choices=[(0, b'<= 1m'), (1, b'1m - 2m'), (2, b'2m - 6m'), (3, b'6m - 20m'), (4, b'20m - 35m'), (5, b'35m - 60m')])),
                ('sensor_inclination_angle_start', models.FloatField(help_text=b'Enter a minimum sensor inclination angle.', null=True, blank=True)),
                ('sensor_inclination_angle_end', models.FloatField(help_text=b'Enter a maximum sensor inclination angle.', null=True, blank=True)),
                ('collection', models.ManyToManyField(help_text=b'Select one or more satellite collections.', to='dictionaries.Collection', null=True, blank=True)),
                ('instrument_type', models.ManyToManyField(help_text=b'Choosing one or more instrument types is required. Use ctrl-click to select more than one.', to='dictionaries.InstrumentType', null=True, verbose_name='Sensors', blank=True)),
                ('license_type', models.ManyToManyField(help_text=b'Choose a license type.', to='dictionaries.License', null=True, blank=True)),
                ('processing_level', models.ManyToManyField(help_text=b'Select one or more processing level.', to='dictionaries.ProcessingLevel', null=True, blank=True)),
                ('satellite', models.ManyToManyField(help_text=b'Select satellite mission.', to='dictionaries.Satellite', null=True, blank=True)),
                ('spectral_group', models.ManyToManyField(help_text=b'Select one or more spectral groups.', to='dictionaries.SpectralGroup', null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('search_date',),
                'verbose_name': 'Search',
                'verbose_name_plural': 'Searches',
            },
        ),
        migrations.CreateModel(
            name='SearchDateRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(help_text=b'Product date is required. DD-MM-YYYY.')),
                ('end_date', models.DateField(help_text=b'Product date is required. DD-MM-YYYY.')),
                ('search', models.ForeignKey(to='search.Search')),
            ],
        ),
        migrations.CreateModel(
            name='SearchRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('internal_order_id', models.IntegerField(null=True, blank=True)),
                ('download_path', models.CharField(help_text=b'This is the location from where the product can be downloaded after a successfull OS4EO order placement.', max_length=512)),
                ('product_ready', models.BooleanField(default=False)),
                ('cost_per_scene', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('rand_cost_per_scene', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('currency', models.ForeignKey(blank=True, to='exchange.Currency', null=True)),
                ('order', models.ForeignKey(blank=True, to='orders.Order', null=True)),
                ('processing_level', models.ForeignKey(verbose_name=b'Processing Level', blank=True, to='dictionaries.ProcessingLevel', null=True)),
                ('product', models.ForeignKey(to='catalogue.GenericProduct')),
                ('product_process_state', models.ForeignKey(blank=True, to='dictionaries.ProductProcessState', null=True)),
                ('projection', models.ForeignKey(verbose_name=b'Projection', blank=True, to='dictionaries.Projection', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
            },
        ),
    ]
