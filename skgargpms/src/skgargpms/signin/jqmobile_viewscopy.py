from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404
from django.conf import settings
from signin.models import *
from utility import get_clinic_event_map, get_patient_full_name,check_pending_interrupts,format_time
from signin.views import get_request_period, get_event_time
#from django.contrib.admin.views.decorators import staff_member_required
from signin.decorators import custome_login_required
import datetime
import simplejson

#Celery tasks
from signin.tasks import trigger_event

def get_current_patient_event(patient_event_log):
    
    '''
        Input: Events of an active patient..
                if event is set, then only patients under that event will be return
                  
        return value: {'event_name':'waiting_time of last event happened'}
    '''
    
    clinic = patient_event_log[0].header.clinic
    event_map = get_clinic_event_map(clinic.id)
    
    #Remove all other events from pevlog which are not part of the event_map of a clinic.
    patient_event_log = [q for q in patient_event_log if [a for a in event_map if a[1] == q.event.name ] ]
        
    
    #List of active event names.
    event_map_names = [event[1] for event in event_map]
    
    total_events = len(patient_event_log)
    current_event = patient_event_log[total_events - 1]
    current_event_name = current_event.event.name
    
        
    #Get the current event order number from the event_map function.
    current_event_num = [event[0] for event in event_map if event[1] == current_event_name][0]
    
    current_event_waiting_time = datetime.datetime.now() - current_event.dateTime
    
    response = {'event_name': current_event_name,
                'waiting_time': current_event_waiting_time,
                'event_num': current_event_num  }
    
    return response
    

def get_aggr_patients(eshs) :
    '''
        Input: Set of active patients from a clinic.
        
        Output: {'event_name':('patient_count',avg_time) , ...}
        
    '''
    response = {}
    flag = "false"
    
    for esh in eshs:
        
        flag = "false"
        pevlog = PatientEventLog.objects.filter(header = esh)
        
        for pev in pevlog:
            if pev.event.name == "delete":
               flag = "True"
               
        if  flag=="false":
         current_event = get_current_patient_event(pevlog)
         
        
         if response.has_key(current_event.get('event_name')):
            'Event already added to dict'
            
            count,avg_time = response.get(current_event.get('event_name'))
            
            avg_time = (avg_time + current_event.get('waiting_time'))/2
            
            response[current_event.get('event_name')] = (count + 1, avg_time)
         else:
            response[current_event.get('event_name')] = (1,current_event.get('waiting_time'))
       
    return response

def get_event_attributes(clinic, event, header = None):
    '''
        This function return the attributes of a current clinic.
        
        if the 'event' or 'header' where specified then we get the specific output corresponding to the input.
        
        output format -
            
            [{'attrmap_id':id, 
              'attr_name':'attr_name', 
              'attr_hidden':True, 
              'attr_required':True, 
              'attr_value':value,
              'attr_error_msg': msg
            },
            ...
            ]
            
    '''
    attr_list = []
    attr_dict = {}
    
    attributes = EventAttributeMap.objects.filter(clinic = clinic, event = event)
    
    if header:
        attr_values = EventSetAttributeLog.objects.filter(header = header, attr_map__event = event)
    else:
        attr_values = None
    
    for attr in attributes:
        
        attr_dict = {
                     'attrmap_id': attr.id,
                     'attr_name': attr.attribute.name,
                     'attr_error_msg': attr.attribute.error_message,
                     'attr_hidden': attr.hidden,
                     'attr_required': attr.required
                     }
                
        attr_value = attr_values.filter(attr_map = attr)
        if attr_value:
            attr_value = attr_value[0].value
        else:
            attr_value = None
                           
        attr_dict.update({'attr_value': attr_value })
        
        attr_list.append(attr_dict)
    
    return attr_list
    
    
  



@custome_login_required(template_name = "jqmobile/login.html")
def jqmobile_home(request):
    '''
        Home Page of the Jqmobile, Which list the set of locations and Clinics.
    '''
    
    locations = Location.objects.all()
    clinics = Clinic.objects.all()
    
    dynamic_datas = {'STATIC_URL': settings.STATIC_URL,
                     'locations': locations,
                     'clinics': clinics,
                    }
    
    return render_to_response('jqmobile/index.html',dynamic_datas)


