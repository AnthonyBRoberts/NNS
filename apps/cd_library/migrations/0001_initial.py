# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CD'
        db.create_table('cd_library_cd', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('genre', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('cd_library', ['CD'])


    def backwards(self, orm):
        # Deleting model 'CD'
        db.delete_table('cd_library_cd')


    models = {
        'cd_library.cd': {
            'Meta': {'object_name': 'CD'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cd_library']