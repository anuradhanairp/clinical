######################################################################### 
# Copyright (C) 2009, 2010 Alex Clemesha <alex@clemesha.org>
# 
# This module is part of Hotdot, and is distributed under the terms 
# of the BSD License: http://www.opensource.org/licenses/bsd-license.php
#########################################################################
"""
Handlers that inspect, log, and modify
in-transit Orbited messages.

This file is very application specific,
so there needs to be a clear way to:
    1. Create custom message handlers
    2. Overide of message handlers
    3. "Plug in" custom message handlers
"""
import os
import sys
import datetime

#Get the Main Project Dir.
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DJANGO_DIR = os.path.join(PROJECT_DIR,"skgargpms")
#print "PROJECT DIR ===> %s , DJANGO_DIR ===> %s " % (PROJECT_DIR,DJANGO_DIR)
# Environment setup for your Django project files:
sys.path.insert(0,DJANGO_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'skgargpms.settings'

from skgargpms.signin.views import get_local_time

from django.contrib.auth.models import User
from skgargpms.signin.models import *

from signin.utility import gen_report, get_patient_full_name, check_pending_interrupts
#from skgargpms.signin.notifier import start_messager

#A celery task
from signin.tasks import sendmail
try:
    import json
except ImportError:
    import simplejson as json

# TODO
# take all below functions and put into an base class and subclass:
# Make 'logging' of all message tunable
# Have base-class use  'getattr' in combination with 'msgtype'.
# to get the appropiate message handler.


def handle_send(msg, username, channel_id):
    
    #Here in the signin case we replay back with relevant informations only.
    ack_msg = {}
    update = {}
    ack_msg.update({"from":username})
    
    msg = json.loads(msg)
    msgtype = msg.get("type")
    
    if not msgtype:
        update = {"error":"Missing message type"}
        
    elif msgtype == "signin":
        '''
            Signin is now via ajax call, so to brodcast the msgs,
            we just return the msg back.
        '''
        return msg

    elif msgtype == "eventlog":
        
        #print "handling event log from the realtime python module ..."
        
        event_name = msg.get("event")
        headerID = msg.get("headerID")
        
        #--- if the event name is not checkout , then the notifier function will get called...---#
        #start_messager()
        if msg.get('event') != "checkout":
            #Send mailing task to queue.
            sendmail.delay() 
        
        #Update the event to Models.
        header = EventSetHeader.objects.get(id=headerID)
        
        check_interrupt = check_pending_interrupts(headerID)
        #check_interrupt = []
        if check_interrupt:
            reason = 'Patient Waiting for these Interrupts: '
            for intr in check_interrupt:
                reason +=  intr[1] + ", "
            update = {'response':'False','type':'eventlog','reason':reason}
            
        elif event_name == 'provider' and header.clinic.location.provider_required == True and header.provider == None :
            '''
            If patient Has no provider assigned then go back to add that first.
            
            Additional updation were done on 22/07/2011, Location wise provider enable/desable feature.
            '''
                   
            
            reason = 'Please asign a Provider to this patient...'
            update = {'response':'False','type':'eventlog','reason':reason}
            
        else: 
            event  = Event.objects.filter(name = event_name)[0] 
            pevlogcount = PatientEventLog.objects.filter(header = header, event = event ).count()
            
            if pevlogcount == 0:
                #Update the New envent to corresponding patient.
                PatientEventLog(header = header , event = event, user = username).save()
                
                #update the other clients using below json object.
                pevlogs = PatientEventLog.objects.filter(header = header)
                
                #Get localtime zone.
                local_timezone = pevlogs[0].header.clinic.location.timezone
                
                patient = {}
                patient['name'] = get_patient_full_name(header)#header.patient.lName + "," + header.patient.fName + "," + str(header.patient.dob)
                
                for pevlog in pevlogs:
                    #event_name = pevlog.event.name
                    #time = str(pevlog.dateTime.hour) + ":" + str(pevlog.dateTime.minute)
                    
                    #Call get_local_time function to convert the time to local timezone format.
                    patient[pevlog.event.name] = get_local_time(local_timezone,pevlog.dateTime)
                
                #Get parameters for the report page.
                report = gen_report(header)
                
                patient.update(report)
                #Full patient informations in a dictionary.
                update = {"patient":patient}
                
        #filling msg values into ack_msg.
        ack_msg.update(msg)
        
    elif msgtype == 'move':
        '''
        Patient modification , orginated from shadow edit tab.
        msg = {'type':'edit','headerID':header, 'new_clinic':clinic '}
        
        In the response mail we change the event type to new "signin"
        '''
        
        #Reply messages.
        patient_info = {}
        update = {'response':"OK",'type':'signin'}
        
        header_id = msg.get("headerID")
        new_clinic = msg.get("new_clinic")    
        
        
        #Get patient details from EventSetHeader.
        
        old_esh = EventSetHeader.objects.get(id = header_id)
        #change current clinic to new one.
        #Create new Entry for this patient at EventSetHeader.
        
        new_clinic = Clinic.objects.get(id = new_clinic)
        
        local_timezone = new_clinic.location.timezone
        
        esh = EventSetHeader(patient = old_esh.patient, clinic = new_clinic)
        if old_esh.provider :
            esh.provider = old_esh.provider
        esh.save()
        

        
        #Update the Patient Event log with this new info.
        #Add basic patient info.
        patient_info['name'] = get_patient_full_name(esh)#esh.patient.lName + "," + esh.patient.fName + "," + str(esh.patient.dob)
        update['headerID'] = esh.id
        
        #update patient's current event.
        event = Event.objects.get(name = 'signin')
        pel = PatientEventLog(header = esh , event = event, user = username)
        pel.save()
        #Add signin event.
        patient_info[pel.event.name] = get_local_time(local_timezone,pel.dateTime)#pel.dateTime.strftime("%H:%M") #str(pel.dateTime.hour) + ":" + str(pel.dateTime.minute)
        
        #Check for whethere user where already Taken "appointment":
        event,_ = Event.objects.get_or_create(name="appointment")
        pel = PatientEventLog.objects.filter(header = esh, event = event)
        
        if pel:
            pel = PatientEventLog(header = esh, event = event , user = username)
            pel.save()
            patient_info[pel.event.name] = get_local_time(local_timezone,pel.dateTime) #pel.dateTime.strftime("%H:%M") #str(pel.dateTime.hour) + ":" + str(pel.dateTime.minute)
        
        
        #Get parameters for the report page.
        report = gen_report(esh)
        patient_info.update(report)
        
        update['patient'] = patient_info
        
    #update the message with type specific response info:
    #msg.update(update)
    ack_msg.update(update)
    return ack_msg


def handle_subscribe(msg, username, channel_id):
    #print "=handle_subscribe= ", msg, username, channel_id
    return msg

def handle_connect(msg, username, channel_id):
    #print "=handle_connect= ", msg, username, channel_id
    return msg

def handle_disconnect(msg, username, channel_id):
    #print "=handle_disconnect= ", msg, username, channel_id
    return msg

def handle_unsubscribe(msg,username,channel_id):
    #print "=handle_unsubscribe=" , msg , username , channel_id
    return msg


MESSAGE_HANDLERS = {
    "send":handle_send,
    "subscribe":handle_subscribe,
    "connect":handle_connect,
    "disconnect":handle_disconnect,
    "unsubscribe": handle_unsubscribe
}
