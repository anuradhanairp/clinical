###########################################################
#             General notification module(Final Beta)     #
#             Author : Robert -Spark                      # 
# conventions used '###' for testing intermediate values  #
# '#----#' for comments etc..                             #
###########################################################
import os
import sys
sys.path = [os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), os.path.dirname(os.path.abspath(os.path.dirname(__file__))), os.path.abspath(os.path.dirname(__file__))] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
import datetime
from signin.models import *
from signin.smtp import *
import time
from django import forms
from django.core.validators import validate_email

#Importing django model Field method, F, The db field increment operations are done by db itself.
from django.db.models import F

import pytz

#---creating two blank lists ,which will be used later in the module..---#
checkd_out_ids = [] 
active_patient_ids = []
last_event = None
count = None

total_patient_ids = []
choice = settings.ENABLE_NOTIFIER.lower()
old_values = {}

def messager(rules, dict_passed):
                  
        n_mins = rules['aggr_time']
        mailer = Smtp();
        mailer.rcpt_to(rules['to_addr'].split(','))
        mailer.from_addr(rules['from_addr'])
        msge = msg_replace(dict_passed)
        msge = msge.replace('{n}', str(n_mins))
        mailer.message(msge)
        ###-subject=rules['subject']
        subject = "Alert :- Patient {fname} is still waiting to be  processed..."
        subject = subject.replace('{fname}', dict_passed['{fname}'])
        mailer.subject(subject)
        #print vars()
        try:
           mailer.send()
          
        except:
             return None

 
def msg_replace(valuedic):
    x = open(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'templates/email-message.txt'), 'r')
    msg_txt = x.read()
    
    for i, j in valuedic.iteritems():
        msg_txt = msg_txt.replace(str(i), str(j))
###    x.close()
    return msg_txt