def jqmobile_station_summary(request,clinic_id):
    
     #clinic = get_object_or_404(Clinic,id = clinic_id)
     stations = []
     clinic = Clinic.objects.get(id = clinic_id)
    
     dtStart, dtEnd = get_request_period(request,clinic)
     eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
     
     response = get_aggr_patients(eshs)
     
     event_map = get_clinic_event_map(clinic_id)
     
     for event in event_map:
         
         e=Event.objects.get(name = event[1])
         
         if response.has_key(event[1]):

             count,avg_time = response.get(event[1])
             stations.append((e.id,event[1],count,avg_time))
             
         else:
             
             stations.append((e.id,event[1],0,0))
     
     datas = {
               'clinic_event_map': event_map
              
              }
     return render_to_response('jqmobile/stationsummary.html',{'stations':stations})


def jqmobile_patient_summary(request,clinic_id):
    '''
        List the All patients under this clinic.
    '''
    
    clinic = Clinic.objects.get(id = clinic_id)
    
    dtStart, dtEnd = get_request_period(request,clinic)
    eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
    
    patient_list = []
    patient_info = {}
    
    for esh in eshs:
        
        pevlog = PatientEventLog.objects.filter(header = esh)
        
        patient_name = get_patient_full_name(esh)
        
        current_event = get_current_patient_event(pevlog)
        
        patient_info = {
                        'name': patient_name,
                        'header_id': esh.id,
                        'event_num': current_event.get('event_num'),
                        'waiting_time': current_event.get('waiting_time')
                        }
        
        #Add the patient_info to master dict.
        patient_list.append(patient_info)
    
    #To get the new patient at the top    
    patient_list.reverse()
    
    data = { 'patients': patient_list }
    
    return render_to_response('jqmobile/patientsummary.html',data)
    
        
        
def jqmobile_event_patient_summary(request,clinic_id,event_id):
    '''
        List the patients specific to an event under a clinic.
    '''
    
    clinic = Clinic.objects.get(id = clinic_id)
    event = Event.objects.get(id = event_id)
    
    
    dtStart, dtEnd = get_request_period(request,clinic)
    eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
    
    patient_list = []
    patient_info = {}
    
    for esh in eshs:
        
        pevlog = PatientEventLog.objects.filter(header = esh)
        
        patient_name = get_patient_full_name(esh)
        
        current_event = get_current_patient_event(pevlog)
        
        patient_info = {
                        'name': patient_name,
                        'header_id': esh.id,
                        'event_num': current_event.get('event_num'),
                        'waiting_time': format_time(current_event.get('waiting_time'))
                        }
        
        #Add the patient_info to master dict, if its matches the filter condition.
        if current_event.get('event_name') == event.name:
            patient_list.append(patient_info)
    
    #To get the new patient at the top    
    patient_list.reverse()
    
    data = { 'patients': patient_list }
    
    return render_to_response('jqmobile/patientsummary.html',data)

    

def jqmobile_patient_stations(request,header_id):
    '''
        List events of a particular patient, with current status of each event.
        
        output to template format.
        
        [('event_name','current_status','waiting_time','event_order_num'),....]
        
    '''
    
        
    header = EventSetHeader.objects.get(id = header_id)
    pevlog = PatientEventLog.objects.filter(header = header_id)
    
    active_events = [(p.event.name,p.dateTime) for p in pevlog]
           
    event_map = get_clinic_event_map(header.clinic.id)
    
    event_list = []
    #Remove Un importand events like 'appointment'.
    for ev in event_map:
        
        match = [ event for event in active_events if ev[1] == event[0] ]
        if match:
            event_list += match
    
    patient_events = []
    
    current_event = get_current_patient_event(pevlog)
    
    event_map_len = len(event_map)
    
    for i in range(event_map_len):
        
        ev_name = event_map[i][1]
        ev_time = get_event_time(pevlog, ev_name)
        
        if ev_time:
            
            if ev_name == current_event.get('event_name'):
                if (i+1) == event_map_len:
                    #Edge event case at the right end.
                    ev_waiting_time =  "NA"
                else:
                    ev_time = "In Progress"
                        
            #Get Time of two successive events to get waiting time of first event.
            if i < (event_map_len - 1):
                'To prevent list overflow, when appointment or other edge events happens'
                t1 = [ev[1] for ev in event_list if ev[0] == event_map[i + 1][1] ]
                t2 = [ev[1] for ev in event_list if ev[0] == ev_name ]
                
                if t1 and  t2:
                    ev_waiting_time = format_time(t1[0] - t2[0])
                else:
                    ev_waiting_time =  "NA"
            
            elif (i+1) != event_map_len:
                ev_waiting_time =  "NA"
                ev_time = "In Queue"
        
        else:
            ev_time = "In Queue"
            ev_waiting_time =  "NA"
        
        
        patient_events.append((ev_name,ev_time,ev_waiting_time,event_map[i][0]))
        
        #print patient_events
    
    
    
    template_render = { 'patient_name': get_patient_full_name(header),
                       'header_id': header.id,
                       'stations': patient_events
                       }
        
    return render_to_response("jqmobile/patientstations.html",template_render)
        
                

