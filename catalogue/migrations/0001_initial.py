# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MissionGroup'
        db.create_table('catalogue_missiongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
        ))
        db.send_create_signal('catalogue', ['MissionGroup'])

        # Adding model 'Mission'
        db.create_table('catalogue_mission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('operator_abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('mission_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.MissionGroup'])),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('catalogue', ['Mission'])

        # Adding model 'MissionSensor'
        db.create_table('catalogue_missionsensor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length='3')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('has_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Mission'])),
            ('is_radar', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_taskable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('operator_abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('catalogue', ['MissionSensor'])

        # Adding unique constraint on 'MissionSensor', fields ['mission', 'abbreviation']
        db.create_unique('catalogue_missionsensor', ['mission_id', 'abbreviation'])

        # Adding model 'SensorType'
        db.create_table('catalogue_sensortype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length='4')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('mission_sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.MissionSensor'])),
            ('operator_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('catalogue', ['SensorType'])

        # Adding unique constraint on 'SensorType', fields ['mission_sensor', 'abbreviation']
        db.create_unique('catalogue_sensortype', ['mission_sensor_id', 'abbreviation'])

        # Adding model 'AcquisitionMode'
        db.create_table('catalogue_acquisitionmode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.SensorType'])),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length='4')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('geometric_resolution', self.gf('django.db.models.fields.IntegerField')()),
            ('band_count', self.gf('django.db.models.fields.IntegerField')()),
            ('is_grayscale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('operator_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('catalogue', ['AcquisitionMode'])

        # Adding unique constraint on 'AcquisitionMode', fields ['sensor_type', 'abbreviation']
        db.create_unique('catalogue_acquisitionmode', ['sensor_type_id', 'abbreviation'])

        # Adding model 'ProcessingLevel'
        db.create_table('catalogue_processinglevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length='4')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='255')),
        ))
        db.send_create_signal('catalogue', ['ProcessingLevel'])

        # Adding model 'Projection'
        db.create_table('catalogue_projection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('epsg_code', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
        ))
        db.send_create_signal('catalogue', ['Projection'])

        # Adding model 'Institution'
        db.create_table('catalogue_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('address3', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length='255')),
        ))
        db.send_create_signal('catalogue', ['Institution'])

        # Adding model 'License'
        db.create_table('catalogue_license', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=3)),
        ))
        db.send_create_signal('catalogue', ['License'])

        # Adding model 'Quality'
        db.create_table('catalogue_quality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
        ))
        db.send_create_signal('catalogue', ['Quality'])

        # Adding model 'CreatingSoftware'
        db.create_table('catalogue_creatingsoftware', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
            ('version', self.gf('django.db.models.fields.CharField')(max_length='100')),
        ))
        db.send_create_signal('catalogue', ['CreatingSoftware'])

        # Adding model 'Topic'
        db.create_table('catalogue_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length='10')),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
        ))
        db.send_create_signal('catalogue', ['Topic'])

        # Adding model 'PlaceType'
        db.create_table('catalogue_placetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
        ))
        db.send_create_signal('catalogue', ['PlaceType'])

        # Adding model 'Place'
        db.create_table('catalogue_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('place_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.PlaceType'])),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('catalogue', ['Place'])

        # Adding model 'Unit'
        db.create_table('catalogue_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length='10')),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
        ))
        db.send_create_signal('catalogue', ['Unit'])

        # Adding model 'GenericProduct'
        db.create_table('catalogue_genericproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('processing_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.ProcessingLevel'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Institution'])),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.License'])),
            ('spatial_coverage', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('projection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Projection'])),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Quality'])),
            ('creating_software', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.CreatingSoftware'])),
            ('original_product_id', self.gf('django.db.models.fields.CharField')(max_length='255', null=True, blank=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255', db_index=True)),
            ('product_revision', self.gf('django.db.models.fields.CharField')(max_length='255', null=True, blank=True)),
            ('local_storage_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.TextField')()),
            ('remote_thumbnail_url', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['GenericProduct'])

        # Adding model 'ProductLink'
        db.create_table('catalogue_productlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='GenericProduct_child', to=orm['catalogue.GenericProduct'])),
            ('child', self.gf('django.db.models.fields.related.ForeignKey')(related_name='GenericProduct_parent', to=orm['catalogue.GenericProduct'])),
        ))
        db.send_create_signal('catalogue', ['ProductLink'])

        # Adding model 'GenericImageryProduct'
        db.create_table('catalogue_genericimageryproduct', (
            ('genericproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericProduct'], unique=True, primary_key=True)),
            ('geometric_resolution', self.gf('django.db.models.fields.FloatField')()),
            ('geometric_resolution_x', self.gf('django.db.models.fields.FloatField')()),
            ('geometric_resolution_y', self.gf('django.db.models.fields.FloatField')()),
            ('radiometric_resolution', self.gf('django.db.models.fields.IntegerField')()),
            ('band_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('catalogue', ['GenericImageryProduct'])

        # Adding model 'GenericSensorProduct'
        db.create_table('catalogue_genericsensorproduct', (
            ('genericimageryproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericImageryProduct'], unique=True, primary_key=True)),
            ('acquisition_mode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AcquisitionMode'])),
            ('product_acquisition_start', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('product_acquisition_end', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('geometric_accuracy_mean', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('geometric_accuracy_1sigma', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geometric_accuracy_2sigma', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('radiometric_signal_to_noise_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('radiometric_percentage_error', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('spectral_accuracy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbit_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('path', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('path_offset', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('row', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('row_offset', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('offline_storage_medium_id', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('online_storage_medium_id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['GenericSensorProduct'])

        # Adding model 'OpticalProduct'
        db.create_table('catalogue_opticalproduct', (
            ('genericsensorproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericSensorProduct'], unique=True, primary_key=True)),
            ('cloud_cover', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('sensor_inclination_angle', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sensor_viewing_angle', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gain_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('gain_value_per_channel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('gain_change_per_channel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('bias_per_channel', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('solar_zenith_angle', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('solar_azimuth_angle', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('earth_sun_distance', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['OpticalProduct'])

        # Adding model 'RadarProduct'
        db.create_table('catalogue_radarproduct', (
            ('genericsensorproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericSensorProduct'], unique=True, primary_key=True)),
            ('imaging_mode', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('look_direction', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('antenna_receive_configuration', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('polarising_mode', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('polarising_list', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slant_range_resolution', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('azimuth_range_resolution', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('orbit_direction', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('calibration', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('incidence_angle', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['RadarProduct'])

        # Adding model 'GeospatialProduct'
        db.create_table('catalogue_geospatialproduct', (
            ('genericproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericProduct'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('processing_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('equivalent_scale', self.gf('django.db.models.fields.IntegerField')(default=1000000, null=True, blank=True)),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('temporal_extent_start', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('temporal_extent_end', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('place_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.PlaceType'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Place'])),
            ('primary_topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Topic'])),
        ))
        db.send_create_signal('catalogue', ['GeospatialProduct'])

        # Adding model 'OrdinalProduct'
        db.create_table('catalogue_ordinalproduct', (
            ('genericproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericProduct'], unique=True, primary_key=True)),
            ('class_count', self.gf('django.db.models.fields.IntegerField')()),
            ('confusion_matrix', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=80, null=True, blank=True)),
            ('kappa_score', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['OrdinalProduct'])

        # Adding model 'ContinuousProduct'
        db.create_table('catalogue_continuousproduct', (
            ('genericproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.GenericProduct'], unique=True, primary_key=True)),
            ('range_min', self.gf('django.db.models.fields.FloatField')()),
            ('range_max', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Unit'])),
        ))
        db.send_create_signal('catalogue', ['ContinuousProduct'])

        # Adding model 'Datum'
        db.create_table('catalogue_datum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
        ))
        db.send_create_signal('catalogue', ['Datum'])

        # Adding model 'ResamplingMethod'
        db.create_table('catalogue_resamplingmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
        ))
        db.send_create_signal('catalogue', ['ResamplingMethod'])

        # Adding model 'FileFormat'
        db.create_table('catalogue_fileformat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
        ))
        db.send_create_signal('catalogue', ['FileFormat'])

        # Adding model 'OrderStatus'
        db.create_table('catalogue_orderstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
        ))
        db.send_create_signal('catalogue', ['OrderStatus'])

        # Adding model 'DeliveryMethod'
        db.create_table('catalogue_deliverymethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
        ))
        db.send_create_signal('catalogue', ['DeliveryMethod'])

        # Adding model 'DeliveryDetail'
        db.create_table('catalogue_deliverydetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('processing_level', self.gf('django.db.models.fields.related.ForeignKey')(default=3, to=orm['catalogue.ProcessingLevel'])),
            ('projection', self.gf('django.db.models.fields.related.ForeignKey')(default=3, to=orm['catalogue.Projection'])),
            ('datum', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['catalogue.Datum'])),
            ('resampling_method', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['catalogue.ResamplingMethod'])),
            ('file_format', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['catalogue.FileFormat'])),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['DeliveryDetail'])

        # Adding model 'MarketSector'
        db.create_table('catalogue_marketsector', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length='80')),
        ))
        db.send_create_signal('catalogue', ['MarketSector'])

        # Adding model 'Order'
        db.create_table('catalogue_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order_status', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['catalogue.OrderStatus'])),
            ('delivery_method', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['catalogue.DeliveryMethod'])),
            ('delivery_detail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.DeliveryDetail'], null=True, blank=True)),
            ('market_sector', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['catalogue.MarketSector'])),
            ('order_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Order'])

        # Adding model 'OrderStatusHistory'
        db.create_table('catalogue_orderstatushistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Order'])),
            ('order_change_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('old_order_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='old_order_status', to=orm['catalogue.OrderStatus'])),
            ('new_order_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='new_order_status', to=orm['catalogue.OrderStatus'])),
        ))
        db.send_create_signal('catalogue', ['OrderStatusHistory'])

        # Adding model 'TaskingRequest'
        db.create_table('catalogue_taskingrequest', (
            ('order_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.Order'], unique=True, primary_key=True)),
            ('target_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('mission_sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.MissionSensor'])),
        ))
        db.send_create_signal('catalogue', ['TaskingRequest'])

        # Adding model 'SearchRecord'
        db.create_table('catalogue_searchrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Order'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.GenericProduct'])),
            ('delivery_detail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.DeliveryDetail'], null=True, blank=True)),
            ('internal_order_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('download_path', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('product_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('catalogue', ['SearchRecord'])

        # Adding model 'Search'
        db.create_table('catalogue_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_type', self.gf('django.db.models.fields.IntegerField')(default=1, db_index=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('k_orbit_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('j_frame_row', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ip_position', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('search_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('deleted', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('use_cloud_cover', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cloud_mean', self.gf('django.db.models.fields.IntegerField')(default=5, max_length=1, null=True, blank=True)),
            ('acquisition_mode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AcquisitionMode'], null=True, blank=True)),
            ('license_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('band_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('geometric_accuracy_mean', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sensor_inclination_angle_start', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sensor_inclination_angle_end', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Mission'], null=True, blank=True)),
            ('sensor_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='search_sensor_type', null=True, to=orm['catalogue.SensorType'])),
            ('polarising_mode', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('record_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Search'])

        # Adding M2M table for field sensors on 'Search'
        db.create_table('catalogue_search_sensors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm['catalogue.search'], null=False)),
            ('missionsensor', models.ForeignKey(orm['catalogue.missionsensor'], null=False))
        ))
        db.create_unique('catalogue_search_sensors', ['search_id', 'missionsensor_id'])

        # Adding M2M table for field processing_level on 'Search'
        db.create_table('catalogue_search_processing_level', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm['catalogue.search'], null=False)),
            ('processinglevel', models.ForeignKey(orm['catalogue.processinglevel'], null=False))
        ))
        db.create_unique('catalogue_search_processing_level', ['search_id', 'processinglevel_id'])

        # Adding model 'SearchDateRange'
        db.create_table('catalogue_searchdaterange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Search'])),
        ))
        db.send_create_signal('catalogue', ['SearchDateRange'])

        # Adding model 'Clip'
        db.create_table('catalogue_clip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('result_url', self.gf('django.db.models.fields.URLField')(max_length=1024)),
        ))
        db.send_create_signal('catalogue', ['Clip'])

        # Adding model 'Visit'
        db.create_table('catalogue_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('ip_position', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('visit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Visit'])

        # Adding model 'SacUserProfile'
        db.create_table('catalogue_sacuserprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('country', self.gf('userprofile.countries.CountryField')(max_length=2, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=6, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=6, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('strategic_partner', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address3', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address4', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact_no', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('catalogue', ['SacUserProfile'])

        # Adding model 'OrderNotificationRecipients'
        db.create_table('catalogue_ordernotificationrecipients', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('catalogue', ['OrderNotificationRecipients'])

        # Adding M2M table for field sensors on 'OrderNotificationRecipients'
        db.create_table('catalogue_ordernotificationrecipients_sensors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordernotificationrecipients', models.ForeignKey(orm['catalogue.ordernotificationrecipients'], null=False)),
            ('missionsensor', models.ForeignKey(orm['catalogue.missionsensor'], null=False))
        ))
        db.create_unique('catalogue_ordernotificationrecipients_sensors', ['ordernotificationrecipients_id', 'missionsensor_id'])

        # Adding M2M table for field classes on 'OrderNotificationRecipients'
        db.create_table('catalogue_ordernotificationrecipients_classes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordernotificationrecipients', models.ForeignKey(orm['catalogue.ordernotificationrecipients'], null=False)),
            ('contenttype', models.ForeignKey(orm['contenttypes.contenttype'], null=False))
        ))
        db.create_unique('catalogue_ordernotificationrecipients_classes', ['ordernotificationrecipients_id', 'contenttype_id'])

        # Adding model 'WorldBorders'
        db.create_table('catalogue_worldborders', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso2', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('catalogue', ['WorldBorders'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AcquisitionMode', fields ['sensor_type', 'abbreviation']
        db.delete_unique('catalogue_acquisitionmode', ['sensor_type_id', 'abbreviation'])

        # Removing unique constraint on 'SensorType', fields ['mission_sensor', 'abbreviation']
        db.delete_unique('catalogue_sensortype', ['mission_sensor_id', 'abbreviation'])

        # Removing unique constraint on 'MissionSensor', fields ['mission', 'abbreviation']
        db.delete_unique('catalogue_missionsensor', ['mission_id', 'abbreviation'])

        # Deleting model 'MissionGroup'
        db.delete_table('catalogue_missiongroup')

        # Deleting model 'Mission'
        db.delete_table('catalogue_mission')

        # Deleting model 'MissionSensor'
        db.delete_table('catalogue_missionsensor')

        # Deleting model 'SensorType'
        db.delete_table('catalogue_sensortype')

        # Deleting model 'AcquisitionMode'
        db.delete_table('catalogue_acquisitionmode')

        # Deleting model 'ProcessingLevel'
        db.delete_table('catalogue_processinglevel')

        # Deleting model 'Projection'
        db.delete_table('catalogue_projection')

        # Deleting model 'Institution'
        db.delete_table('catalogue_institution')

        # Deleting model 'License'
        db.delete_table('catalogue_license')

        # Deleting model 'Quality'
        db.delete_table('catalogue_quality')

        # Deleting model 'CreatingSoftware'
        db.delete_table('catalogue_creatingsoftware')

        # Deleting model 'Topic'
        db.delete_table('catalogue_topic')

        # Deleting model 'PlaceType'
        db.delete_table('catalogue_placetype')

        # Deleting model 'Place'
        db.delete_table('catalogue_place')

        # Deleting model 'Unit'
        db.delete_table('catalogue_unit')

        # Deleting model 'GenericProduct'
        db.delete_table('catalogue_genericproduct')

        # Deleting model 'ProductLink'
        db.delete_table('catalogue_productlink')

        # Deleting model 'GenericImageryProduct'
        db.delete_table('catalogue_genericimageryproduct')

        # Deleting model 'GenericSensorProduct'
        db.delete_table('catalogue_genericsensorproduct')

        # Deleting model 'OpticalProduct'
        db.delete_table('catalogue_opticalproduct')

        # Deleting model 'RadarProduct'
        db.delete_table('catalogue_radarproduct')

        # Deleting model 'GeospatialProduct'
        db.delete_table('catalogue_geospatialproduct')

        # Deleting model 'OrdinalProduct'
        db.delete_table('catalogue_ordinalproduct')

        # Deleting model 'ContinuousProduct'
        db.delete_table('catalogue_continuousproduct')

        # Deleting model 'Datum'
        db.delete_table('catalogue_datum')

        # Deleting model 'ResamplingMethod'
        db.delete_table('catalogue_resamplingmethod')

        # Deleting model 'FileFormat'
        db.delete_table('catalogue_fileformat')

        # Deleting model 'OrderStatus'
        db.delete_table('catalogue_orderstatus')

        # Deleting model 'DeliveryMethod'
        db.delete_table('catalogue_deliverymethod')

        # Deleting model 'DeliveryDetail'
        db.delete_table('catalogue_deliverydetail')

        # Deleting model 'MarketSector'
        db.delete_table('catalogue_marketsector')

        # Deleting model 'Order'
        db.delete_table('catalogue_order')

        # Deleting model 'OrderStatusHistory'
        db.delete_table('catalogue_orderstatushistory')

        # Deleting model 'TaskingRequest'
        db.delete_table('catalogue_taskingrequest')

        # Deleting model 'SearchRecord'
        db.delete_table('catalogue_searchrecord')

        # Deleting model 'Search'
        db.delete_table('catalogue_search')

        # Removing M2M table for field sensors on 'Search'
        db.delete_table('catalogue_search_sensors')

        # Removing M2M table for field processing_level on 'Search'
        db.delete_table('catalogue_search_processing_level')

        # Deleting model 'SearchDateRange'
        db.delete_table('catalogue_searchdaterange')

        # Deleting model 'Clip'
        db.delete_table('catalogue_clip')

        # Deleting model 'Visit'
        db.delete_table('catalogue_visit')

        # Deleting model 'SacUserProfile'
        db.delete_table('catalogue_sacuserprofile')

        # Deleting model 'OrderNotificationRecipients'
        db.delete_table('catalogue_ordernotificationrecipients')

        # Removing M2M table for field sensors on 'OrderNotificationRecipients'
        db.delete_table('catalogue_ordernotificationrecipients_sensors')

        # Removing M2M table for field classes on 'OrderNotificationRecipients'
        db.delete_table('catalogue_ordernotificationrecipients_classes')

        # Deleting model 'WorldBorders'
        db.delete_table('catalogue_worldborders')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'catalogue.acquisitionmode': {
            'Meta': {'unique_together': "(('sensor_type', 'abbreviation'),)", 'object_name': 'AcquisitionMode'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': "'4'"}),
            'band_count': ('django.db.models.fields.IntegerField', [], {}),
            'geometric_resolution': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_grayscale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'operator_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sensor_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.SensorType']"})
        },
        'catalogue.clip': {
            'Meta': {'object_name': 'Clip'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'result_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'catalogue.continuousproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'ContinuousProduct', '_ormbases': ['catalogue.GenericProduct']},
            'genericproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'range_max': ('django.db.models.fields.FloatField', [], {}),
            'range_min': ('django.db.models.fields.FloatField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Unit']"})
        },
        'catalogue.creatingsoftware': {
            'Meta': {'object_name': 'CreatingSoftware'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': "'100'"})
        },
        'catalogue.datum': {
            'Meta': {'object_name': 'Datum'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        'catalogue.deliverydetail': {
            'Meta': {'object_name': 'DeliveryDetail'},
            'datum': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['catalogue.Datum']"}),
            'file_format': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['catalogue.FileFormat']"}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processing_level': ('django.db.models.fields.related.ForeignKey', [], {'default': '3', 'to': "orm['catalogue.ProcessingLevel']"}),
            'projection': ('django.db.models.fields.related.ForeignKey', [], {'default': '3', 'to': "orm['catalogue.Projection']"}),
            'resampling_method': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': "orm['catalogue.ResamplingMethod']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'catalogue.deliverymethod': {
            'Meta': {'object_name': 'DeliveryMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        'catalogue.fileformat': {
            'Meta': {'object_name': 'FileFormat'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        'catalogue.genericimageryproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'GenericImageryProduct', '_ormbases': ['catalogue.GenericProduct']},
            'band_count': ('django.db.models.fields.IntegerField', [], {}),
            'genericproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'geometric_resolution': ('django.db.models.fields.FloatField', [], {}),
            'geometric_resolution_x': ('django.db.models.fields.FloatField', [], {}),
            'geometric_resolution_y': ('django.db.models.fields.FloatField', [], {}),
            'radiometric_resolution': ('django.db.models.fields.IntegerField', [], {})
        },
        'catalogue.genericproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'GenericProduct'},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalogue.GenericProduct']", 'null': 'True', 'through': "orm['catalogue.ProductLink']", 'blank': 'True'}),
            'creating_software': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.CreatingSoftware']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.License']"}),
            'local_storage_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {}),
            'original_product_id': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Institution']"}),
            'processing_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.ProcessingLevel']"}),
            'product_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'", 'db_index': 'True'}),
            'product_revision': ('django.db.models.fields.CharField', [], {'max_length': "'255'", 'null': 'True', 'blank': 'True'}),
            'projection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Projection']"}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Quality']"}),
            'remote_thumbnail_url': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'spatial_coverage': ('django.contrib.gis.db.models.fields.PolygonField', [], {})
        },
        'catalogue.genericsensorproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'GenericSensorProduct', '_ormbases': ['catalogue.GenericImageryProduct']},
            'acquisition_mode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.AcquisitionMode']"}),
            'genericimageryproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericImageryProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'geometric_accuracy_1sigma': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geometric_accuracy_2sigma': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geometric_accuracy_mean': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'offline_storage_medium_id': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'online_storage_medium_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'orbit_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'path_offset': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'product_acquisition_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'product_acquisition_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'radiometric_percentage_error': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'radiometric_signal_to_noise_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'row': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'row_offset': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spectral_accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.geospatialproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'GeospatialProduct', '_ormbases': ['catalogue.GenericProduct']},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'equivalent_scale': ('django.db.models.fields.IntegerField', [], {'default': '1000000', 'null': 'True', 'blank': 'True'}),
            'genericproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Place']"}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.PlaceType']"}),
            'primary_topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Topic']"}),
            'processing_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'temporal_extent_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'temporal_extent_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'catalogue.institution': {
            'Meta': {'object_name': 'Institution'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': "'255'"})
        },
        'catalogue.license': {
            'Meta': {'object_name': 'License'},
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        'catalogue.marketsector': {
            'Meta': {'object_name': 'MarketSector'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'80'"})
        },
        'catalogue.mission': {
            'Meta': {'object_name': 'Mission'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.MissionGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'operator_abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalogue.missiongroup': {
            'Meta': {'object_name': 'MissionGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"})
        },
        'catalogue.missionsensor': {
            'Meta': {'unique_together': "(('mission', 'abbreviation'),)", 'object_name': 'MissionSensor'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': "'3'"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'has_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_radar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_taskable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Mission']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'operator_abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'catalogue.opticalproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'OpticalProduct', '_ormbases': ['catalogue.GenericSensorProduct']},
            'bias_per_channel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cloud_cover': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'earth_sun_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gain_change_per_channel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gain_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gain_value_per_channel': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'genericsensorproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericSensorProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor_inclination_angle': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor_viewing_angle': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solar_azimuth_angle': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'solar_zenith_angle': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.order': {
            'Meta': {'object_name': 'Order'},
            'delivery_detail': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.DeliveryDetail']", 'null': 'True', 'blank': 'True'}),
            'delivery_method': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['catalogue.DeliveryMethod']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_sector': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['catalogue.MarketSector']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'order_status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['catalogue.OrderStatus']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'catalogue.ordernotificationrecipients': {
            'Meta': {'object_name': 'OrderNotificationRecipients'},
            'classes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalogue.MissionSensor']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'catalogue.orderstatus': {
            'Meta': {'object_name': 'OrderStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        'catalogue.orderstatushistory': {
            'Meta': {'ordering': "('-order_change_date',)", 'object_name': 'OrderStatusHistory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_order_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_order_status'", 'to': "orm['catalogue.OrderStatus']"}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'old_order_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'old_order_status'", 'to': "orm['catalogue.OrderStatus']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Order']"}),
            'order_change_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'catalogue.ordinalproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'OrdinalProduct', '_ormbases': ['catalogue.GenericProduct']},
            'class_count': ('django.db.models.fields.IntegerField', [], {}),
            'confusion_matrix': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'genericproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'kappa_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.place': {
            'Meta': {'object_name': 'Place'},
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.PlaceType']"})
        },
        'catalogue.placetype': {
            'Meta': {'object_name': 'PlaceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"})
        },
        'catalogue.processinglevel': {
            'Meta': {'object_name': 'ProcessingLevel'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'4'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"})
        },
        'catalogue.productlink': {
            'Meta': {'object_name': 'ProductLink'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GenericProduct_parent'", 'to': "orm['catalogue.GenericProduct']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'GenericProduct_child'", 'to': "orm['catalogue.GenericProduct']"})
        },
        'catalogue.projection': {
            'Meta': {'ordering': "('epsg_code', 'name')", 'object_name': 'Projection'},
            'epsg_code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        'catalogue.quality': {
            'Meta': {'object_name': 'Quality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"})
        },
        'catalogue.radarproduct': {
            'Meta': {'ordering': "('product_date',)", 'object_name': 'RadarProduct', '_ormbases': ['catalogue.GenericSensorProduct']},
            'antenna_receive_configuration': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'azimuth_range_resolution': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'calibration': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'genericsensorproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.GenericSensorProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'imaging_mode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'incidence_angle': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'look_direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'orbit_direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'polarising_list': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'polarising_mode': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'slant_range_resolution': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.resamplingmethod': {
            'Meta': {'object_name': 'ResamplingMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        'catalogue.sacuserprofile': {
            'Meta': {'object_name': 'SacUserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_no': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'country': ('userprofile.countries.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '6', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'strategic_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'catalogue.search': {
            'Meta': {'ordering': "('search_date',)", 'object_name': 'Search'},
            'acquisition_mode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.AcquisitionMode']", 'null': 'True', 'blank': 'True'}),
            'band_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cloud_mean': ('django.db.models.fields.IntegerField', [], {'default': '5', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'geometric_accuracy_mean': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_position': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'j_frame_row': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'k_orbit_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Mission']", 'null': 'True', 'blank': 'True'}),
            'polarising_mode': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'processing_level': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalogue.ProcessingLevel']", 'null': 'True', 'blank': 'True'}),
            'record_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'search_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'search_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'sensor_inclination_angle_end': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor_inclination_angle_start': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'search_sensor_type'", 'null': 'True', 'to': "orm['catalogue.SensorType']"}),
            'sensors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalogue.MissionSensor']", 'null': 'True', 'blank': 'True'}),
            'use_cloud_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'catalogue.searchdaterange': {
            'Meta': {'object_name': 'SearchDateRange'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Search']"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'catalogue.searchrecord': {
            'Meta': {'object_name': 'SearchRecord'},
            'delivery_detail': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.DeliveryDetail']", 'null': 'True', 'blank': 'True'}),
            'download_path': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Order']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.GenericProduct']"}),
            'product_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'catalogue.sensortype': {
            'Meta': {'unique_together': "(('mission_sensor', 'abbreviation'),)", 'object_name': 'SensorType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': "'4'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.MissionSensor']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'operator_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalogue.taskingrequest': {
            'Meta': {'object_name': 'TaskingRequest', '_ormbases': ['catalogue.Order']},
            'mission_sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.MissionSensor']"}),
            'order_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.Order']", 'unique': 'True', 'primary_key': 'True'}),
            'target_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'catalogue.topic': {
            'Meta': {'object_name': 'Topic'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'10'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"})
        },
        'catalogue.unit': {
            'Meta': {'object_name': 'Unit'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'10'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"})
        },
        'catalogue.visit': {
            'Meta': {'ordering': "('visit_date',)", 'object_name': 'Visit'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'ip_position': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'visit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'catalogue.visitorreport': {
            'Meta': {'object_name': 'VisitorReport', 'db_table': "u'vw_visitor_report'", 'managed': 'False'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visit_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'catalogue.worldborders': {
            'Meta': {'object_name': 'WorldBorders'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalogue']
