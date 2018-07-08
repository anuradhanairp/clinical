# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('signin_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('signin', ['Location'])

        # Adding model 'Clinic'
        db.create_table('signin_clinic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Location'])),
            ('work_time', self.gf('django.db.models.fields.CharField')(default='morning', max_length=32)),
        ))
        db.send_create_signal('signin', ['Clinic'])

        # Adding model 'Event'
        db.create_table('signin_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('signin', ['Event'])

        # Adding model 'Patient'
        db.create_table('signin_patient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('signin', ['Patient'])

        # Adding model 'Provider'
        db.create_table('signin_provider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lName', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('signin', ['Provider'])

        # Adding model 'EventSetHeader'
        db.create_table('signin_eventsetheader', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Patient'])),
            ('clinic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Clinic'])),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Provider'], null=True, blank=True)),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('signin', ['EventSetHeader'])

        # Adding model 'PatientEventLog'
        db.create_table('signin_patienteventlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Event'])),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.EventSetHeader'])),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('signin', ['PatientEventLog'])

        # Adding model 'Payment'
        db.create_table('signin_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.EventSetHeader'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('signin', ['Payment'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('signin_location')

        # Deleting model 'Clinic'
        db.delete_table('signin_clinic')

        # Deleting model 'Event'
        db.delete_table('signin_event')

        # Deleting model 'Patient'
        db.delete_table('signin_patient')

        # Deleting model 'Provider'
        db.delete_table('signin_provider')

        # Deleting model 'EventSetHeader'
        db.delete_table('signin_eventsetheader')

        # Deleting model 'PatientEventLog'
        db.delete_table('signin_patienteventlog')

        # Deleting model 'Payment'
        db.delete_table('signin_payment')


    models = {
        'signin.clinic': {
            'Meta': {'object_name': 'Clinic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'work_time': ('django.db.models.fields.CharField', [], {'default': "'morning'", 'max_length': '32'})
        },
        'signin.event': {
            'Meta': {'object_name': 'Event'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'signin.eventsetheader': {
            'Meta': {'object_name': 'EventSetHeader'},
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Clinic']"}),
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Patient']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Provider']", 'null': 'True', 'blank': 'True'})
        },
        'signin.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'signin.patient': {
            'Meta': {'object_name': 'Patient'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'signin.patienteventlog': {
            'Meta': {'object_name': 'PatientEventLog'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Event']"}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.EventSetHeader']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'signin.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.EventSetHeader']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'signin.provider': {
            'Meta': {'object_name': 'Provider'},
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['signin']