def jqmobile_patient_station(request,header_id,event_order):
    '''
        Display the information of a particular event of a patient,
        with all of its attributes and interrupts.
        
        input:
            header_id
            event_order - Number corresponds to a event name from clininc_event_map.
            
    '''     
    
    event_order = int(event_order)
    
    #By default we make the patient event is not updatable.
    read_only = False
    
    header = EventSetHeader.objects.get(id = header_id)
    
    pevlog = PatientEventLog.objects.filter(header = header)
    
    event_map  = get_clinic_event_map(header.clinic.id)
          
    event_name = [ ev[1] for ev in event_map if ev[0] == event_order ][0]
    
    event_time = get_event_time(pevlog,event_name)
    #current_event = get_current_patient_event(pevlog)
    
    if event_time:
        'Event already occured, so we disable the event start button.'
        read_only = True
        
    if event_order == len(event_map):
        next_event_order = False
    else:
        next_event_order = event_order + 1
    
    if event_order == 1:
        prev_event_order = False
    else:
        prev_event_order = event_order - 1
    
    station_url = '/jqmobile/patient/' + header_id + '/'
    
    #Attribute and Interrupt operations.
    
    event = Event.objects.filter(name = event_name)
    if event:
        event = event[0]        
        event_attributes = get_event_attributes(header.clinic,event,header)
        
    
    '''
      to check whether the interrupt of a particular patient is completed(start and stop) or not we take the entries from Interrupt table
      and PatientInterruptLog table.If any interrupt has 2 entries in PatientInterruptLog table it means that, that event is completed.If any 
      interrupt has 1 entry in PatientInterruptLog ,it means that , that interrupt is not completed  
    '''    
    interrupts = []
    
    patient_interrupt = []
    
    result = []
    
    inter = Interrupt.objects.all()
        
    for i in inter:
        interrupts.append((i.name,i.id))    
    
    pat_inter  = PatientInterruptLog.objects.filter(header = header_id)
    
    if pat_inter:

        for i in pat_inter:
            patient_interrupt.append((i.interrupt.name,i.interrupt.id))  
        
    
        for i in interrupts:
            c = 0
            for j in patient_interrupt:
                if i[0] == j[0]:
                    c = c+1
            if c == 2:
                result.append((i[0],"complete",i[1]))
            if c == 1:
                result.append((i[0],"stop",i[1]))                      
                   
                                 
    template_data = {'read_only':read_only,
                     'header':header,
                     'event': event,
                     'next_event_order': next_event_order,
                     'prev_event_order': prev_event_order,
                     'station_url': station_url,
                     'patient_name': get_patient_full_name(header),
                     'event_attributes': event_attributes,
                     'patient_header':header.id
                     
                     }
    if result:
        template_data.update({'result':result})
    
    return render_to_response('jqmobile/eventattribute.html',template_data)

def jqmobile_procedures(request,header_id):
       
        header = EventSetHeader.objects.get(id = header_id)
        
        interrupts = []
        
        patient_interrupt = []
        
        result = []
       
        inter = Interrupt.objects.all()
        
        for i in inter:
            interrupts.append((i.name,i.id)) 
            
        data ={
               'header':header_id,
               
               'patient_name': get_patient_full_name(header)
               }        
        
        pat_inter  = PatientInterruptLog.objects.filter(header = header_id) 
        
        if pat_inter:
                 
            for i in pat_inter:
                patient_interrupt.append((i.interrupt.name,i.interrupt.id))
            for i in interrupts:
                c = 0
                for j in patient_interrupt:
                    if i[0] == j[0]:
                        c = c+1
                if c == 0:
                    result.append((i[0],i[1]))      
            data.update({'interrupts':result})
        else:
             data.update({'interrupts':interrupts})   
            
        
            
        return render_to_response('jqmobile/pickaprocedure.html',data)    
           

            


####### Bellow Views are specific to the special Ajax calls #####

