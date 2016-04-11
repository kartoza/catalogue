# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Datum'
        db.create_table(u'orders_datum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'orders', ['Datum'])

        # Adding model 'ResamplingMethod'
        db.create_table(u'orders_resamplingmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'orders', ['ResamplingMethod'])

        # Adding model 'FileFormat'
        db.create_table(u'orders_fileformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'orders', ['FileFormat'])

        # Adding model 'OrderStatus'
        db.create_table(u'orders_orderstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'orders', ['OrderStatus'])

        # Adding model 'DeliveryMethod'
        db.create_table(u'orders_deliverymethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'orders', ['DeliveryMethod'])

        # Adding model 'MarketSector'
        db.create_table(u'orders_marketsector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal(u'orders', ['MarketSector'])

        # Adding model 'Order'
        db.create_table(u'orders_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order_status', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['orders.OrderStatus'])),
            ('delivery_method', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['orders.DeliveryMethod'])),
            ('market_sector', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['orders.MarketSector'])),
            ('order_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('datum', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['orders.Datum'])),
            ('resampling_method', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['orders.ResamplingMethod'])),
            ('file_format', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['orders.FileFormat'])),
            ('subsidy_type_requested', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subsidy_type+', null=True, to=orm['dictionaries.SubsidyType'])),
            ('subsidy_type_assigned', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subsidy_type+', null=True, to=orm['dictionaries.SubsidyType'])),
        ))
        db.send_create_signal(u'orders', ['Order'])

        # Adding model 'OrderStatusHistory'
        db.create_table(u'orders_orderstatushistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'])),
            ('order_change_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('old_order_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='old_order_status', to=orm['orders.OrderStatus'])),
            ('new_order_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='new_order_status', to=orm['orders.OrderStatus'])),
        ))
        db.send_create_signal(u'orders', ['OrderStatusHistory'])

        # Adding model 'OrderNotificationRecipients'
        db.create_table(u'orders_ordernotificationrecipients', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'orders', ['OrderNotificationRecipients'])

        # Adding M2M table for field satellite_instrument_group on 'OrderNotificationRecipients'
        m2m_table_name = db.shorten_name(u'orders_ordernotificationrecipients_satellite_instrument_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordernotificationrecipients', models.ForeignKey(orm[u'orders.ordernotificationrecipients'], null=False)),
            ('satelliteinstrumentgroup', models.ForeignKey(orm[u'dictionaries.satelliteinstrumentgroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ordernotificationrecipients_id', 'satelliteinstrumentgroup_id'])

        # Adding M2M table for field classes on 'OrderNotificationRecipients'
        m2m_table_name = db.shorten_name(u'orders_ordernotificationrecipients_classes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ordernotificationrecipients', models.ForeignKey(orm[u'orders.ordernotificationrecipients'], null=False)),
            ('contenttype', models.ForeignKey(orm[u'contenttypes.contenttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ordernotificationrecipients_id', 'contenttype_id'])

        # Adding model 'NonSearchRecord'
        db.create_table(u'orders_nonsearchrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'], null=True, blank=True)),
            ('product_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('download_path', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('cost_per_scene', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('rand_cost_per_scene', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency'], null=True, blank=True)),
        ))
        db.send_create_signal(u'orders', ['NonSearchRecord'])


    def backwards(self, orm):
        # Deleting model 'Datum'
        db.delete_table(u'orders_datum')

        # Deleting model 'ResamplingMethod'
        db.delete_table(u'orders_resamplingmethod')

        # Deleting model 'FileFormat'
        db.delete_table(u'orders_fileformat')

        # Deleting model 'OrderStatus'
        db.delete_table(u'orders_orderstatus')

        # Deleting model 'DeliveryMethod'
        db.delete_table(u'orders_deliverymethod')

        # Deleting model 'MarketSector'
        db.delete_table(u'orders_marketsector')

        # Deleting model 'Order'
        db.delete_table(u'orders_order')

        # Deleting model 'OrderStatusHistory'
        db.delete_table(u'orders_orderstatushistory')

        # Deleting model 'OrderNotificationRecipients'
        db.delete_table(u'orders_ordernotificationrecipients')

        # Removing M2M table for field satellite_instrument_group on 'OrderNotificationRecipients'
        db.delete_table(db.shorten_name(u'orders_ordernotificationrecipients_satellite_instrument_group'))

        # Removing M2M table for field classes on 'OrderNotificationRecipients'
        db.delete_table(db.shorten_name(u'orders_ordernotificationrecipients_classes'))

        # Deleting model 'NonSearchRecord'
        db.delete_table(u'orders_nonsearchrecord')


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
        u'dictionaries.satelliteinstrumentgroup': {
            'Meta': {'ordering': "['satellite', 'instrument_type']", 'unique_together': "(('satellite', 'instrument_type'),)", 'object_name': 'SatelliteInstrumentGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.InstrumentType']"}),
            'satellite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dictionaries.Satellite']"})
        },
        u'dictionaries.scannertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ScannerType'},
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
        u'orders.nonsearchrecord': {
            'Meta': {'object_name': 'NonSearchRecord'},
            'cost_per_scene': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']", 'null': 'True', 'blank': 'True'}),
            'download_path': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']", 'null': 'True', 'blank': 'True'}),
            'product_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rand_cost_per_scene': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        u'orders.ordernotificationrecipients': {
            'Meta': {'ordering': "['user']", 'object_name': 'OrderNotificationRecipients'},
            'classes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'satellite_instrument_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dictionaries.SatelliteInstrumentGroup']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'orders.orderstatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'OrderStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'orders.orderstatushistory': {
            'Meta': {'ordering': "('-order_change_date',)", 'object_name': 'OrderStatusHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_order_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_order_status'", 'to': u"orm['orders.OrderStatus']"}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'old_order_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'old_order_status'", 'to': u"orm['orders.OrderStatus']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']"}),
            'order_change_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'orders.resamplingmethod': {
            'Meta': {'ordering': "['name']", 'object_name': 'ResamplingMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['orders']