# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
        ('dictionaries', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='geospatialproduct',
            name='place',
            field=models.ForeignKey(help_text=b'Nearest place, town, country region etc. to this product', to='dictionaries.Place'),
        ),
        migrations.AddField(
            model_name='geospatialproduct',
            name='place_type',
            field=models.ForeignKey(help_text=b'Select the type of geographic region covered by this dataset', to='dictionaries.PlaceType'),
        ),
        migrations.AddField(
            model_name='geospatialproduct',
            name='primary_topic',
            field=models.ForeignKey(help_text=b'Select the most appopriate topic for this dataset. You can add additional keywords in the tags box.', to='dictionaries.Topic'),
        ),
        migrations.AddField(
            model_name='continuousproduct',
            name='unit',
            field=models.ForeignKey(help_text=b'Units for the values represented in this dataset.', to='dictionaries.Unit'),
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