def jqmobile_submit_event_attr(request):
    '''
        Attribute value submit from jqm interface, here we will check the attributes values 
        and its required status, if success we send 'OK' or
        
        we send id's of required attributes...
        
        on success - 
        {'status':OK}
        
        on Failure - 
        {'status': FAILED, attributes: { id_attr_'mapid':{ }, id_atrr_'mapid':... }, }
        
    '''
    
    get_data = request.POST
    header_id = get_data.get('header_id')
    event_id = get_data.get('event_id')
    
    header = EventSetHeader.objects.get(id = header_id)
    
    #To collect attributes that requires value but we wont supply it. It will be used for the form validation.
    attributes = []
    
    for attr_name in get_data.iterkeys():

        if attr_name.find('attr_name') == 0:
            #Get the Data from the form field.
            attr_value = get_data[attr_name]
            
            # Attribute name is of the form "attr_name34", where 34 is the id of eventAttribute table.
            attr_id = int(attr_name.split('attr_name')[1])
            
            #Get the EventAttribute Map object.
            attr_map = EventAttributeMap.objects.get(id = attr_id)
            
            if attr_map.required == True:
                #Here we validate the form attribute value.
                if attr_value == '':
                    attributes.append(attr_name)
                    continue #skip other operations.
                 
            #Save value of that object. Use 'filter' instead of 'get', the later one throw an exception in the no record case.
            attr_log = EventSetAttributeLog.objects.filter(header = header, attr_map = attr_map)
            if attr_log:
                attr_log = attr_log[0]
                attr_log.value = attr_value
                attr_log.save()
                
            else:
                EventSetAttributeLog(header = header, attr_map = attr_map, value = attr_value).save()
            
    if attributes :
        response = {'status':'FAILED', 'attributes':attributes}
    else:
        response = {'status':'OK'}
    
    
    response = simplejson.dumps(response)
    return HttpResponse(response, mimetype="application/json")
    
    

def jqmobile_event_finished(request):
    '''
        This function will be called when we click on the event finish button,
        
        return success, only if there is no attributes or any pending interrupts.
        
        { status:OK }
        
        Fail condition: {status: FAILED, 
                         interrupts:[[intr_id,intr_name],..],
                         attributes:[[attr_id,attr_name],..]
                        }
    '''
    
    post_data = request.POST
    
    header_id = post_data.get('header_id')
    event_id = post_data.get('event_id')
    
    header = EventSetHeader.objects.get(id = header_id)
    event = Event.objects.get(id = event_id)
    
    attributes = get_event_attributes(header.clinic,event,header)
    
    pending_attr = [(a.get('attrmap_id'),a.get('attr_name')) for a in attributes if a.get('attr_required')==True and a.get('attr_value')==None]
    
    pending_intr = check_pending_interrupts(header.id)
    
    
    response = {'status':'FAILED'}
    if pending_attr or pending_intr:
        response.update({'interrupts':pending_intr,'attributes': pending_attr})
    else:
        #Save this event corresponding to this patient.
        #pevlog = PatientEventLog.objects.filter(header = header, event = event)
        
        #if not pevlog:
             #To prevent multiple saving of same event.
        #    PatientEventLog(header = header, event = event).save()
        
        "  if status response status == 'OK', we update the same event change to stomp channel also. "
        username = request.user.username
        password = request.COOKIES.get(settings.SESSION_COOKIE_NAME,None)
        trigger_event.delay(event.name, header_id,{ 'username':username, 'password': password })    
        
        response['status'] = 'OK'

    response = simplejson.dumps(response)
    
    return HttpResponse(response,mimetype="application/json")

        
def jqmobile_process_interrupt(request):        
    
    '''
     This function is used to save the status of interrrupts in PatientInterrupt table
     status: started or stopped
    '''
    post_data = request.POST
    
    header_id = post_data.get('header_id')
    
    interrupt_id = post_data.get('interrupt_id')
    
    status = post_data.get('status')
    
    header_obj = EventSetHeader.objects.get(id=header_id)
    
    interrupt = Interrupt.objects.get(id=interrupt_id)
    
    PatientInterruptLog(header=header_obj,interrupt=interrupt,status=status).save()
    
    msg = {'header':header_id,'interrupt_id':interrupt_id,'status':status,'interrupt_name':interrupt.name}
    
    msg = simplejson.dumps(msg)
    
    return HttpResponse(msg,mimetype="application/json")