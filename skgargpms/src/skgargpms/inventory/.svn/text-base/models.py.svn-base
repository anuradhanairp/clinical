from django.db import models

from django.contrib.auth.models import User

from signin.models import Patient,Provider
# Create your models here.


class Item(models.Model):
    'Name and other details of the Item'
    
    name = models.CharField(max_length=100,blank=False,null=False)
    type = models.CharField(max_length=100,blank=True,null=True)
    manufacturer = models.CharField(max_length=100,blank=True,null=True)
    manufacturernumber = models.CharField(max_length=100,blank=True,null=True)
    

class ItemPack(models.Model):
    'To group Items '
    
    name = models.CharField(max_length=100,blank=False,null=False)
    

class ItemsforItemPack(models.Model):
    'The mapping of Items and Itempack'
    
    packId = models.ForeignKey(ItemPack)
    itemId = models.ForeignKey(Item)
    
class ItemsOpenedSession(models.Model):
    'Get the Bind Patient,User and provider info'
    
    userId = models.ForeignKey(User)
    providerId = models.ForeignKey(Provider)
    patientId  = models.ForeignKey(Patient)
    dateTime   = models.DateTimeField(auto_now_add = True)
    

class ItemsOpened(models.Model):
    
    'Track Items opened and utilized by the patient'
    
    sessionId = models.ForeignKey(ItemsOpenedSession)
    itemId    = models.ForeignKey(Item)
    used      = models.BooleanField(default=False)
    dateTime  = models.DateTimeField(auto_now_add = True)    
    
    
    