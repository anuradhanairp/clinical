#Celery Tasks Module.

#Put Mailing tasks here as one celery task, so we can asynchronously run them.

from celery.decorators import task
from celery.decorators import periodic_task

from signin.notifier import start_messager, process_one_alert_rule
from django.shortcuts import get_object_or_404
from utility import gen_report, get_patient_full_name
import datetime
import time
from signin.models import *
from signin.views import get_local_time
from django.conf import settings
import simplejson as json


#Stomp Client.
from stompclient import PublishClient


#using new stompclient.

#from stompest.simple import Stomp

########################################################
#Periodical Tasks
# We create them as usual Tasks but via DB
# Periodic task schedular we add them via code in the 
#DB.
########################################################

@task
def process_an_alert(alert_conf_id):
    '''
        We set optional arguemnt as alert_conf_id when we create a periodic task, so 
        we get that value as argument to this function...
    '''
    
    print 'testing...%s' % (alert_conf_id,)
    
    process_one_alert_rule(alert_conf_id)






########################################
#Noramal Celery Tasks
#We call them based on the user events.
########################################
@task
def sendmail():
    '''
         Now this function will be called for user click event and done as celery task
    '''
    start_messager()
  

@task
def post_signin_process(request):
    '''
    Do All remaining process of signin. The main signin process will just 
    
    pass the values and then return to the browser.
    
    This is to improve the user interactiveness.
    
    
    Processing new patient signin here.
        
        return JSON frommat:- 
        
        Possitive result:- 
         {'type':'signin','headerID':header,'from':user,'response':'OK', 'patient':{'name':name ,'event_name':time ...}}
        
        Negative result:-
         {'type':'signin','response':'failed','from':user}
         
         
         #Also Modified to get the genaralizing property.
    
    '''
    
    #Update other browsers by sending update to message queue channel.
    STOMP_HOST = settings.INTERFACE
    STOMP_PORT = settings.STOMP_PORT
    
    
    #Stomp client that will just push the message to the server. Do this process at first
    # To avoid the improper connection.
    stomp_client = PublishClient(STOMP_HOST, STOMP_PORT)
    
    #stomp_client = Stomp(STOMP_HOST,STOMP_PORT)
    
    user = request.REQUEST['user']
    
    #Stomp backend server use this user session key to authenitcate with the backend stomp broker.
    password = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    stomp_client.connect(user, password)
    
    #One second delay here, before we send data to channel.
    #To complete all initial handshakes with stomp server.
    time.sleep(1)
    
    
    fName = request.REQUEST["fname"]
    lName = request.REQUEST["lname"]
    clinic = request.REQUEST["clinic"]
    appointment = request.REQUEST["appointment"]
    
    if request.REQUEST.get('day'):
        
        day = request.REQUEST["day"]
        month = request.REQUEST["month"]
        year = request.REQUEST["year"]
        dob = datetime.date(int(year), int(month), int(day))
        
    else:
        dob = None
        
    #providernew = request.REQUEST["provider"] #take the provider info.
    #provider = get_object_or_404(Provider, id = request.REQUEST.get('provider',None))
    #provider = Provider.objects.get(id=providernew)
    
    
    #Fill required parameters to update the client.
    patient_info = {}
    
    
    patient = Patient.objects.filter(fName = fName, lName = lName, dob = dob)

    if patient.count() == 0:
        patient = Patient(fName = fName, lName = lName, dob = dob)
        patient.save()
    else:
        patient = patient[0]

    clinic = Clinic.objects.get(id = clinic)
    esh = EventSetHeader(patient = patient, clinic = clinic, provider = None)#along with patient info provider info are added to eventsetheader. 
    esh.save()
    
    #Add basic patient info.
    patient_info['name'] = get_patient_full_name(esh)#esh.patient.lName + "," + esh.patient.fName + "," + str(esh.patient.dob)
    
    
    local_timezone = clinic.location.timezone
    
    event = Event.objects.filter(name = "signin")[0]
    
    pel = PatientEventLog(event = event, header = esh, user = user)
    pel.save()
    
    #Add signin event.
    patient_info[pel.event.name] = get_local_time(local_timezone, pel.dateTime)
    
    if (appointment == "yes"):
        event, _ = Event.objects.get_or_create(name = "appointment")
        pel = PatientEventLog(event = event, header = esh, user = user)
        pel.save()
        
        #Add appointment event.
        patient_info[pel.event.name] = get_local_time(local_timezone, pel.dateTime)
    
    
    #Get parameters for the report page.
    report = gen_report(esh)
    patient_info.update(report)
    
    CHANNEL_NAME = '/topic/frontdesk' + str(clinic.id)
    
    ack_msg = {'type': 'signin', 'from':user, 'headerID':esh.id, 'response':'OK', 'patient':patient_info }
    ack_msg = json.dumps(ack_msg)
    
                   
    stomp_client.send(CHANNEL_NAME, ack_msg)
    
    #Wait successfull completion of message sending.
    time.sleep(5)
    
    stomp_client.disconnect()
    


