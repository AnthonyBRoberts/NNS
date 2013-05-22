# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Editor'
        db.delete_table('account_editor')

        # Deleting model 'Client'
        db.delete_table('account_client')

        # Deleting model 'Reporter'
        db.delete_table('account_reporter')

        # Adding field 'UserProfile.can_publish'
        db.add_column('account_userprofile', 'can_publish',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.bio'
        db.add_column('account_userprofile', 'bio',
                      self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.byline'
        db.add_column('account_userprofile', 'byline',
                      self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.address'
        db.add_column('account_userprofile', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.city'
        db.add_column('account_userprofile', 'city',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.state'
        db.add_column('account_userprofile', 'state',
                      self.gf('django.contrib.localflavor.us.models.USStateField')(default='NE', max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.zipcode'
        db.add_column('account_userprofile', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.phone'
        db.add_column('account_userprofile', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.pub_area'
        db.add_column('account_userprofile', 'pub_area',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.twitter'
        db.add_column('account_userprofile', 'twitter',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.facebook'
        db.add_column('account_userprofile', 'facebook',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.website'
        db.add_column('account_userprofile', 'website',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)


        # Changing field 'UserProfile.about'
        db.alter_column('account_userprofile', 'about', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Adding model 'Editor'
        db.create_table('account_editor', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.UserProfile'], unique=True, primary_key=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('can_publish', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('account', ['Editor'])

        # Adding model 'Client'
        db.create_table('account_client', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.UserProfile'], unique=True, primary_key=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(default='NE', max_length=2)),
            ('pub_area', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('account', ['Client'])

        # Adding model 'Reporter'
        db.create_table('account_reporter', (
            ('userprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.UserProfile'], unique=True, primary_key=True)),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=75)),
        ))
        db.send_create_signal('account', ['Reporter'])

        # Deleting field 'UserProfile.can_publish'
        db.delete_column('account_userprofile', 'can_publish')

        # Deleting field 'UserProfile.bio'
        db.delete_column('account_userprofile', 'bio')

        # Deleting field 'UserProfile.byline'
        db.delete_column('account_userprofile', 'byline')

        # Deleting field 'UserProfile.address'
        db.delete_column('account_userprofile', 'address')

        # Deleting field 'UserProfile.city'
        db.delete_column('account_userprofile', 'city')

        # Deleting field 'UserProfile.state'
        db.delete_column('account_userprofile', 'state')

        # Deleting field 'UserProfile.zipcode'
        db.delete_column('account_userprofile', 'zipcode')

        # Deleting field 'UserProfile.phone'
        db.delete_column('account_userprofile', 'phone')

        # Deleting field 'UserProfile.pub_area'
        db.delete_column('account_userprofile', 'pub_area')

        # Deleting field 'UserProfile.twitter'
        db.delete_column('account_userprofile', 'twitter')

        # Deleting field 'UserProfile.facebook'
        db.delete_column('account_userprofile', 'facebook')

        # Deleting field 'UserProfile.website'
        db.delete_column('account_userprofile', 'website')


        # Changing field 'UserProfile.about'
        db.alter_column('account_userprofile', 'about', self.gf('django.db.models.fields.TextField')(default=''))

    models = {
        'account.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'can_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pub_area': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'default': "'NE'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'Client'", 'max_length': '10'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
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