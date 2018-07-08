from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from signin.models import *
from django.contrib.auth.models import User
from django.utils.hashcompat import md5_constructor, sha_constructor

from django.contrib.auth.models import *
import simplejson
import datetime
from django import forms
from django.conf import settings
from utility import get_clinic_event_map
import random

#Celery modules.
from djcelery.models import PeriodicTask, IntervalSchedule


@login_required(login_url = '/admin')
def Notifier_Settings(request):
    def get_old_notifier_settings():
        global old_values
        from signin.models import Settings_General
        old_values = {}
        if  Settings_General.objects.filter(field_type = "notifier"):
             
            for i in Settings_General.objects.filter(field_type = "notifier"):
                old_values['enable_disable'] = (str(i.enable_disable))
                argument3 = (str(i.argument3)).split(",")
                
                old_values['time_limit_minutes'] = argument3[0]
                old_values['time_limit_hours'] = argument3[1]
                old_values['from_mail_addr'] = str(i.argument2)
                old_values['to_mail_addr'] = (str(i.argument1))
                old_values['alert_mail_sub'] = str(i.argument4)
        else:
            old_values['enable_disable'] = 'No'
            old_values['to_mail_addr'] = ''
            old_values['from_mail_addr'] = ''
            old_values['time_limit_minutes'] = 10
            old_values['time_limit_hours'] = 2
        return old_values
    
    from signin.notifier import Notifier_Settings_Form
    ''' the notifier settings view... calls the the notifier settings template '''
    if request.method == 'POST':
        ##raise NameError('Hi')
        form = Notifier_Settings_Form(request.POST)
        if form.is_valid():
           field_type = "notifier"
           alert_message = 'Alert :- Patient {fname} is still waiting to be  processed...'
           enable_disable = form.cleaned_data['enable_disable']
           if enable_disable == "No":
               to_mail = ""
               from_mail = ""
               time_mins = ""
               time_hours = ""
               alert_message = ""
           elif enable_disable == "Yes":    
               to_mail = str(form.cleaned_data['to_mail'])
               from_mail = str(form.cleaned_data['from_mail'])
               time_mins = form.cleaned_data['time_mins']
               time_hours = form.cleaned_data['time_hours']
               ###raise NameError(form.cleaned_data['from_mail'])
               
           to_db = Settings_General(id = 1, field_type = field_type, enable_disable = enable_disable, argument1 = to_mail, argument2 = from_mail, argument3 = str(time_mins + "," + time_hours), argument4 = alert_message, change_time = datetime.datetime.now())
           to_db.save()
           return HttpResponseRedirect('')

          
        else:
            pass    
    else:
        form = Notifier_Settings_Form(initial = {'enable_disable':get_old_notifier_settings()['enable_disable'],
                                             'from_mail':get_old_notifier_settings()['from_mail_addr'],
                                             'to_mail':get_old_notifier_settings()['to_mail_addr'],
                                             'time_mins':get_old_notifier_settings()['time_limit_minutes'],
                                             'time_hours':get_old_notifier_settings()['time_limit_hours']
                                             })    
        #pass
    return render_to_response("admin/signin/notifier_template.html", {'form':form})



def alert_home(request):
    '''
        Alert Home, This View list the set of available Alerts for all the clinics.
        From this list we add/modifiy/remove the specfic alerts.
    '''
    
    alert_confs = AlertConfiguration.objects.all()
    
    response = {'alert_confs':alert_confs}
    
    return render_to_response('admin/signin/alert_home.html', response, RequestContext(request, {}))

def alert_form_edit(request, conf_id):
    '''
        Custom form for the Adidtion and Modification of the Alert configuration.
    '''
    
    alert_conf = get_object_or_404(AlertConfiguration, id = conf_id)
    
    clinic_list = Clinic.objects.filter(location = alert_conf.clinic.location)
    location_list = Location.objects.all()
    
    event_map = get_clinic_event_map(alert_conf.clinic.id)
    alert_events = alert_conf.event_list.split(",")
    
    event_view = []
    for event in event_map:
        if event[1] in alert_events:
            event_view.append((event[1], 1))
        else:
            event_view.append((event[1], 0))
    
    
    response = {'alert_conf':alert_conf, 'clinic_list':clinic_list , 'location_list':location_list, 'event_view':event_view, 'STATIC_URL':settings.STATIC_URL}
    
    return render_to_response('admin/signin/alert_form.html', response, RequestContext(request, {}))
    

