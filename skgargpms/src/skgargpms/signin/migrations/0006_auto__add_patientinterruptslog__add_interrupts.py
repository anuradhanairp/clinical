# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PatientInterruptsLog'
        db.create_table('signin_patientinterruptslog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interrupt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Interrupts'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.EventSetHeader'])),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('signin', ['PatientInterruptsLog'])

        # Adding model 'Interrupts'
        db.create_table('signin_interrupts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('signin', ['Interrupts'])


    def backwards(self, orm):
        
        # Deleting model 'PatientInterruptsLog'
        db.delete_table('signin_patientinterruptslog')

        # Deleting model 'Interrupts'
        db.delete_table('signin_interrupts')


    models = {
        'signin.clinic': {
            'Meta': {'object_name': 'Clinic'},
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)', 'blank': 'True'}),
            'work_time': ('django.db.models.fields.CharField', [], {'default': "'morning'", 'max_length': '32'})
        },
        'signin.cliniceventmap': {
            'Meta': {'object_name': 'ClinicEventMap'},
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Clinic']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
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
        'signin.interrupts': {
            'Meta': {'object_name': 'Interrupts'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
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
        'signin.patientinterruptslog': {
            'Meta': {'object_name': 'PatientInterruptsLog'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.EventSetHeader']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interrupt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Interrupts']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
