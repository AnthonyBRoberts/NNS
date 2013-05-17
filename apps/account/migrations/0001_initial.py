# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('account_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('account', ['UserProfile'])

        # Adding model 'Editor'
        db.create_table('account_editor', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.UserProfile'], unique=True, primary_key=True)),
            ('can_publish', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=2000)),
        ))
        db.send_create_signal('account', ['Editor'])

        # Adding model 'Reporter'
        db.create_table('account_reporter', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.UserProfile'], unique=True, primary_key=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal('account', ['Reporter'])

        # Adding model 'Client'
        db.create_table('account_client', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.UserProfile'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(default='NE', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pub_area', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('account', ['Client'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('account_userprofile')

        # Deleting model 'Editor'
        db.delete_table('account_editor')

        # Deleting model 'Reporter'
        db.delete_table('account_reporter')

        # Deleting model 'Client'
        db.delete_table('account_client')


    models = {
        'account.client': {
            'Meta': {'object_name': 'Client', '_ormbases': ['account.UserProfile']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pub_area': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'default': "'NE'", 'max_length': '2'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['account.UserProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        'account.editor': {
            'Meta': {'object_name': 'Editor', '_ormbases': ['account.UserProfile']},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'can_publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['account.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'account.reporter': {
            'Meta': {'object_name': 'Reporter', '_ormbases': ['account.UserProfile']},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'userprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['account.UserProfile']", 'unique': 'True', 'primary_key': 'True'})
        },
        'account.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']