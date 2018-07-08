from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.conf import settings
from signin.models import *
from utility import get_clinic_event_map, get_patient_full_name,check_pending_interrupts,format_time
from signin.views import get_request_period, get_event_time,get_current_clinics
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.simple import direct_to_template
from django.template import loader,Context
from django.conf import settings 
from django.contrib.auth.models import User
from signin.decorators import custome_login_required

import datetime
import simplejson

from signin.tasks import move_patient, remove_patient

#@staff_member_required
@custome_login_required(template_name = "jqmtab/login.html")
def jqmtab_home(request):
    '''
        Home Page of the Jqmobile, Which list the set of locations and Clinics.
    '''
    
    locations = Location.objects.all()
    clinics = Clinic.objects.all()
    
    dynamic_datas = {'STATIC_URL': settings.STATIC_URL,
                     'locations': locations,
                     'clinics': clinics,
                    }
    
    return render_to_response('jqmtab/index.html',dynamic_datas)



@custome_login_required(template_name = "jqmtab/login.html")
def jqmtab_frontdesk(request):
    '''
        Index page of the Jquery Mobile Web application.
    '''
    
    locations = Location.objects.all()
    clinics = Clinic.objects.all()
    
    '''
        Currently taking first location's first clinic as default clinic to be displyed at frontdesk.
    '''
    
    clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))

    event_map = get_clinic_event_map(clinic.id)
    
    
    dtStart, dtEnd = get_request_period(request,clinic)
    eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
    
    patients = []
    patient = {}
    events = []
    
    #Get this delete event objects to check whether this patient have delete event. 
    delete = Event.objects.get(name='delete')
    
    
    #Get details of each patients with their current status in specified clinic.
    for esh in eshs:
        
        patient_name = get_patient_full_name(esh)#esh.patient.lName + "," +  esh.patient.fName + "," +  str(esh.patient.dob)
        
        patient_event_logs =  PatientEventLog.objects.filter(header=esh)
        
        #Will have value when this use is been deleted : BUG Fixed(6-May-2010)
        delete_event = patient_event_logs.filter(event = delete)
        
        #for pevlog in patient_event_logs:
        #    events[pevlog.event.name] = pevlog.dateTime.strftime("%H:%M") #str(pevlog.dateTime.hour) + ":" + str(pevlog.dateTime.minute)
        
        #Here we creating events in the Array format with index gives the order, to match the order and genearlized event management.
        '''
         events = [('22:22','event_name'),...]
         
         Due to the clinic generalization, we may have different event order.So we taking genearl methods to 
         get correct event order for a clinic.
        '''
        events = []
        
        #To check deleted users.
        delete_flag = False
        
        for event in event_map:
            event_time = get_event_time(patient_event_logs,event[1])
            events.append((event_time,event[1]))
            if delete_event :
                delete_flag = True
            
        patient = { "patient_name" : patient_name, "header":esh.id,"events":events}
        
        
        #Add This patient to the patient List if the event include "delete" then just discard it.
        if not delete_flag:
            patients.append(patient)
        #patients.append(patient)  
        #if not events.has_key("delete"):
        #    '''
        #    If "delete" entry were present, we just discard that user from frontdesk.
        #    '''
        #    patients.append(patient)
        
        
        
    patients.reverse()
    
    #Channel name is specific for each Clinics. At frontdesk we list the patients of one clinic at a time.
    channel_name = 'frontdesk'+ str(clinic.id)
    
    
    comet = {"SESSION_COOKIE_NAME":settings.SESSION_COOKIE_NAME,"HOST":settings.INTERFACE,"CHANNEL_NAME":channel_name,
             "STOMP_PORT":settings.STOMP_PORT,"USER":request.user}
    
    provider_list = Provider.objects.filter(loc = clinic.location.id)#select the provider info corresponding to a location

    #For hidden header layout fixing, we taking one row of patient data.
    patient_hidden = ''
    
    dynamic_datas = {'STATIC_URL': settings.STATIC_URL,
                     'locations': locations,
                     'clinic':clinic,
                     'clinics': clinics,
                     'clinic_event_map': event_map,
                     'patients': patients,
                     'patient_hidden': patient_hidden,
                     'provider_list' : provider_list,
                     }
    dynamic_datas.update(comet)
                     
    
    return render_to_response('jqmtab/jqmtab_frontdesk.html',dynamic_datas)