def alert_form_add(request):
    ' Add New Alert configurations. '
    location_list = Location.objects.all()
    response = {'location_list':location_list, 'STATIC_URL':settings.STATIC_URL}
    return render_to_response('admin/signin/alert_form.html', response, RequestContext(request, {}))


def alert_form_save(request):
    '''
        Save the New Alert configurations.
    '''
    clinic = get_object_or_404(Clinic, id = request.POST['clinic_list'])
    
    location = get_object_or_404(Location, id = request.POST['location_list'])
    
    from_addr = request.POST['from_addr']
    to_addr = request.POST['to_addr']
    name = request.POST['name']
    
    event_list = request.POST.getlist('event_names')
    
    waiting_time = int(request.POST['waiting_time'])
    enabled = request.POST['enabled']
    
    alert_retry = int(request.POST['alert_retry'])
    
    alert_interv = int(request.POST['alert_interv'])
    
    comp_event_list = ','.join(event_list)
    
    check_dup = AlertConfiguration.objects.filter(clinic = clinic,
                                                  event_list = comp_event_list,
                                                  )
    
    if check_dup:
        '''
            While modifying a alert rule we didn't changed the 
            a) Clinic
            b) Event list
                        
            then we keep the existing rule by updating other fields, otherwise,
            we create new alert rule instead of modifying it.
            
            Here we modifying the existing rule.
        '''
                      
        check_dup = check_dup[0]
             
        #take old interval time.
        interval_old = check_dup.alert_interv
        
        check_dup.from_addr = from_addr
        check_dup.to_addr = to_addr
        check_dup.name = name
        check_dup.waiting_time = waiting_time
        check_dup.enabled = enabled
        check_dup.alert_retry = alert_retry
        check_dup.alert_interv = alert_interv
        check_dup.save()
        
        ###Update the Periodic tasks interval time.###
        
        
        
        if interval_old != alert_interv:
            'If there is any change in the interval we update the periodic task.'
            periodic_task = PeriodicTask.objects.filter(args = simplejson.dumps([check_dup.id]))
            
            if periodic_task:
                #updating the new interval with existing periodic task.
                periodic_task = periodic_task[0]
                
                #Check for the new interval object associated with this time.
                interval = IntervalSchedule.objects.filter(every = alert_interv, period = 'minutes')
                if interval:
                    interval = interval[0]
                else:
                    interval = IntervalSchedule(every = alert_interv, period = 'minutes')
                    interval.save()
                
                
                periodic_task.interval = interval
                periodic_task.save()
            else:
                'No Periodic task for this rule... create one..'
                #Adding periodic task.
                add_periodic_task(alert_interv, check_dup)
        
    else:
        'Adding new rule.'
        
        alert_conf = AlertConfiguration(clinic = clinic,
                                        from_addr = from_addr ,
                                        to_addr = to_addr,
                                        name = name,
                                        waiting_time = waiting_time,
                                        enabled = enabled,
                                        event_list = comp_event_list,
                                        alert_retry = alert_retry,
                                        alert_interv = alert_interv
                                        )
        
        alert_conf.save()
        
        #Adding new periodic task.
        add_periodic_task(alert_interv, alert_conf)
        
       
        
         
    
    return HttpResponseRedirect('/admin/signin/alertconfiguration/')
    
    #response  = HttpResponse(mimetype='text/plain')
    
    #response.write(check_dup)
    #response.write()
    
    #return response



def add_periodic_task(every, alert_conf):
    
    '''
        
        ###Add one celery periodic task for this rule###
        Accept interval time and alert_conf_id, and add new periodic task with these details.
        intervals reused if already exist.
    '''
        
        
    #1. Set Interval time on IntervalSchedule Table.
    interval = IntervalSchedule.objects.filter(every = every, period = 'minutes')
        
    if interval:
        interval = interval[0]
    else:
        'No interval exist, add new one.'
        interval = IntervalSchedule(every = every, period = 'minutes')
        interval.save()
        
        
    #2. Adding Periodic task
    
    #generate unique name, This make user to freely assign name for Alert Confs.
    name = "%s-%s" % (alert_conf.name, random.randrange(start = 100, stop = 999))
    
    periodic_task = PeriodicTask(name = name,
                                     task = 'signin.tasks.process_an_alert',
                                     args = simplejson.dumps([alert_conf.id]),
                                     interval = interval,
                                     enabled = True
                                     )
    periodic_task.save()    
    
    

