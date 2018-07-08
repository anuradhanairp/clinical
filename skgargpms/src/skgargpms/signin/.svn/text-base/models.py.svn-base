# -*- coding: utf-8 -*-
from django.db import models
import datetime
from djcelery.models import PeriodicTask

class Settings_General(models.Model):
     '''general settings table '''
     FIELD_CHOICES = (
                    ('notifier', 'notifier'),
                    )
     ENABLE_CHOICES = (
                ('Yes', 'Enable'),
                ('No', 'Disable'),)
     field_type = models.CharField(max_length = 16, choices = FIELD_CHOICES)
     enable_disable = models.CharField(max_length = 4, choices = ENABLE_CHOICES, default = 'Yes')
     argument1 = models.CharField(max_length = 16, default = '')
     argument2 = models.CharField(max_length = 200, default = '')
     argument3 = models.CharField(max_length = 16, default = '')
     argument4 = models.CharField(max_length = 200, default = '')
     change_time = models.DateTimeField()

class Location(models.Model):
    '''
    Hospital Location.
    '''
    
    TIMEZONES = (
            ('America/Chicago', 'America/Chicago'),
            ('America/Yakutat', 'America/Yakutat'),
            ('EST', 'EST'),
        )
    
    'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US/East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Pacific-New', 'US/Samoa',
    name = models.CharField(max_length = 100)
    timezone = models.CharField(max_length = 100, choices = TIMEZONES, default = 'EST')
    appointment = models.BooleanField(default = False)
    
    provider_required = models.BooleanField(default = False)
    
    dob_required = models.BooleanField(default = False)
    
    
    def __unicode__(self):
        return self.name

class Clinic(models.Model):
    '''
    Name of a clinic, One location have multiple clinics and work time of the clinic.
    '''
    DATE_TYPES = (
        ('morning', 'Morning'),
        ('evening', 'Evening')
        )
    
    
    name = models.CharField(max_length = 100)
    location = models.ForeignKey(Location)
    start_time = models.TimeField(default = datetime.time, blank = True)
    end_time = models.TimeField(default = datetime.time, blank = True)
    
    
    def __unicode__(self):
        return '%s, %s' % (self.name, self.location.name)


class Event(models.Model):
    '''
    Specifies a set of events, through which every patients will go through in any Clinic.
    '''
    name = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.name
    
class Interrupt(models.Model):
    '''
      Storing set of Interrupts, ECG and EKG are eg;. It have two events "start" and "stop" interrupts.
    '''
    name = models.CharField(max_length = 150)
    def __unicode__(self):
        return self.name
    
class Attribute(models.Model):
    '''
       Define the name of the attribute and its default error message,
       it will be used when there wont be any value assigned to this attribute and the attribute status is 'required'.
    '''
    
    name = models.TextField()
    error_message = models.TextField()
    
    def __unicord__(self):
        return self.name
   

class EventAttributeMap(models.Model):
    ''' 
        Configuring a particular event to a attribute under a clinic.
        This will be used with the GUI part, to create event based form.
    '''

    attribute = models.ForeignKey(Attribute)
    clinic = models.ForeignKey(Clinic)
    event = models.ForeignKey(Event)
    hidden = models.BooleanField(default = False)
    required = models.BooleanField(default = False)
    def __unicord__(self):
        return "%s > %s > %s" % (self.attribute.name, self.clinic.name, self.event.name)

            

class ClinicEventMap(models.Model):
    '''
    Map to the Clinic Specific Event Set.
    '''
    clinic = models.ForeignKey(Clinic)
    event = models.ForeignKey(Event)
    position = models.IntegerField(max_length = 3, blank = False)
    
    def __unicord__(self):
        return "ClinicEventMap"
    
    
    
class Patient(models.Model):
    '''
    Patient Informations.
    '''
    fName = models.CharField(max_length = 100)
    lName = models.CharField(max_length = 100)
    dob = models.DateField(null = True, blank = True)
    def __unicode__(self):
        return '%s, %s %s' % (self.lName, self.fName, self.dob)
    class Meta:
        permissions = (
            ('can_sign_in', 'Can sign in'),
            ('can_save_event', 'Can save event')
            )


