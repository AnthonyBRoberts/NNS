# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Reporter.user'
        db.delete_column('polls_reporter', 'user_id')

        # Adding field 'Reporter.user_ptr'
        db.add_column('polls_reporter', 'user_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['auth.User'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Editor.user'
        db.delete_column('polls_editor', 'user_id')

        # Adding field 'Editor.user_ptr'
        db.add_column('polls_editor', 'user_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=4, to=orm['auth.User'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Client.user'
        db.delete_column('polls_client', 'user_id')

        # Adding field 'Client.user_ptr'
        db.add_column('polls_client', 'user_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=6, to=orm['auth.User'], unique=True, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Reporter.user'
        db.add_column('polls_reporter', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='reporter', unique=True, primary_key=True, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Reporter.user_ptr'
        db.delete_column('polls_reporter', 'user_ptr_id')

        # Adding field 'Editor.user'
        db.add_column('polls_editor', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=3, related_name='editor', unique=True, primary_key=True, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Editor.user_ptr'
        db.delete_column('polls_editor', 'user_ptr_id')

        # Adding field 'Client.user'
        db.add_column('polls_client', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=5, related_name='client', unique=True, primary_key=True, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Client.user_ptr'
        db.delete_column('polls_client', 'user_ptr_id')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        'polls.client': {
            'Meta': {'object_name': 'Client', '_ormbases': ['auth.User']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pub_area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'polls.editor': {
            'Meta': {'object_name': 'Editor', '_ormbases': ['auth.User']},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'can_publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'polls.reporter': {
            'Meta': {'object_name': 'Reporter', '_ormbases': ['auth.User']},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['polls']