def jqmtab_shadowwindow(request,patient_header): 
   
    esh = EventSetHeader.objects.get(id = patient_header)
    home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
    
    #home_url = '/jqmtab/clinic/'
    header = {'headerid':patient_header,'home_url':home_url,'clinic_id':esh.clinic.id }
    
    return render_to_response('jqmtab/jqmtab_shadow_window.html',header)


def jqmtab_shadowwindow_payment(request,patient_header):
    
    esh = EventSetHeader.objects.get(id = patient_header)
    home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
    
    #home_url = '/jqmtab/clinic/'
    header = {'headerid':patient_header,'home_url':home_url }
    
    return render_to_response('jqmtab/jqmtab_shadow_payment.html',header)


def jqmtab_shadowwindow_provider(request,patient_header):
    
    #header = {'headerid':patient_header }
    
    esh = EventSetHeader.objects.get(id = patient_header)
    
    clinic = Clinic.objects.get(id = esh.clinic.id)
    
    provider_list = Provider.objects.filter(loc = esh.clinic.location.id)
    
    home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
     
    data ={'headerid':patient_header,'provider_list':provider_list,'home_url':home_url}
    
    return render_to_response('jqmtab/jqmtab_provider.html',data)


def jqmtab_shadowwindow_edit(request,patient_header):
    
    esh = EventSetHeader.objects.get(id = patient_header)
    
    clinic = get_object_or_404(Clinic.objects, id = esh.clinic.id)

    all_clinics = Clinic.objects.filter(location = clinic.location.id ) 
    
    home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)

    
    data = {'headerid':patient_header,'clinic':clinic,'all_clinics':all_clinics,'home_url':home_url}
    
    return render_to_response('jqmtab/jqmtab_edit.html',data)


def jqmtab_shadowwindow_procedures(request,patient_header):
   ''' 
   pending_stop = []
   
   pending_start = [] 
    
   interrupts = Interrupt.objects.all()
   
   pending_interrupts = check_pending_interrupts(patient_header);
   
   for i in interrupts:
       for j in pending_interrupts:
           if i.name == j[1]:
               pending_stop.append((i.id,i.name,"stop"))

   for i in interrupts:
       p = 0
       for j in pending_stop:
           if i.name == j[1]:
               p = p+1
       if p == 0:
            pending_start.append((i.id,i.name,"start"))  
  
   pending_result =   pending_stop+pending_start       
   '''
   esh = EventSetHeader.objects.get(id = patient_header)
   
   interrupts = []
    
   patient_interrupt = []
    
   result = []
    
   inter = Interrupt.objects.all()
        
   for i in inter:
        interrupts.append((i.name,"start",i.id))    
    
   pat_inter  = PatientInterruptLog.objects.filter(header = esh)
    
   if pat_inter:

        for i in pat_inter:
            patient_interrupt.append((i.interrupt.name,i.interrupt.id))  
        
    
        for i in interrupts:
            c = 0
            for j in patient_interrupt:
                if i[0] == j[0]:
                    c = c+1
            if c == 2:
                result.append((i[0],"complete",i[2]))
            if c == 1:
                result.append((i[0],"stop",i[2])) 
            if c == 0:
                result.append((i[0],"start",i[2]))                         
                            
   
   
   home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
   
   if result:
   
       data = {'headerid':patient_header,'interrupts':result,'home_url':home_url}
   else:
           
       data = {'headerid':patient_header,'interrupts':interrupts,'home_url':home_url}
   
   return render_to_response('jqmtab/jqmtab_procedure.html',data)


def jqmtab_shadowwindow_remove(request,patient_header):
    
   esh = EventSetHeader.objects.get(id = patient_header)
   
   home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
   
   data = {'headerid':patient_header,'home_url':home_url}
   
   return render_to_response('jqmtab/jqmtab_remove.html',data)


def jqmtab_shadowwindow_payment_procedure(request,patient_header):  

   esh = EventSetHeader.objects.get(id = patient_header)
   
   home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
   
   data = {'headerid':patient_header,'home_url':home_url}      
    
   return render_to_response('jqmtab/jqmtab_payment_procedure.html',data)
   

def jqmtab_shadowwindow_appintment(request,patient_header):
    
     
   esh = EventSetHeader.objects.get(id = patient_header)
   
   home_url = '/jqmtab/clinic/?clinicID=' + str(esh.clinic.id)
   
    
   data = {'headerid':patient_header,'home_url':home_url}      
    
   return render_to_response('jqmtab/jqmtab_appointment.html',data)  