class Provider(models.Model):
    '''
    Provider details,
    '''
    fName = models.CharField(max_length = 100)
    lName = models.CharField(max_length = 100)
    loc = models.ForeignKey(Location, null = True)
    
    def __unicode__(self):
        return '%s %s' % (self.fName, self.lName)
    
    

    
class EventSetHeader(models.Model):
    '''
    This table bind the Patient with a particular Clinic.
    '''
    patient = models.ForeignKey(Patient)
    clinic = models.ForeignKey(Clinic)
    provider = models.ForeignKey(Provider, null = True, blank = True)
    dateTime = models.DateTimeField(default = datetime.datetime.now)
    
    def __unicode__(self):
        return '%s clinic: %s, %s' % (self.patient, self.clinic, self.dateTime)

    def get_cash(self):
        return reduce(lambda a, b: a + float(b.amount), Payment.objects.filter(type = 'cash', header = self), 0.0)
    def get_cc(self):
        return reduce(lambda a, b: a + float(b.amount), Payment.objects.filter(type = 'cc', header = self), 0.0)
    def get_total(self):
        return reduce(lambda a, b: a + float(b.amount), Payment.objects.filter(header = self), 0.0)
    def patientinterruptlist(self):
        patintr = Payment.objects.select_related('interrupttype').filter(header = self)
        result = patintr.values_list('interrupttype', 'interrupttype__name', 'amount', 'type')
        return result
    def get_negativetotal(self):
        negativesum = 0
        negativepayments = Payment.objects.filter(header = self)
        for i in negativepayments:
            if i.amount < 0:
                negativesum = negativesum + i.amount
        return negativesum  
    def get_positivetotal(self):
        positivesum = 0
        positivepayments = Payment.objects.filter(header = self)
        for i in positivepayments:
            if i.amount > 0:
                positivesum = positivesum + i.amount
        return positivesum  
    def get_negcash(self): 
        negcashsum = 0
        negcash = Payment.objects.filter(type = 'cash', header = self) 
        for i in negcash:
            if i.amount < 0:
                negcashsum = negcashsum + i.amount
        return negcashsum 
    def get_negcc(self): 
        negccsum = 0
        negcc = Payment.objects.filter(type = 'cc', header = self) 
        for i in negcc:
            if i.amount < 0:
                negccsum = negccsum + i.amount
        return negccsum   
    def get_user(self):
        event, _ = Event.objects.get_or_create(name = "payment")
        users = PatientEventLog.objects.filter(header = self, event = event)
        for i in users:
            user = i.user
            break 
        return user      


class EventSetAttributeLog(models.Model):
    '''
         This model hold the attribute values inputed by user,
         So here we link the each attribute value to corresponding patient info.
    ''' 
    
    attr_map = models.ForeignKey(EventAttributeMap)
    header = models.ForeignKey(EventSetHeader)
    value = models.TextField()
    
    


class PatientInterruptLog(models.Model):
    '''
      record patient interrupt log.
    '''
    INTERRUPT_STATUS = (('started', "Starting the Interrupts"), ('stopped', "Stopping the Interrupts"))
    
    interrupt = models.ForeignKey(Interrupt)
    status = models.CharField(max_length = 50, blank = False, choices = INTERRUPT_STATUS)
    header = models.ForeignKey(EventSetHeader)
    dateTime = models.DateTimeField(auto_now_add = True)
    user = models.CharField(max_length = 100, blank = True)#User who originated this event.
    
    def __unicode__(self):
        return '%s, eventSetHeader: %s dateTime: %s' % (self.interrupt, self.header, self.dateTime)
    

class PatientEventLog(models.Model):
    '''
    This table hold the current status of each patients under any Clinic.
    '''
    event = models.ForeignKey(Event)
    header = models.ForeignKey(EventSetHeader)
    dateTime = models.DateTimeField(auto_now_add = True)
    user = models.CharField(max_length = 100, blank = True)#User who originated this event.
    
    def __unicode__(self):
        return '%s, eventSetHeader: %s dateTime: %s' % (self.event, self.header, self.dateTime)


