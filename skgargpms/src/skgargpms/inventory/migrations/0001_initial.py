# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Item'
        db.create_table('inventory_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('manufacturernumber', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Item'])

        # Adding model 'ItemPack'
        db.create_table('inventory_itempack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('inventory', ['ItemPack'])

        # Adding model 'ItemsforItemPack'
        db.create_table('inventory_itemsforitempack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('packId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemPack'])),
            ('itemId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
        ))
        db.send_create_signal('inventory', ['ItemsforItemPack'])

        # Adding model 'ItemsOpenedSession'
        db.create_table('inventory_itemsopenedsession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('providerId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Provider'])),
            ('patientId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['signin.Patient'])),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['ItemsOpenedSession'])

        # Adding model 'ItemsOpened'
        db.create_table('inventory_itemsopened', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sessionId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemsOpenedSession'])),
            ('itemId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dateTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['ItemsOpened'])


    def backwards(self, orm):
        
        # Deleting model 'Item'
        db.delete_table('inventory_item')

        # Deleting model 'ItemPack'
        db.delete_table('inventory_itempack')

        # Deleting model 'ItemsforItemPack'
        db.delete_table('inventory_itemsforitempack')

        # Deleting model 'ItemsOpenedSession'
        db.delete_table('inventory_itemsopenedsession')

        # Deleting model 'ItemsOpened'
        db.delete_table('inventory_itemsopened')


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
        'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturernumber': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'inventory.itempack': {
            'Meta': {'object_name': 'ItemPack'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inventory.itemsforitempack': {
            'Meta': {'object_name': 'ItemsforItemPack'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Item']"}),
            'packId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.ItemPack']"})
        },
        'inventory.itemsopened': {
            'Meta': {'object_name': 'ItemsOpened'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Item']"}),
            'sessionId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.ItemsOpenedSession']"}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'inventory.itemsopenedsession': {
            'Meta': {'object_name': 'ItemsOpenedSession'},
            'dateTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patientId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Patient']"}),
            'providerId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signin.Provider']"}),
            'userId': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'signin.patient': {
            'Meta': {'object_name': 'Patient'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'signin.provider': {
            'Meta': {'object_name': 'Provider'},
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['inventory']
