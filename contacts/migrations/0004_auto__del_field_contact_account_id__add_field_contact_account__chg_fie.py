# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Contact.account_id'
        db.delete_column('contacts_contact', 'account_id_id')

        # Adding field 'Contact.account'
        db.add_column('contacts_contact', 'account',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field tag_ids on 'Contact'
        db.delete_table('contacts_contact_tag_ids')

        # Adding M2M table for field tags on 'Contact'
        db.create_table('contacts_contact_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['contacts.contact'], null=False)),
            ('tag', models.ForeignKey(orm['contacts.tag'], null=False))
        ))
        db.create_unique('contacts_contact_tags', ['contact_id', 'tag_id'])


        # Changing field 'Contact.last_name'
        db.alter_column('contacts_contact', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Contact.email'
        db.alter_column('contacts_contact', 'email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True))

        # Changing field 'Contact.phone_primary'
        db.alter_column('contacts_contact', 'phone_primary', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True))

    def backwards(self, orm):
        # Adding field 'Contact.account_id'
        db.add_column('contacts_contact', 'account_id',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.Account'], unique=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Contact.account'
        db.delete_column('contacts_contact', 'account_id')

        # Adding M2M table for field tag_ids on 'Contact'
        db.create_table('contacts_contact_tag_ids', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm['contacts.contact'], null=False)),
            ('tag', models.ForeignKey(orm['contacts.tag'], null=False))
        ))
        db.create_unique('contacts_contact_tag_ids', ['contact_id', 'tag_id'])

        # Removing M2M table for field tags on 'Contact'
        db.delete_table('contacts_contact_tags')


        # Changing field 'Contact.last_name'
        db.alter_column('contacts_contact', 'last_name', self.gf('django.db.models.fields.CharField')(default='Last', max_length=255))

        # Changing field 'Contact.email'
        db.alter_column('contacts_contact', 'email', self.gf('django.db.models.fields.EmailField')(default='a@b.com', max_length=255))

        # Changing field 'Contact.phone_primary'
        db.alter_column('contacts_contact', 'phone_primary', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

    models = {
        'account.account': {
            'Meta': {'object_name': 'Account'},
            'admin': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
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
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone_primary': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['contacts.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'contacts.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contacts.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['contacts']