# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AlertMailLog'
        db.create_table('signin_alertmaillog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_addr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('to_addr', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('email_body', self.gf('django.db.models.fields.TextField')()),
            ('clinic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Clinic'])),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('signin', ['AlertMailLog'])

        # Adding model 'AlertEventMap'
        db.create_table('signin_alerteventmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alert_conf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.AlertConfiguration'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Event'])),
        ))
        db.send_create_signal('signin', ['AlertEventMap'])

        # Adding model 'AlertConfiguration'
        db.create_table('signin_alertconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=10)),
            ('clinic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Clinic'])),
            ('from_addr', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('to_addr', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('waiting_time', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 6, 1, 13, 24, 3, 43886))),
        ))
        db.send_create_signal('signin', ['AlertConfiguration'])


    def backwards(self, orm):
        
        # Deleting model 'AlertMailLog'
        db.delete_table('signin_alertmaillog')

        # Deleting model 'AlertEventMap'
        db.delete_table('signin_alerteventmap')

        # Deleting model 'AlertConfiguration'
        db.delete_table('signin_alertconfiguration')


    models = {
        'signin.alertconfiguration': {
            'Meta': {'object_name': 'AlertConfiguration'},
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Clinic']"}),
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 6, 1, 13, 24, 3, 43886)'}),
            'enabled': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'from_addr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'to_addr': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'waiting_time': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        'signin.alerteventmap': {
            'Meta': {'object_name': 'AlertEventMap'},
            'alert_conf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.AlertConfiguration']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'signin.alertmaillog': {
            'Meta': {'object_name': 'AlertMailLog'},
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Clinic']"}),
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_body': ('django.db.models.fields.TextField', [], {}),
            'from_addr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_addr': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
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
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 6, 1, 13, 24, 3, 38836)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Patient']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Provider']", 'null': 'True', 'blank': 'True'})
        },
        'signin.interrupt': {
            'Meta': {'object_name': 'Interrupt'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'signin.location': {
            'Meta': {'object_name': 'Location'},
            'appointment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'EST'", 'max_length': '100'})
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
        'signin.patientinterruptlog': {
            'Meta': {'object_name': 'PatientInterruptLog'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.EventSetHeader']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interrupt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Interrupt']"}),
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
            'interrupttype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Interrupt']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'signin.provider': {
            'Meta': {'object_name': 'Provider'},
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'loc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Location']", 'null': 'True'})
        },
        'signin.settings_general': {
            'Meta': {'object_name': 'Settings_General'},
            'argument1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'argument2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'argument3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'argument4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'change_time': ('django.db.models.fields.DateTimeField', [], {}),
            'enable_disable': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '4'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['signin']
