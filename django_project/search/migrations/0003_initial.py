# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SearchRecord'
        db.create_table(u'search_searchrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.GenericProduct'])),
            ('internal_order_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('download_path', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('product_ready', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost_per_scene', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('rand_cost_per_scene', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency'], null=True, blank=True)),
            ('processing_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dictionaries.ProcessingLevel'], null=True, blank=True)),
            ('projection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dictionaries.Projection'], null=True, blank=True)),
            ('product_process_state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dictionaries.ProductProcessState'], null=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['SearchRecord'])

        # Adding model 'Search'
        db.create_table(u'search_search', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('ip_position', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('search_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('deleted', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('record_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('k_orbit_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('j_frame_row', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('use_cloud_cover', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cloud_mean', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('band_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('spatial_resolution', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sensor_inclination_angle_start', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sensor_inclination_angle_end', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['Search'])

        # Adding M2M table for field instrument_type on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_instrument_type')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('instrumenttype', models.ForeignKey(orm[u'dictionaries.instrumenttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'instrumenttype_id'])

        # Adding M2M table for field satellite on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_satellite')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('satellite', models.ForeignKey(orm[u'dictionaries.satellite'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'satellite_id'])

        # Adding M2M table for field license_type on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_license_type')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('license', models.ForeignKey(orm[u'dictionaries.license'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'license_id'])

        # Adding M2M table for field spectral_group on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_spectral_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('spectralgroup', models.ForeignKey(orm[u'dictionaries.spectralgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'spectralgroup_id'])

        # Adding M2M table for field processing_level on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_processing_level')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('processinglevel', models.ForeignKey(orm[u'dictionaries.processinglevel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'processinglevel_id'])

        # Adding M2M table for field collection on 'Search'
        m2m_table_name = db.shorten_name(u'search_search_collection')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm[u'search.search'], null=False)),
            ('collection', models.ForeignKey(orm[u'dictionaries.collection'], null=False))
        ))
        db.create_unique(m2m_table_name, ['search_id', 'collection_id'])

        # Adding model 'SearchDateRange'
        db.create_table(u'search_searchdaterange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Search'])),
        ))
        db.send_create_signal(u'search', ['SearchDateRange'])

        # Adding model 'Clip'
        db.create_table(u'search_clip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('result_url', self.gf('django.db.models.fields.URLField')(max_length=1024)),
        ))
        db.send_create_signal(u'search', ['Clip'])


    def backwards(self, orm):
        # Deleting model 'SearchRecord'
        db.delete_table(u'search_searchrecord')

        # Deleting model 'Search'
        db.delete_table(u'search_search')

        # Removing M2M table for field instrument_type on 'Search'
        db.delete_table(db.shorten_name(u'search_search_instrument_type'))

        # Removing M2M table for field satellite on 'Search'
        db.delete_table(db.shorten_name(u'search_search_satellite'))

        # Removing M2M table for field license_type on 'Search'
        db.delete_table(db.shorten_name(u'search_search_license_type'))

        # Removing M2M table for field spectral_group on 'Search'
        db.delete_table(db.shorten_name(u'search_search_spectral_group'))

        # Removing M2M table for field processing_level on 'Search'
        db.delete_table(db.shorten_name(u'search_search_processing_level'))

        # Removing M2M table for field collection on 'Search'
        db.delete_table(db.shorten_name(u'search_search_collection'))

        # Deleting model 'SearchDateRange'
        db.delete_table(u'search_searchdaterange')

        # Deleting model 'Clip'
        db.delete_table(u'search_clip')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'catalogue.genericproduct': {
            'Meta': {'ordering': "('-product_date',)", 'object_name': 'GenericProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingestion_log': ('django.db.models.fields.TextField', [], {}),
            'local_storage_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {}),
            'original_product_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'product_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'projection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.Projection']"}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.Quality']"}),
            'remote_thumbnail_url': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'spatial_coverage': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'unique_product_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dictionaries.collection': {
            'Meta': {'ordering': "['name']", 'object_name': 'Collection'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.Institution']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dictionaries.institution': {
            'Meta': {'object_name': 'Institution'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'dictionaries.instrumenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'InstrumentType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'band_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'band_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'base_processing_level': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'base_processing_level'", 'null': 'True', 'to': u"orm['dictionaries.ProcessingLevel']"}),
            'default_processing_level': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_processing_level'", 'null': 'True', 'to': u"orm['dictionaries.ProcessingLevel']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_size_km': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_radar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_taskable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'operator_abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pixel_size_list_m': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'processing_software': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'quantization_bits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reference_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.ReferenceSystem']", 'null': 'True', 'blank': 'True'}),
            'scanner_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.ScannerType']"}),
            'spatial_resolution_range': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'spectral_range_list_nm': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'swath_optical_km': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dictionaries.license': {
            'Meta': {'object_name': 'License'},
            'details': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        u'dictionaries.processinglevel': {
            'Meta': {'ordering': "['abbreviation']", 'object_name': 'ProcessingLevel'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dictionaries.productprocessstate': {
            'Meta': {'object_name': 'ProductProcessState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'dictionaries.projection': {
            'Meta': {'ordering': "('epsg_code', 'name')", 'object_name': 'Projection'},
            'epsg_code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'dictionaries.quality': {
            'Meta': {'object_name': 'Quality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"})
        },
        u'dictionaries.referencesystem': {
            'Meta': {'ordering': "['name']", 'object_name': 'ReferenceSystem'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dictionaries.satellite': {
            'Meta': {'ordering': "['name']", 'object_name': 'Satellite'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'altitude_km': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.Collection']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launch_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'operator_abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'orbit': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'revisit_time_days': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dictionaries.scannertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ScannerType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dictionaries.spectralgroup': {
            'Meta': {'ordering': "['abbreviation', 'name']", 'object_name': 'SpectralGroup'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dictionaries.subsidytype': {
            'Meta': {'object_name': 'SubsidyType'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'exchange.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'orders.datum': {
            'Meta': {'ordering': "['name']", 'object_name': 'Datum'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'orders.deliverymethod': {
            'Meta': {'ordering': "['name']", 'object_name': 'DeliveryMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'orders.fileformat': {
            'Meta': {'ordering': "['name']", 'object_name': 'FileFormat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'orders.marketsector': {
            'Meta': {'ordering': "['name']", 'object_name': 'MarketSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'orders.order': {
            'Meta': {'ordering': "['-order_date']", 'object_name': 'Order'},
            'datum': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['orders.Datum']"}),
            'delivery_method': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['orders.DeliveryMethod']"}),
            'file_format': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['orders.FileFormat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_sector': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['orders.MarketSector']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'order_status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['orders.OrderStatus']"}),
            'resampling_method': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': u"orm['orders.ResamplingMethod']"}),
            'subsidy_type_assigned': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsidy_type+'", 'null': 'True', 'to': u"orm['dictionaries.SubsidyType']"}),
            'subsidy_type_requested': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subsidy_type+'", 'null': 'True', 'to': u"orm['dictionaries.SubsidyType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'orders.orderstatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'OrderStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'orders.resamplingmethod': {
            'Meta': {'ordering': "['name']", 'object_name': 'ResamplingMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'search.clip': {
            'Meta': {'object_name': 'Clip'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'result_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'search.search': {
            'Meta': {'ordering': "('search_date',)", 'object_name': 'Search'},
            'band_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cloud_mean': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.Collection']", 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.InstrumentType']", 'null': 'True', 'blank': 'True'}),
            'ip_position': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'j_frame_row': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'k_orbit_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.License']", 'null': 'True', 'blank': 'True'}),
            'processing_level': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.ProcessingLevel']", 'null': 'True', 'blank': 'True'}),
            'record_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'satellite': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.Satellite']", 'null': 'True', 'blank': 'True'}),
            'search_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'sensor_inclination_angle_end': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor_inclination_angle_start': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'spatial_resolution': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spectral_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.SpectralGroup']", 'null': 'True', 'blank': 'True'}),
            'use_cloud_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'search.searchdaterange': {
            'Meta': {'object_name': 'SearchDateRange'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Search']"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'search.searchrecord': {
            'Meta': {'object_name': 'SearchRecord'},
            'cost_per_scene': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']", 'null': 'True', 'blank': 'True'}),
            'download_path': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_order_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']", 'null': 'True', 'blank': 'True'}),
            'processing_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.ProcessingLevel']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.GenericProduct']"}),
            'product_process_state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.ProductProcessState']", 'null': 'True', 'blank': 'True'}),
            'product_ready': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'projection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.Projection']", 'null': 'True', 'blank': 'True'}),
            'rand_cost_per_scene': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['search']