# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Notifier_Settings.alert_mail_subject'
        db.add_column('signin_notifier_settings', 'alert_mail_subject', self.gf('django.db.models.fields.CharField')(default='Alert :- Patient {fname} is still waiting to be  processed...', max_length=100), keep_default=False)

        # Changing field 'Notifier_Settings.time_hours'
        db.alter_column('signin_notifier_settings', 'time_hours', self.gf('django.db.models.fields.IntegerField')(max_length=16))

        # Changing field 'Notifier_Settings.time_mins'
        db.alter_column('signin_notifier_settings', 'time_mins', self.gf('django.db.models.fields.IntegerField')(max_length=16))


    def backwards(self, orm):
        
        # Deleting field 'Notifier_Settings.alert_mail_subject'
        db.delete_column('signin_notifier_settings', 'alert_mail_subject')

        # Changing field 'Notifier_Settings.time_hours'
        db.alter_column('signin_notifier_settings', 'time_hours', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Changing field 'Notifier_Settings.time_mins'
        db.alter_column('signin_notifier_settings', 'time_mins', self.gf('django.db.models.fields.CharField')(max_length=4))


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
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 5, 20, 23, 27, 3, 99213)'}),
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
        'signin.notifier_settings': {
            'Meta': {'object_name': 'Notifier_Settings'},
            'alert_mail_subject': ('django.db.models.fields.CharField', [], {'default': "'Alert :- Patient {fname} is still waiting to be  processed...'", 'max_length': '100'}),
            'changed_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 5, 20, 23, 27, 3, 95062)'}),
            'enable_disable': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '4'}),
            'from_mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_hours': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '16'}),
            'time_mins': ('django.db.models.fields.IntegerField', [], {'default': '10', 'max_length': '16'}),
            'to_mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
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
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'signin.testdateinfo': {
            'Meta': {'object_name': 'Testdateinfo'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['signin']