def jqmtab_move_patient(request):
    '''
        Move patient from clinic1 to clinic2.
        
        steps are -
            1. remove patient from clinic1
            2. add patient in to clinic2
            3. update frontdesk of both clinic1 and clinic2 via Longpolling.
            
            These functionalities are already defined in the realtime section, so we here just reusing it.
    '''
    
    #Check for any pending interrupts.
    header_id = request.POST['headerID']
    pending_intr = check_pending_interrupts(header_id)
    if pending_intr:
        response = {'status':'FAILD',
                    'msg':'This patient has following active Procedure(s)..',
                    'interrupts': pending_intr,
                    'headerID': header_id
                    }
    else:
        #Do this task asynchronously, a celery task
        move_patient.delay(request)
        response = {'status':'OK'}
    
    response = simplejson.dumps(response)
    return HttpResponse(response,mimetype="application/json")


def jqmtab_remove_patient(request):
    '''
        Removing selected patient from that clinic.
        
        we using celery for asynchronous processing and already existing realtime backed.
    '''
    header_id = request.POST['headerID']
    pending_intr = check_pending_interrupts(header_id)
    #This function return the tuple of pending interrupts [(id,int_name),...]
    if pending_intr:
        response = {'status':'FAILD',
                    'msg':'This patient has following active Procedure(s)..',
                    'interrupts': pending_intr,
                    'headerID': header_id
                    }
    else:
        #Do this task asynchronously, a celery task
        remove_patient.delay(request)
        response = {'status':'OK'}
        
    
    response = simplejson.dumps(response)
    return HttpResponse(response,mimetype="application/json")


@custome_login_required(template_name = "jqmtab/login.html")
def jqmtab_payment(request):
    
    ansDict = dict()
    ansDict['menu'] = 'paymenthistory'
    ansDict['left_menu'] = Clinic.objects.all()
   # ansDict["date"] = request.REQUEST.get("date_in_frontdesk",None)
    
    #if not request.REQUEST.has_key("clinicID"):
        #ansDict['work_time'] = get_current_worktime()
        #ansDict['clinics'] = get_current_clinics()
        #return direct_to_template(request,'payment-base.html',ansDict)

    clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
    
    '''
    dt = datetime.datetime.now()
    dtStart = datetime.datetime(dt.year,dt.month,dt.day,0,0,0)
    dayAddDelta = datetime.timedelta(1)
    dtEnd = dtStart + dayAddDelta
    '''
    dtStart, dtEnd = get_request_period(request,clinic)
    
    
    eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart).order_by("dateTime")

    total = {}
    total['cash']=reduce(lambda a,b: a+b.get_cash(), eshs, 0.0)
    total['cc']=reduce(lambda a,b: a+b.get_cc(), eshs, 0.0)
    total['total'] = total['cash'] + total['cc']
    ansDict['total'] = total
    ansDict['clinic']=clinic
    ansDict['events']=eshs
    return direct_to_template(request,'jqmtab/jqmtab_payment_page.html',ansDict)