class Payment(models.Model):
    '''
    Payment Information of a patient, It's Clinic specific.
    '''
    PAYMENT_TYPES = (
        ('cc', 'Credit card'),
        ('cash', 'Cash')
        )
    header = models.ForeignKey(EventSetHeader)
    type = models.CharField(blank = False, max_length = 16, choices = PAYMENT_TYPES)
    info = models.CharField(blank = True, max_length = 32)
    amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    dateTime = models.DateTimeField(auto_now_add = True)
    #to provide the payment facility to interrupt
    interrupttype = models.ForeignKey(Interrupt, blank = True, null = True)
    #def __unicode__(self):
        #return '%s, eventSetHeader: %s dateTime: %s' % ( self.header, self.dateTime,self.interrupttype)

class AlertConfiguration(models.Model):
    '''
        Each entry hold the specific alert settings. So we need to track each settings.
    '''
    
    ENABLE_CHOICES = (
                ('Yes', 'Enable'),
                ('No', 'Disable'),)
    #general name for this conf
    name = models.CharField(blank = True, null = True, max_length = 100)
    enabled = models.CharField(max_length = 10, choices = ENABLE_CHOICES, default = 'Yes')
    
    clinic = models.ForeignKey(Clinic)
    from_addr = models.CharField(blank = False, null = False, max_length = 100)
    
    event_list = models.CharField(blank = False, null = False, max_length = 300, default = '')
    
    #Multiple to address seperated by ,.
    to_addr = models.CharField(blank = False, null = False, max_length = 1000)
    #Cumulative waiting time for all events in the alert_event_map.
    waiting_time = models.IntegerField(blank = False, null = False, max_length = 3)
    
    #To save maximum retries of mail sending if a patient is matched this rule, 0 for infinite. 
    alert_retry = models.IntegerField(default = 0, max_length = 3)
    
    #save alert interval time.
    alert_interv = models.IntegerField(default = 0, max_length = 3)
    
 
    
    dateTime = models.DateTimeField(default = datetime.datetime.now)
    
    def __unicode__(self):
        return '%s, %s' % (self.name, self.clinic)

#class AlertEventMap(models.Model):
#    '''
#        Map the alert_conf with set of events they tracking..
#    '''
#    alert_conf = models.ForeignKey(AlertConfiguration)
#    event = models.ForeignKey(Event)

class AlertMailLog(models.Model):
    '''
        Log table which save the already sent mail notification for
        future references.
        
        Need explicit informations about client,from_addr and etc.., because
        we might delete the alert_conf once the clinic event pattern changes.
         
    '''
        
    rule_matched = models.ForeignKey(AlertConfiguration, blank = True, null = True,)
    header = models.ForeignKey(EventSetHeader, blank = True, null = True)
    iteration = models.IntegerField(max_length = 3, default = 1)
    dateTime = models.DateTimeField(default = datetime.datetime.now)
    





'''
    Python Module, Here we define the Django signals associated with the Clinic Workflow application.
    
    It includes, signal handlers, signal produces and their binding informations. 
    
    ***IMPORTANT***
    Never include this module in to multiple files, that may lead to replication of signals.So we define,
    this functions under the models.py, that's safe place.
'''

from django.db.models.signals import post_delete
from django.dispatch import receiver
  

@receiver(post_delete, sender = AlertConfiguration, dispatch_uid = "Delete Celery Periodic Task")
def post_alert_conf_delete(sender, **kargs):
    '''
        This will be called when we delete one row from the AlertConfiguration Model.
        
        This is to remove the linking between AlertConfiguration object and Celery 
        PeriodicTask object.
    '''
    
    #print kargs
    
    #Take alert conf object from signal args.
    alert_conf = kargs['instance']
    
    args = '[%s]' % (alert_conf.id,)         
    periodic_task = PeriodicTask.objects.filter(args = args)
    
    #Delete the Corresponding Periodic Task added for this alert conf.
    periodic_task.delete()
    
    #print "Corresponding Periodic Task been deleted.."
    