@task
def move_patient(request):
    '''
        This function is used with JQM Tab application.
        
        A task to asychronously process the patient movement from one clinic to another ,
        and propagate the information to frontdsek via STOMP clinent.
    '''
    
    post_data = request.POST
    header_id = post_data['headerID']
    new_clinic_id = post_data['new_clinic_id']
    
    user = post_data['user']
    password = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    
    #Update other browsers by sending update to message queue channel.
    STOMP_HOST = settings.INTERFACE
    STOMP_PORT = settings.STOMP_PORT
        
    #Stomp client that will just push the message to the server. Do this process at first
    # To avoid the improper connection.
    stomp_client = PublishClient(STOMP_HOST, STOMP_PORT)
    stomp_client.connect(user,password)
    time.sleep(1)
    
    #First send the delete event to current clinic.
    header = EventSetHeader.objects.get(id = header_id)
    curr_channel_name = '/topic/frontdesk' + str(header.clinic.id)
    msg = {'type':'eventlog','headerID':header_id,'event':'delete'};
    msg = json.dumps(msg)
    stomp_client.send(curr_channel_name,msg)
    
    
    new_channel_name = '/topic/frontdesk' + new_clinic_id
    msg = {'type':'move','headerID':header_id,'new_clinic':new_clinic_id}
    msg = json.dumps(msg)
    stomp_client.send(new_channel_name,msg)
    
    time.sleep(2)
    
    stomp_client.disconnect()
    

@task
def remove_patient(request):
    '''
        This function is used with JQM Tab.
      
        Just delete the patient asynchronously.
    '''
    
    post_data = request.POST
    
    header_id = post_data['headerID']
    
    header = EventSetHeader.objects.get(id = header_id)
    
    user = post_data['user']
    password = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    
    #Update other browsers by sending update to message queue channel.
    STOMP_HOST = settings.INTERFACE
    STOMP_PORT = settings.STOMP_PORT
        
    #Stomp client that will just push the message to the server. Do this process at first
    # To avoid the improper connection.
    stomp_client = PublishClient(STOMP_HOST, STOMP_PORT)
    stomp_client.connect(user,password)
    time.sleep(1)
    
    curr_channel_name = '/topic/frontdesk' + str(header.clinic.id)
    
    msg = {'type':'eventlog','headerID':header_id,'event':'delete'};
    msg = json.dumps(msg)
    stomp_client.send(curr_channel_name,msg)
    
    time.sleep(2)
    stomp_client.disconnect()
    

@task
def trigger_event(event_name,headerID = '',credantials = {}):
    '''
        Trigger the given event from python client.
        Due to the spceial scenarios we use this function to programmatically trigger events. 
    '''
    header = EventSetHeader.objects.get(id = headerID)
    
    channel_name = '/topic/frontdesk' + str(header.clinic.id)
    
    #Prepare the python dict for stomp server.
    msg = {'type':'eventlog','headerID':headerID,'event':event_name}
    
    send_stomp_msg(msg,[channel_name],credantials)
    
       
    
def send_stomp_msg(msg,channels,credantials):
    '''
        A general function to send message to the long polling channel.
        
        input - 
            msg - The standard msg format that supported by the backend stomp implementation.
            channels - List of channels to which we want to publish this messages.
            credantials - username/password pair to login to the stomp server.
            
        Here we using a simple publish client to send the messages to corresponding channels.
    '''
    
    #Update other browsers by sending update to message queue channel.

    username = credantials.get('username',None)
    password = credantials.get('password',None)
    
    #Stomp client that will just push the message to the server. Do this process at first
    # To avoid the improper connection.
    stomp_client = PublishClient(settings.INTERFACE, settings.STOMP_PORT)
    stomp_client.connect(username,password)
    time.sleep(1)
    
    #Encode the python dict to json object.
    msg = json.dumps(msg)
    
    #Sending msg to corresponding channels.
    for channel_name in channels:
         stomp_client.send(channel_name,msg)
    
    time.sleep(2)
    stomp_client.disconnect()

