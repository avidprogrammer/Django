# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table(u'contacts_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'contacts', ['Address'])

        # Adding model 'Contact'
        db.create_table(u'contacts_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'contacts', ['Contact'])

        # Adding model 'Bill'
        db.create_table(u'contacts_bill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('ship_date', self.gf('django.db.models.fields.DateField')()),
            ('item', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'contacts', ['Bill'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table(u'contacts_address')

        # Deleting model 'Contact'
        db.delete_table(u'contacts_contact')

        # Deleting model 'Bill'
        db.delete_table(u'contacts_bill')


    models = {
        u'contacts.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'contacts.bill': {
            'Meta': {'object_name': 'Bill'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.TextField', [], {}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'ship_date': ('django.db.models.fields.DateField', [], {})
        },
        u'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['contacts']