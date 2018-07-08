# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'AlertMailLog.to_addr'
        db.delete_column('signin_alertmaillog', 'to_addr')

        # Deleting field 'AlertMailLog.clinic'
        db.delete_column('signin_alertmaillog', 'clinic')

        # Deleting field 'AlertMailLog.waiting_event'
        db.delete_column('signin_alertmaillog', 'waiting_event')

        # Deleting field 'AlertMailLog.from_addr'
        db.delete_column('signin_alertmaillog', 'from_addr')

        # Deleting field 'AlertMailLog.patient_firstname'
        db.delete_column('signin_alertmaillog', 'patient_firstname')

        # Deleting field 'AlertMailLog.patient_lastname'
        db.delete_column('signin_alertmaillog', 'patient_lastname')

        # Deleting field 'AlertMailLog.patient_id'
        db.delete_column('signin_alertmaillog', 'patient_id')

        # Deleting field 'AlertMailLog.location'
        db.delete_column('signin_alertmaillog', 'location')

        # Adding field 'AlertMailLog.rule_matched'
        db.add_column('signin_alertmaillog', 'rule_matched', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.AlertConfiguration'], null=True, blank=True), keep_default=False)

        # Adding field 'AlertMailLog.patient'
        db.add_column('signin_alertmaillog', 'patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Patient'], null=True, blank=True), keep_default=False)

        # Adding field 'AlertMailLog.iteration'
        db.add_column('signin_alertmaillog', 'iteration', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3), keep_default=False)

        # Changing field 'AlertMailLog.dateTime'
        db.alter_column('signin_alertmaillog', 'dateTime', self.gf('django.db.models.fields.DateTimeField')())


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'AlertMailLog.to_addr'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.to_addr' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.clinic'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.clinic' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.waiting_event'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.waiting_event' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.from_addr'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.from_addr' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.patient_firstname'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.patient_firstname' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.patient_lastname'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.patient_lastname' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.patient_id'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.patient_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AlertMailLog.location'
        raise RuntimeError("Cannot reverse this migration. 'AlertMailLog.location' and its values cannot be restored.")

        # Deleting field 'AlertMailLog.rule_matched'
        db.delete_column('signin_alertmaillog', 'rule_matched_id')

        # Deleting field 'AlertMailLog.patient'
        db.delete_column('signin_alertmaillog', 'patient_id')

        # Deleting field 'AlertMailLog.iteration'
        db.delete_column('signin_alertmaillog', 'iteration')

        # Changing field 'AlertMailLog.dateTime'
        db.alter_column('signin_alertmaillog', 'dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))


    models = {
        'signin.alertconfiguration': {
            'Meta': {'object_name': 'AlertConfiguration'},
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Clinic']"}),
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 6, 29, 9, 59, 22, 485558)'}),
            'enabled': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'event_list': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'from_addr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'to_addr': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'waiting_time': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        'signin.alertmaillog': {
            'Meta': {'object_name': 'AlertMailLog'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 6, 29, 9, 59, 22, 486690)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Patient']", 'null': 'True', 'blank': 'True'}),
            'rule_matched': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.AlertConfiguration']", 'null': 'True', 'blank': 'True'})
        },
        'signin.clinic': {
            'Meta': {'object_name': 'Clinic'},
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)', 'blank': 'True'})
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
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 6, 29, 9, 59, 22, 467074)'}),
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