@custome_login_required(template_name = "jqmtab/login.html")
def jqmtab_reports(request):
    
    ansDict = updateDict(request)
    ansDict['menu'] = 'reports'
    ansDict['left_menu'] = Clinic.objects.all()
    
    #if not request.REQUEST.has_key("clinicID"):
        #ansDict['work_time'] = get_current_worktime()
        #ansDict['clinics'] = get_current_clinics()
        #return direct_to_template(request,'reports-base.html',ansDict)
    
    clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
    
    ansDict["clinic"] = clinic
    
    #ansDict["date"] = request.REQUEST.get("date_in_frontdesk",None)
    
    #Added variables required for the comet session at report page.
    #channel_name = 'frontdesk' + str(clinic.id)
    #comet = {"SESSION_COOKIE_NAME":settings.SESSION_COOKIE_NAME,"HOST":settings.INTERFACE,"CHANNEL_NAME":channel_name,
             #"STOMP_PORT":settings.STOMP_PORT,"USER":request.user}
    #ansDict.update(comet)
    
    #Get Event map of this clininc. event_map = [(1,signin),(2,registration),...]
    #For User specific mode its better.
    event_map = get_clinic_event_map(clinic.id)
    ansDict['user_clinic_event_map'] = event_map
    
    #Get user specific event_map, signinTregistration or,,, like that format.
    
    default_clinic_event_map = []
    
    for i in range(len(event_map)):
        '''
         creating special header names for report templates.
        '''
        if (i+1) < len(event_map):
            default_clinic_event_map.append(event_map[i][1] + ' To ' + event_map[i+1][1])
        else:
            default_clinic_event_map.append(event_map[i][1])
    
    ansDict['default_clinic_event_map'] = default_clinic_event_map
   
    #Featch the initial Report from the serverclinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None)) itself rather than go for axaj method.
    dtStart, dtEnd = get_request_period(request,clinic)
    eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
    
    patients = []
    patient = {}
    events = []
    pel_temp = {}
    
    
    
    for esh in eshs:
       
        pels = PatientEventLog.objects.filter(header = esh)
    
        patient_name = get_patient_full_name(esh) #esh.patient.lName + "," +  esh.patient.fName + "," +  str(esh.patient.dob)
    
        for pel in pels:
            pel_temp[pel.event.name] = pel.dateTime
     
        for i in range(len(event_map)):
            '''
                Get time interval between events. The order of the event name is passed in "default_clinic_event_map", it hold the ordered events,
                signingTregistration,..etc..
                
                So the events are already ordered, so we take the event_times according to that order in a list. 
            clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
            '''
            if (i+1) < len(event_map):
                if event_map[i][1] in pel_temp and event_map[i+1][1] in pel_temp:
                    events.append(":".join(str(pel_temp[event_map[i+1][1]] - pel_temp[event_map[i][1]]).split(":")[:2]))
                else:
                    events.append(False)
            else:
                if event_map[i][1] in pel_temp:
                    events.append(":".join(str(datetime.datetime.now() - pel_temp[event_map[i][1]] ).split(":")[:2]))
                else:
                    events.append(False)
        
        
        '''pel_temp = {}
        events = []
        if 'signin' in pel_temp and 'registration' in pel_temp:clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
            events['signinTregistration'] = ":".join(str(pel_temp['registration'] - pel_temp['signin']).split(":")[:2])
        
        if 'registration' in pel_temp and 'triage' in pel_temp:
            events['registrationTtriage'] = ":".join(str(pel_temp['triage'] - pel_temp['registration']).split(":")[:2])
        
        if 'triage' in pel_temp and 'provider' in pel_temp:
            events['triageTprovider'] = ":".join(str(pel_temp['provider'] - pel_temp['triage']).split(":")[:2])
        
        if 'provider' in pel_temp and 'checkout' in pel_temp:
            events['providerTcheckout'] = ":".join(str(pel_temp['checkout'] - pel_temp['provider']).split(":")[:2])
        
        if 'appointment' in pel_temp:
            events['appointment'] = ":".join(str(datetime.datetime.now() - pel_temp['appointment'] ).split(":")[:2])
        '''
        
        patient = {"patient_name":patient_name,"header":esh.id,"events":events}
    
        if not 'delete' in pel_temp:
            '''
            If "delete" entry were present, we just discard that user from frontdesk.
            '''
            patients.append(patient)
                       
        #Clear old values.
        pel_temp = {}
        events = []
    
    
    patients.reverse()
    ansDict['patients'] = patients
    
    users = User.objects.all()
    ansDict['users'] = users
                                                    
    return direct_to_template(request, 'jqmtab/jqmtab_reports.html',ansDict);



def updateDict(request):
    ansDict = dict()
    ansDict["STATIC_URL"] = settings.STATIC_URL
    ansDict["user"] = request.user
    # ansDict['left_menu'] = get_current_clinics()
    return ansDict
    

@custome_login_required(template_name = "jqmtab/login.html")
def jqmtab_signin(request):
    
    ansDict = updateDict(request)
    ansDict['menu'] = 'signin'
    
    request.REQUEST.has_key("locationID")
    
    location = get_object_or_404(Location,id=request.REQUEST.get("locationID",None))
    
    ansDict["location"] = location
    providers = Provider.objects.filter(loc=location) #select the provider info corresponding to a location.
    ansDict['providers'] = providers
    clinics = get_current_clinics(default_location = location)
    
    ansDict['clinics'] = clinics
    
    #Added other parameters requred for the comet session.
    comet = {"USER":request.user}
        
    ansDict.update(comet)
    
    return direct_to_template(request,'jqmtab/jqmtab_signin.html', ansDict)


def jqmtab_changedate(request):
    
    return direct_to_template(request,'jqmtab/jqmtab_change_date.html')
    




def jqmtab_logout(request):
    '''
        Logout the user, and show the page with link to login page.
    '''
    
    from django.contrib.auth.view import logout
    
    logout( template_name="jqmtab/logout.html")


















