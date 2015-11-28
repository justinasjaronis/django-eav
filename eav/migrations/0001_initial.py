# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EnumValue'
        db.create_table(u'eav_enumvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal(u'eav', ['EnumValue'])

        # Adding model 'EnumGroup'
        db.create_table(u'eav_enumgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'eav', ['EnumGroup'])

        # Adding M2M table for field enums on 'EnumGroup'
        m2m_table_name = db.shorten_name(u'eav_enumgroup_enums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enumgroup', models.ForeignKey(orm[u'eav.enumgroup'], null=False)),
            ('enumvalue', models.ForeignKey(orm[u'eav.enumvalue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enumgroup_id', 'enumvalue_id'])

        # Adding model 'Attribute'
        db.create_table(u'eav_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('slug', self.gf('eav.fields.EavSlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('enum_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eav.EnumGroup'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('datatype', self.gf('eav.fields.EavDatatypeField')(max_length=6)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'eav', ['Attribute'])

        # Adding unique constraint on 'Attribute', fields ['site', 'slug']
        db.create_unique(u'eav_attribute', ['site_id', 'slug'])

        # Adding model 'Value'
        db.create_table(u'eav_value', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity_ct', self.gf('django.db.models.fields.related.ForeignKey')(related_name='value_entities', to=orm['contenttypes.ContentType'])),
            ('entity_id', self.gf('django.db.models.fields.IntegerField')()),
            ('value_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('value_float', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('value_int', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('value_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('value_bool', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('value_enum', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='eav_values', null=True, to=orm['eav.EnumValue'])),
            ('generic_value_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('generic_value_ct', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='value_values', null=True, to=orm['contenttypes.ContentType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eav.Attribute'])),
        ))
        db.send_create_signal(u'eav', ['Value'])


    def backwards(self, orm):
        # Removing unique constraint on 'Attribute', fields ['site', 'slug']
        db.delete_unique(u'eav_attribute', ['site_id', 'slug'])

        # Deleting model 'EnumValue'
        db.delete_table(u'eav_enumvalue')

        # Deleting model 'EnumGroup'
        db.delete_table(u'eav_enumgroup')

        # Removing M2M table for field enums on 'EnumGroup'
        db.delete_table(db.shorten_name(u'eav_enumgroup_enums'))

        # Deleting model 'Attribute'
        db.delete_table(u'eav_attribute')

        # Deleting model 'Value'
        db.delete_table(u'eav_value')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'eav.attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Attribute'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'datatype': ('eav.fields.EavDatatypeField', [], {'max_length': '6'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'enum_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eav.EnumGroup']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('eav.fields.EavSlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'eav.enumgroup': {
            'Meta': {'object_name': 'EnumGroup'},
            'enums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['eav.EnumValue']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'eav.enumvalue': {
            'Meta': {'object_name': 'EnumValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        u'eav.value': {
            'Meta': {'object_name': 'Value'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['eav.Attribute']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'entity_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_entities'", 'to': u"orm['contenttypes.ContentType']"}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'generic_value_ct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_values'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'generic_value_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value_enum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eav_values'", 'null': 'True', 'to': u"orm['eav.EnumValue']"}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['eav']