def ajax_get_clinics(request):
    '''
        return the all clinics under the given location id.
    '''
    location_id = request.REQUEST.get('location_id', None)
    
    clinic_list = Clinic.objects.filter(location = location_id).values_list('id', 'name', 'location__name')
    
    json_data = simplejson.dumps([list(a) for a in clinic_list])
    
    return HttpResponse(json_data, mimetype = 'application/json')
    
def ajax_get_eventmap(request):
    '''
        returns Event map order of given clinic.
    '''
    clinic_id = request.REQUEST.get('clinic_id', None)
    
    event_map = [ list(a)[1] for a in   get_clinic_event_map(clinic_id)]
    
    json_data = simplejson.dumps(event_map)
    
    return HttpResponse(json_data, mimetype = 'application/json')
    
def ajax_get_attrs(request):
    '''
        Return the list of Attributes, that will be used to bind attrs to events under a clinic..
        return value: [['attr_name',attr_id],[],[]..etc..]    
    '''
    
    attributes = Attribute.objects.all()
    json_msg = simplejson.dumps([ (attr.name, attr.id) for attr in attributes ])
    return HttpResponse(json_msg, mimetype = 'application/json')
    
def ajax_get_event_attr_list(request):
    '''
        Function which return the list of event to attribute map, under a clinic.
        
        return value is in json, [[['attr_name',id],required,hidden],[ ['attr_name2',id],reqired,hidden ] .. etc..]
    '''
    
    event = Event.objects.filter(name = request.GET['event_name'])[0]
    
    attr_map = EventAttributeMap.objects.filter(clinic = request.GET['clinicID'], event = event)
    
    map = [((a.attribute.name, a.attribute.id), a.required, a.hidden) for a in attr_map]
    
    json_map = simplejson.dumps(map)
    
    return HttpResponse(json_map, mimetype = 'application/json')


def clinic_design(request):
    ''' UserManager
    Main Clinic designing view. Which extend the django admin templates.
    '''
    clinics = Clinic.objects.all()
    response = {"clinics":clinics}
    return render_to_response("admin/signin/clinic_admin.html", response, RequestContext(request, {}))


def clinic_admin(request, clinic_id):
    '''
        View to define the Clininc Design and mapping the events to each clinincs.
        
        Default Event order for a clininc:- 
            Total Events : 6
            signin, registration, triage , provider , checkout , Appointment.
            
        In Costume Design This will be any number of events with different order.  
   
    '''
    if request.is_ajax():
        '''
            Process the POST request inside this view itself.
        '''
        try:
            
            clinicID = request.POST['clinicID']
            #events = request.POST['id_event1_name']
            
            #Event order that will be updated to this clinicID.
            events = []
            length = (len(request.POST) - 1)
            from django.contrib.auth.models import User
            #Traverse through the id field of select tag from POST 
            for i in range(1, length + 1) :
                index = 'id_event' + str(i) + '_name'
                events.append(request.POST[index])
            
            ### MODEL UPDATION SECTION ###
            #Delete all the existing mapping for this Clinic.
            clinic = Clinic.objects.get(id = clinicID)
            ClinicEventMap.objects.filter(clinic = clinic).delete()
            
            #Add New mappings to the server.
            
            position = 1
            for event in events:
                event_obj = Event.objects.get(name = event)
                ClinicEventMap(clinic = clinic, event = event_obj , position = position).save()
                position += 1
            
            msg = {"status": 'OK'}
            
        except:
            msg = {"status":"Failes"}  #simplejson.dumps({"events":events})
        #Return status in json format.
        msg = simplejson.dumps(msg)
        return HttpResponse(msg, mimetype = "application/json")
        #return render_to_response('admin/signin/test.html',{'post',request.POST['test']})
   
    '''
     Here we get the clinic current event map.
    '''
    #Default Clinic design
    default = True
    
    clinic = Clinic.objects.get(id = clinic_id)
    event_map = ClinicEventMap.objects.filter(clinic = clinic)
    
    #This will store the clinic_event mappings.sha1$e9c15$a95034952e05627bb82396b994f8243bcc2454e7
    clinic_events = []
    
    if event_map.count() != 0:
        '''
            Get custom Event maps from the ClinicEventMap.
        '''
        default = False
        clinic_events = []
        for map in event_map:
            '''
            Create tupple with event and its position.                
            '''
            clinic_events.append((map.position, map.event.name))
    else:
        '''
        Collect default Event map.
        '''
        clinic_events = [(1, 'signin'), (2, 'registration'), (3, 'triage'), (4, 'provider'), (5, 'checkout'), (6, 'appointment')]
  
    #Collect all total Events 
    events = Event.objects.all()
    response = {"clinic":clinic, "default":default, 'clinic_events':clinic_events, 'events':events}
    
    return render_to_response('admin/signin/change_from.html', response, RequestContext(request, {}))