def process_one_alert_rule(alert_conf_id):
    
    ''' 
        
        Function which accept an alert configuration ID and match for the 
        patients under that clinic. If there is any matching then send mail about
        that mail.
        
        To process single alert rule only we can use this function.
        
        ie; After midnight we have to avoid previous days record.
    '''
    
    #get given rule information.
    alert_rule = AlertConfiguration.objects.get(id = alert_conf_id)
    
    #Active patient threshold window. we will take recent patient events from this threshold window.  
    active_window = datetime.timedelta(hours = 2)
    
    date = datetime.datetime.now()
    
    local_time = pytz.utc.localize(date).astimezone(pytz.timezone(alert_rule.clinic.location.timezone))
    diff = datetime.timedelta(minutes = local_time.minute, seconds = local_time.second, hours = local_time.hour)
    mid_night = local_time - diff
    
    if diff < active_window:
        'In the case of just passed the midnight'
        active_window_start = mid_night
    else:
        active_window_start = local_time - active_window 
    
    #convert localtime to UTC
    active_window_start_utc = active_window_start.astimezone(pytz.utc)
    
    #Delete Event object, to remove the deleted patients from alert sending.
    
    delete_ev = Event.objects.filter(name = 'delete')[0]
    
    if alert_rule.enabled == 'Yes':
        
        #Featch only the Patient information of current location.
        pevlog = PatientEventLog.objects.filter(dateTime__gte = active_window_start_utc,
                                                header__clinic = alert_rule.clinic)
        
        #Event log of Deleted patients..
        pevlog_deletes = PatientEventLog.objects.filter(dateTime__gte = active_window_start_utc,
                                                       header__clinic = alert_rule.clinic,
                                                       event = delete_ev)
        headers_del = [a[0] for a in list(set(pevlog_deletes.values_list('header')))]
        
        #Here we get only the header id's not the objects.
        headers = [ a[0] for a in list(set(pevlog.values_list('header')))]
        
        #After removing deleted patient headers
        headers = list(set(headers) - set(headers_del))
        
        for header in headers:
            
            header = EventSetHeader.objects.get(id = header)
            
            '####Start maching process.###'
            
            #Take setoff happended events of this patient.[ev1,ev2,..]
            pat_evt = [a[0] for a in pevlog.filter(header = header).values_list('event__name')]
          
            #print pat_evt
            
            #Remove boundary events.
            if 'appointment' in pat_evt:
                pat = pat_evt.pop(pat_evt.index('appointment'))
          
            if 'checkout' in pat_evt:
                pat = pat_evt.pop(pat_evt.index('checkout'))
  
            #Take configured events from the alert rule, [ev1, ev2, ..]
            event_list = alert_rule.event_list.split(',')
            
            #Store matched event times after comparing the event_list and pat_evt 
            match_evt = []
            
            
            for evt in event_list:
                '''
                    Match the each events in the event_list with current happened events of a patient.
                    
                    'match_evt' hold list of tupples, in each tupple have start and end time of the matched event.
                '''
                if evt in pat_evt:
                    
                    #Take event matched object object 
                    pev1 = pevlog.get(header = header, event__name = evt)
                    
                    #take index of that event in patient_event array.
                    index = pat_evt.index(evt)
                    
                    #if that is not the last one.
                    if index + 1 < len(pat_evt):
                        
                        #then take successor event object.
                        pev2 = pevlog.get(header = header, event__name = pat_evt[index + 1])
                        
                        #Add the total time taken by the given event.
                        match_evt.append((pev1.dateTime, pev2.dateTime))
                    else:
                        #if the matched event is the last one.
                        match_evt.append((pev1.dateTime, date))
                        
            #End of event matching...
            
            if match_evt:
                'There is a match'
                
                #Find total time span of matched events.
                aggr_time = datetime.timedelta(0)
                for j in match_evt:
                    aggr_time += j[1] - j[0]
                
                if aggr_time > datetime.timedelta(minutes = alert_rule.waiting_time):
                    '''
                        #Total event time span exceeds the given waiting_time, so we need to send alert mail.
                    '''
                    
                    #Mail Template preparation...
                    superrules = {'name': alert_rule.name,
                                  'enabled': alert_rule.enabled,
                                  'from_addr': alert_rule.from_addr,
                                  'event_list': alert_rule.event_list,
                                  'to_addr': alert_rule.to_addr,
                                  'aggr_time': alert_rule.waiting_time
                                  }
                    
                    valuedict = {'{patient-id}' : header.patient.id,
                                 '{fname}': header.patient.fName,
                                 '{lname}': header.patient.lName,
                                 '{location}': header.clinic.location,
                                 '{clinic-id}': header.clinic.name,
                                 '{event}': alert_rule.event_list
                                 }
                    
                    #Log the Mail information to Database.
                    alert_log = AlertMailLog.objects.filter(header = header, rule_matched = alert_rule)
                    
                    if alert_log:
                        'Log entry already exist...'
                        alert_log = alert_log[0]
                        
                        #Increament the Alert Mail count.
                        if alert_log.iteration < alert_rule.alert_retry or alert_rule.alert_retry == 0:
                            'alert_retry = 0, for unlimitted mail sending...'
                            
                            alert_log.iteration += 1
                            alert_log.save()
                            
                            #Send mail
                            messager(superrules, valuedict)
                    else:
                        'Sending alert first time about this patient...'
                        alert_log = AlertMailLog(header = header, rule_matched = alert_rule)
                        alert_log.save()
                        
                        #send mail.
                        messager(superrules, valuedict)
                        
   