def attribute_admin(request, clinic_id):
    '''
        Main view to List and updating the attributes assigned to each events under a clinic.
    '''

    clinic = get_object_or_404(Clinic, id = clinic_id)
    
    if request.is_ajax():
        'Attribute modification request, via ajax...'
        
        #Variable which hold the total number of attributes in the current request.
        length = int(request.POST['length'])
        event = Event.objects.filter(name = request.POST['event_selected'])[0]
             
        
        #remove all attribute map for this event and clinic pair., if there is no attribute while saving we delete every thing.
        EventAttributeMap.objects.filter(event = event, clinic = clinic).delete();
        
        if length > 0:
            'Only update the rows if some attributes are there, other wise we delete it all.'
            for index in range(length):
                'Iterate via all post variables and insert the attribute and required starts ...'
                
                attr = get_object_or_404(Attribute, id = request.POST.get('attr' + str(index)))
                
                required = request.POST.get('attr_required' + str(index), False)
                #Make it boolean True
                if required:
                    required = True
                
                hidden = request.POST.get('attr_hidden' + str(index), False)
                #Make hidden to Boolean format.
                if hidden:
                    hidden = True
                
                
                EventAttributeMap(event = event, clinic = clinic, attribute = attr, required = required, hidden = hidden).save()
        
        msg = simplejson.dumps({'status':'OK'})
        return HttpResponse(msg, mimetype = 'application/json')                        
        
        
    else:
        'List the existing Attributes of each events under a clinic'
        
        respons = {}
        
        #Get event map from the common function, return value format is tupple , [(signin,1),(),...etc]
        events = get_clinic_event_map(clinic.id)
        '''
        ClinicEventMap.objects.filter(clinic = clinic)
        if not events:
            'No custom events, so take default one.'
            events = [(1,'signin'),(2,'registration'),(3,'triage'),(4,'provider'),(5,'checkout'),(6,'appointment')]
        '''
        
        #Attributes of the first Event from the eventmap table.
        first_event = Event.objects.filter(name = events[0][1])
        
        attributes = Attribute.objects.all()
        
        event_attr_list = EventAttributeMap.objects.filter(clinic = clinic, event = first_event)
        
        #event_attr_list = {'1':1,'2':2}
        

        response = {'clinic':clinic, 'events': events, 'attributes': attributes, 'event_attr_list':event_attr_list}
        return render_to_response('admin/signin/assign_attributes.html', response, RequestContext(request, {}))        
        
        
        

 

def add_user(request):
    'View for the Simplified User addition to the django Auth module.'
    users = User.objects.all()
    response = {"users":users}
    return render_to_response('admin/signin/adduser.html', response, RequestContext(request, {}))


def ajax_savenewuser(request):
    'Save new user from the simplified user addition form.'
    
    uname = request.REQUEST.get('uname')
    password = request.REQUEST.get('password')
    #new = check_password(password)
    new = get_hexdigest('md5', '', password)
    staff = request.REQUEST.get('staff')
    superstat = request.REQUEST.get('superstat')
    new_user = User(username = uname , password = new , is_staff = staff, is_superuser = superstat)
    new_user.save()
    new = new_user.check_password(password)
    return HttpResponse("1", mimetype = "text/plain")