def start_messager():
    '''
        New Alert system implementations with minimal complexity.
        
        If we want to process every alert rules then this function is more efficient.
        
        algorithm:-
        
            1. Get Each patient from the list for a active frame of 2hours
            2. Get patient current list of events and its time.
            3. Then patient is traverse through the all rules under his clinic.
            4. Then match each patient event with rule event, and take matching events and its time.
            5. For the boundary matching we take current time for its ending time.
            6. For each such a matched events, we calculate aggregate time and if it exceeds the threshold we send mail out.
                
    '''
    
    for location in Location.objects.all():
        '''
            We iterate the alert checking process for every location, this is to solve 
            the issue of timezone difference and time cross over. 
            
            ie; After midnight we have to avoid previous days record.
            
        '''
        
        date = datetime.datetime.now()
        
        #Active patient threshold window. we will take recent patient events from this threshold window.  
        active_window = datetime.timedelta(hours = 2)
    
        local_time = pytz.utc.localize(date).astimezone(pytz.timezone(location.timezone))
        diff = datetime.timedelta(minutes = local_time.minute, seconds = local_time.second, hours = local_time.hour)
        local_time_midnight = local_time - diff
        
        if diff < active_window:
            'In the case of just passed the midnight'
            active_window_start = local_time_midnight
        else:
            active_window_start = local_time - active_window 
    
        #convert localtime to UTC
        current_time = active_window_start.astimezone(pytz.utc)
        
        
        
        #get delete event object, to avoid those patients.
        delete_ev = Event.objects.filter(name = 'delete')
        
        #Event log of Deleted patients..
        pevlog_deletes = PatientEventLog.objects.filter(dateTime__gte = current_time,
                                                       header__clinic__location = location,
                                                       event = delete_ev)
        
        
        #Featch only the Patient information of current clinic.
        pevlog = PatientEventLog.objects.filter(dateTime__gte = current_time,
                                                header__clinic__location = location)
        
        #print pevlog.count()
        
        #Here we get only the header id's not the objects.
        headers = [ a[0] for a in list(set(pevlog.values_list('header')))]
        
        headers_del = [a[0] for a in list(set(pevlog_deletes.values_list('header')))]
     
        #After removing deleted patient headers
        headers = list(set(headers) - set(headers_del))
        
        
        
        for header in headers:
                
          
          #print header
          
          header = EventSetHeader.objects.get(id = header)
          
          pat_evt = [a[0] for a in pevlog.filter(header = header).values_list('event__name')]
          
          #print pat_evt
          
          if 'appointment' in pat_evt:
              pat = pat_evt.pop(pat_evt.index('appointment'))
          
          if 'checkout' in pat_evt:
              pat = pat_evt.pop(pat_evt.index('checkout'))
          
          alert_confs = AlertConfiguration.objects.filter(clinic = header.clinic, enabled = 'Yes')
          
          for alert_conf in alert_confs:
              
            
            event_list = alert_conf.event_list.split(',')
            match_evt = []
            for evt in event_list:
              if evt in pat_evt:
                #p = PatientEventLog.objects.get(header = header,event__name=evt)
                p = pevlog.get(header = header, event__name = evt)
                a = pat_evt.index(evt)
                
                if a + 1 < len(pat_evt): 
                  #q=PatientEventLog.objects.get(header = header,event__name=pat_evt[a+1])
                  q = pevlog.get(header = header, event__name = pat_evt[a + 1])
                  match_evt.append((p.dateTime, q.dateTime))
                else: 
                   match_evt.append((p.dateTime, date))
                   
            #print match_evt
            
            if match_evt:
                
              agr_time = datetime.timedelta()
              for j in match_evt:
                agr_time += j[1] - j[0]
                
              superrules = {}
              
              superrules['name'] = alert_conf.name
              superrules['enabled'] = alert_conf.enabled
              superrules['from_addr'] = alert_conf.from_addr
              superrules['event_list'] = alert_conf.event_list
              superrules['to_addr'] = alert_conf.to_addr
              superrules['aggr_time'] = alert_conf.waiting_time
              
              if len(superrules) != 0 :
                  
                 waiting_time_sec = int(superrules['aggr_time'])
                 
                 
                 valuedict = {}
                 valuedict['{patient-id}'] = header.patient.id
                 valuedict['{fname}'] = header.patient.fName
                 valuedict['{lname}'] = header.patient.lName
                                   
                 valuedict['{location}'] = header.clinic.location.name
                 valuedict['{clinic-id}'] = header.clinic.name
                 
                 valuedict['{event}'] = alert_conf.event_list
                
                 if agr_time >= datetime.timedelta(seconds = waiting_time_sec):
                     
                     'Agregate time of events is grater than waiting time given'
                     
                     #print 'sending mail...'
                     
                     #Increase the count of repeted sending count for each patient and rule set.
                     
                     alert_log = AlertMailLog.objects.filter(header = header, rule_matched = alert_conf)
                     
                     if alert_log:
                         
                         'Already log entry exist.'
                         
                         alert_log = alert_log[0]
                         
                         if alert_log.iteration < alert_conf.alert_retry or alert_conf.alert_retry == 0:
                             'Retry is not exceeded, so we increament the count, and send mail.'
                             
                             alert_log.iteration += 1;
                             alert_log.save()
                             #send Email.
                             messager(superrules, valuedict)
                     else:
                         
                        'New Alert, so save it in the db'
                        
                        alert_log = AlertMailLog(header = header, rule_matched = alert_conf)
                        alert_log.save()
                        
                        #Then send mail.
                        messager(superrules, valuedict)
                        
                            
     

if __name__ == '__main__':
        start_messager()
