# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404
from django.shortcuts import get_object_or_404
from django.conf import settings 
from skgargpms.signin.models import * 
import datetime,time,StringIO
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.template import loader,Context
from django.db.models import Sum
import ho.pisa as pisa
from django.db.models import Q #To support more complex query set.

import pytz #To support Multiple timezone.

from utility import get_clinic_event_map, get_patient_full_name


def get_current_worktime(location_obj):
    '''
        To support old codes, the program will return morning/evening and the current time in datetime.time format.
        
        Changes to this function:- to support localtime zone a Browser.
        
        When user entering the clinic start_time and end_time , 
            they expecting those values based on their timezone.
            But at server we storing times in UTC(But user point of view this time is in their format,
            so we need to manage it correctly.).
            
            So this function will return current time based on the local timezone. 
    '''
    d = datetime.datetime.now()
    dt_s = d.strftime("%H:%M")
    if dt_s <= settings.EVENING_TIME:
        work_time = 'morning'
    else:
        work_time = 'evening'
    
    #Here we fetch current time by changing system UTC time to user localtimezone and then return objects.
    
    timezone = location_obj.timezone
    
    #Standardize the timezone representation.
    timezone_std = pytz.timezone(timezone)
    
    #Get current UTC time and give timezone info to it.
    now_utc = pytz.utc.localize(datetime.datetime.now())
    
    local_time = now_utc.astimezone(timezone_std)
    
    #get %H:%M:%S from the local_time
    dt_s = datetime.time(local_time.hour, local_time.minute, local_time.second)
    return work_time,dt_s


def get_current_clinics(default_location = ''):
    
    '''
    This function will return list of clinic objects, if they are in the current working time of corresponding 
    locations.
    
    When saving clinics start_time and end_time, eventhough the time is in UTC at server but the time is localtime
    from the user point of view.
         
    '''
    
    #Actually Query result are of type QuerySet, But here we using simple list because we need to add objects.
    current_clinics = []
    
    #To support the default location.
    if default_location :
        locations = [default_location]
    else:
        locations = Location.objects.all()
    
    midnight=datetime.time(0,0,0)
    
    #Fetch all clinincs from Db. Do only once.
    clinics = Clinic.objects.all()
    
    for location in locations:
        
        work_time = get_current_worktime(location)
        
        #print work_time
        first=Q(start_time__lte = work_time[1],end_time__gte = work_time[1])
        second=Q(start_time = midnight,end_time = midnight)
        third = Q(location = location)
        
        query_set = third & (first|second)
        
        #print query_set
        #List instance have __add__ method.
        current_clinics += clinics.filter(query_set)
        
    return current_clinics


def get_request_period(request,clinic):
    
    '''
        This clinic also changed to support the multiple timezone. So we accept clinic object as another argument.
    '''
    timezone = clinic.location.timezone
    local_timezone = pytz.timezone(timezone)
    
    if request.REQUEST.has_key("date"):
        dt = datetime.datetime.strptime(request.REQUEST['date'],"%Y-%m-%d")
        
    
    else:
        
        #Naive UTC time
        dt = datetime.datetime.now()
        
        #Get local time, using timezone info.
        #timezone = clinic.location.timezone
        #local_timezone = pytz.timezone(timezone)
        dt_utc = pytz.utc.localize(dt)
        #Local time
        dt = dt_utc.astimezone(local_timezone)
        
        #Time ahead from mid night at localtime
        diff = datetime.timedelta(hours = dt.hour, minutes = dt.minute , seconds = dt.second, microseconds = dt.microsecond)
        
        #To get One day ahead, as upper bound.
        add  = datetime.timedelta(days =1)
        
        #Get starting time of current day at localtime, inclusive.
        dt_start = dt - diff
        #Get next days start hour as upper hound exclusive. 
        dt_end   = dt_start + add
        
        #Convert local tiemzone to UTC format, to support db query.
        timezone_utc = pytz.timezone("UTC")
        
        dt_start_utc = dt_start.astimezone(timezone_utc)
        dt_end_utc   = dt_end.astimezone(timezone_utc)
        
        return dt_start_utc,dt_end_utc
    
    #timezone = clinic.location.timezone
    #
    #local_timezone = pytz.timezone(timezone)
    #local_dt = dt.replace(tzinfo=local_timezone)
    local_dt=local_timezone.localize(dt,is_dst=True)
    utc_dt = local_dt.astimezone(pytz.utc)   
    delta  =  datetime.timedelta(days=1)
    dtEnd  =  utc_dt + delta
    return utc_dt, dtEnd

'''
def get_clinic_event_map(clinicID):
    \'''
        return array of (event,position) tupples of a given Clinic or it will return Boolean False. 
    \'''
    
    event_map = []
    #clinic = Clininc.objects.get(id = clinicID)
    
    mapping = ClinicEventMap.objects.filter(clinic = clinicID )
    
    
    clinic = Clinic.objects.get(id=clinicID)
    appointment=clinic.location.appointment
    #return appointment
    
    #location=Location.objects.get(name=clinic.location)
    #appointment=location.appointment
    position = 1
    for map in mapping:
        event_map.append((position,map.event.name))
        position += 1
    
    if mapping:
        c=0
        #to avoid the appointment event from frontdesk corresponding to the clinic whose appointment event is set to false
        if  not appointment:
          for i in event_map:
              c=c+1
              if i[1]=="appointment" :
                  del event_map[c-1] 
            
        return event_map
    else:
        #Return default event map.
        default_event_map=[(1,'signin'),(2,'registration'),(3,'triage'),(4,'provider'),(5,'checkout'),(6,'appointment')]
        c=0
        #to avoid the appointment event from frontdesk
        if  not appointment:
          for i in default_event_map:
              c=c+1
              if i[1]=="appointment" :
                  del default_event_map[c-1]
        
        return default_event_map
'''
  
def get_event_time(patient_event_logs,event_name):
    '''
        Here we return the Time of occarance  of this event from the patientEventLog Model or else it return False.
    '''
    event_time_local = False
    
    #By default there will be minimum of one entry in the PatientEventLogs when patient signin.So from that 
    #we can featch the timezone of location.
    clinic_timezone_name = patient_event_logs[0].header.clinic.location.timezone
    
    for pevlog in patient_event_logs:
        if pevlog.event.name == event_name:
            '''
                we changed the old methods to give custom timezone support based on the location.
            '''
            #Get localtimezone representation.
            event_time_local = get_local_time(clinic_timezone_name,pevlog.dateTime)
     
    return event_time_local
    

def get_local_time(timezone_name,time_utc):
    '''
        Function which return localtime by converting UTC time to the local_timezone format.
        
        eg:
        localtime_zone = EST
        time_utc       = timeobject in UTC format.
    '''
    #Convert timezone name to standard form
    local_timezone = pytz.timezone(timezone_name)
    
    #Eventhough the time in the DB is in UTC, it need some more info with existing timeobject.(zoneinfo=<UTC>) 
    #to work with pytz info.
    time_utc_correct = pytz.utc.localize(time_utc)
    
    #Get localtime 
    local_time = time_utc_correct.astimezone(local_timezone).strftime("%H:%M")
    
    return local_time
     

def updateDict(request):
    ansDict = dict()
    ansDict["STATIC_URL"] = settings.STATIC_URL
    ansDict["user"] = request.user
    # ansDict['left_menu'] = get_current_clinics()
    return ansDict


# @permission_required('patient.can_sign_in')
@staff_member_required
def signin(request):
    ansDict = updateDict(request)
    ansDict['menu'] = 'signin'
    
    if request.REQUEST.has_key("locationID"):
        
        location = get_object_or_404(Location,id=request.REQUEST.get("locationID",None))
        ansDict["location"] = location
        providers = Provider.objects.filter(loc=location) #select the provider info corresponding to a location.
        ansDict['providers'] = providers
        clinics = get_current_clinics(default_location = location)
        
        ansDict['clinics'] = clinics
        
        #Added other parameters requred for the comet session.
        comet = {"SESSION_COOKIE_NAME":settings.SESSION_COOKIE_NAME,"HOST":settings.INTERFACE,
                 "STOMP_PORT":settings.STOMP_PORT,"USER":request.user}
        
        ansDict.update(comet)
        
        return direct_to_template(request,'signin.htm', ansDict)
    else:
        # raise Exception('q');
        ansDict['locations'] = [x for x in Location.objects.order_by('name') if x.clinic_set.count()>0]
        return direct_to_template(request,'signin_base.htm',ansDict)
        


@staff_member_required
def frontdesk(request):
    '''
        List the Patients under a Clinic.
    '''
    ansDict = updateDict(request)
    
    ansDict['menu'] = 'frontdesk'
    ansDict['left_menu'] = Clinic.objects.all()
    #if request.REQUEST.has_key("date"):
        #dt = datetime.datetime.strptime(request.REQUEST['date'],"%Y-%m-%d")
    
    if not request.REQUEST.has_key("clinicID"):
        #ansDict['work_time'] = get_current_worktime()
        ansDict['clinics'] = get_current_clinics()
        return direct_to_template(request,'frontDesk-base.html',ansDict)
    
    clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))

    #Get all clinics under this clinic location.
    all_clinics = Clinic.objects.filter(location = clinic.location.id ) 
    
    ansDict["all_clinics"] = all_clinics
    
    ansDict["clinic"] = clinic
    
    
    
    ansDict["location"] = clinic.location
    
    ansDict['interrupts'] = Interrupt.objects.all()
    
    #Get Clinic Event Mapdefault_clinic_event_map = []
    
    
    event_map = get_clinic_event_map(clinic.id)
    #if not event_map:
    #    '''
    #        No map information in the table. Take default map format.
    #    ''' 
    #    event_map = [(1,'signin'),(2,'registration'),(3,'triage'),(4,'provider'),(5,'checkout'),(6,'appointment')]
        
    ansDict['clinic_event_map'] = event_map 
    
    #Get Details to Presents Patients details.
    clinicID = request.REQUEST["clinicID"]
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
    ansDict['patients'] = patients
    
    #Come Variables
    
    #Channel name is specific for each Clinics. At frontdesk we list the patients of one clinic at a time.
    channel_name = 'frontdesk'+ clinicID
    
    comet = {"SESSION_COOKIE_NAME":settings.SESSION_COOKIE_NAME,"HOST":settings.INTERFACE,"CHANNEL_NAME":channel_name,
             "STOMP_PORT":settings.STOMP_PORT,"USER":request.user}
    
    provider_list = Provider.objects.filter(loc = clinic.location.id)#select the provider info corresponding to a location
    ansDict['provider_list'] = provider_list
    
    ansDict.update(comet)
    
    
    return direct_to_template(request, 'frontDesk.html',ansDict);

#@staff_member_required
def testpage(request):
    
    ansDict = updateDict(request)
    ansDict['menu'] = 'frontdesk'
    ansDict['left_menu'] = Clinic.objects.all()
    
    if not request.REQUEST.has_key("clinicID"):
        #ansDict['work_time'] = get_current_worktime()
        ansDict['clinics'] = get_current_clinics()
        return direct_to_template(request,'testproject.html',ansDict)
    

def stomptester(request):
    
    ansDict = updateDict(request)
    ansDict['menu'] = 'frontdesk'
    ansDict['left_menu'] = Clinic.objects.all()
    ansDict['SESSION_COOKIE_NAME'] = settings.SESSION_COOKIE_NAME
    
    return direct_to_template(request,'stomp_tester.html',ansDict)
    


@staff_member_required
def reports(request):
    ansDict = updateDict(request)
    ansDict['menu'] = 'reports'
    ansDict['left_menu'] = Clinic.objects.all()
    
    if not request.REQUEST.has_key("clinicID"):
        #ansDict['work_time'] = get_current_worktime()
        ansDict['clinics'] = get_current_clinics()
        return direct_to_template(request,'reports-base.html',ansDict)
    
    clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
    
    ansDict["clinic"] = clinic
    
    #Added variables required for the comet session at report page.
    channel_name = 'frontdesk' + str(clinic.id)
    comet = {"SESSION_COOKIE_NAME":settings.SESSION_COOKIE_NAME,"HOST":settings.INTERFACE,"CHANNEL_NAME":channel_name,
             "STOMP_PORT":settings.STOMP_PORT,"USER":request.user}
    ansDict.update(comet)
    
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
                                                    
    return direct_to_template(request, 'reports.html',ansDict);




def payment(request):
    ansDict = updateDict(request)
    ansDict['menu'] = 'paymenthistory'
    ansDict['left_menu'] = Clinic.objects.all()
    
    if not request.REQUEST.has_key("clinicID"):
        #ansDict['work_time'] = get_current_worktime()
        ansDict['clinics'] = get_current_clinics()
        return direct_to_template(request,'payment-base.html',ansDict)

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
    return direct_to_template(request,'payment.html',ansDict)


def installBase(request):
    ansDict = updateDict(request)
    # return render_to_response('blackpage.html', ansDict)

    locations = ["Davis Hwy Family Practice", "Pea Ridge Family Care Center"]
    clinics  = ['Cash, Affordable Care','Pea Ridge Family Care Center']
    work_times = ['morning','evening']

    for l in locations:
        location,_ = Location.objects.get_or_create(name=l)
        for c in clinics:
            for wt in work_times:
                cc,_ = Clinic.objects.get_or_create(location=location, name=c, work_time = wt)

    for event_name in 'signin registration triage provider checkout appointment payment delete'.split():
        Event.objects.get_or_create(name=event_name)

    return direct_to_template(request,'blackpage.html', ansDict)

def print_index_view(request):
    print render_to_string('index.html', {'user':request.user})


def make_pdf(func):
    def wrap(request,*args, **kwargs):
        response = func(request,*args, **kwargs)
        if hasattr(response, "pdf"):
            filename = response.pdf
            content = response.content
            output = StringIO.StringIO()
            pdf = pisa.CreatePDF(StringIO.StringIO(content),output)
            response = HttpResponse(output.getvalue(),mimetype='application/pdf')
        return response
    return wrap


@make_pdf
def export_pdf(request):
    
    pdf_type = request.REQUEST.get("type",None)
    
    clinic = get_object_or_404(Clinic, id=request.REQUEST.get("clinicID",None))
    
    dtStart,dtEnd = get_request_period(request,clinic)
                       
    '''
    try:
        date = time.strptime(request.REQUEST.get('date',''),'%Y-%m-%d')
        date = datetime.date.fromtimestamp(time.mktime(date))
    except Exception, e:
        raise
        date = datetime.date.today()
           
    dtStart = datetime.datetime(date.year,date.month,date.day,0,0,0)
    dtEnd = dtStart + datetime.timedelta(days=1)file (6
    '''
    
    context = {'date':dtStart}
    
    if pdf_type == "frontdesk":
       # patients = []
        dataset = EventSetHeader.objects.filter(dateTime__gte=dtStart,dateTime__lt=dtEnd)
        event_map = get_clinic_event_map(clinic.id)        
        if request.REQUEST.has_key("clinicID"):
            #clinic = get_object_or_404(Clinic, id=request.REQUEST['clinicID'])
            context['clinic'] = clinic
            dataset = dataset.filter(clinic = clinic)
        '''           
        for h in dataset:
            x = {}
            x['patient'] = h.patient
            x['file (6events'] = {}
            for ev in PatientEventLog.objects.filter(header = h):
                x['events'][ev.event.name] = ev.dateTime

            x['payment'] = Payment.objects.filter(header = h).aggregate(sum=Sum('amount'))['sum']
            # for i in xrange(100):
            patients.append(x)
            '''
        c = len(event_map)    
        clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
        patients = []
        #patient = {}
        #events = []    
        for esh in dataset:
            patient_name = get_patient_full_name(esh)#esh.patient.lName + "," +  esh.patient.fName + "," +  str(esh.patient.dob)
            patient_event_logs =  PatientEventLog.objects.filter(header=esh)
            events=[]
            #for event in event_map:
              #event_time = get_event_time(patient_event_logs,event[1])
            event_time_first = get_event_time(patient_event_logs,event_map[0][1]) 
            event_time_last = get_event_time(patient_event_logs,event_map[c-1][1]) 
            events.append(event_time_first)
            events.append(event_time_last)              
            payment =  Payment.objects.filter(header = esh).aggregate(sum=Sum('amount'))['sum'] 
            patient = { "patient_name" : patient_name, "header":esh.id,"events":events } 
            patients.append(patient)
            
        #context['events'] = patients
        context['patients'] = patients
        #context['clinic_event_map'] = event_map
        context['clinic_event_map_first'] = event_map[0][1]
        context['clinic_event_map_last'] = event_map[c-1][1]
        template="pdf/frontdesk.htm"
        # raise Exception(pat'''ients)
        
    elif pdf_type == "reports":
        
        from collections import defaultdict
        clinic = get_object_or_404(Clinic.objects, id=request.REQUEST.get("clinicID",None))
        def _diff(dict, a_key, b_key):
            dfl = datetime.datetime(year=datetime.MINYEAR,month=1, day=1)
            a = dict.get(a_key,dfl)
            b = dict.get(b_key,dfl)
            # raise Exception(a,b)
            td = (b - a)
            td = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
            if (td < 0):
                return None
            else:
                return td/60
        
        '''
        patients = []
        dataset = EventSetHeader.objects.filter(dateTime__gte=dtStart,dateTime__lt=dtEnd)
        if request.REQUEST.has_key("clinicID"):
            #clinic = get_object_or_404(Clinic, id=request.REQUEST['clinicID'])
            context['clinic'] = clinic
            dataset = dataset.filter(clinic = clinic)
        for h in dataset:
            x = {}
            x['patient'] = h.patient
            x['events'] = {}
            for ev in PatientEventLog.objects.filter(header = h):
                x['events'][ev.event.name] = ev.dateTime
            x['events']=defaultdict(str,x['events'])
            patients.append(x)
        context['events'] = patients
       '''
        if request.REQUEST.has_key("clinicID"):
            clinic = get_object_or_404(Clinic, id=request.REQUEST['clinicID'])
            eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
        
        event_map = get_clinic_event_map(clinic.id)
        default_clinic_event_map = []
        for i in range(len(event_map)):
           '''
             creating special header names for report templates.
           '''
           if (i+1) < len(event_map):
            default_clinic_event_map.append(event_map[i][1] + ' To ' + event_map[i+1][1])
           else:
            default_clinic_event_map.append(event_map[i][1])
        
        context['default_clinic_event_map'] = default_clinic_event_map
        dtStart, dtEnd = get_request_period(request,clinic)
        eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
        patients = []
        #patient = {}
        events = []
        pel_temp = {}
        for esh in eshs:
            pels = PatientEventLog.objects.filter(header = esh)
            patient_name = get_patient_full_name(esh)#esh.patient.lName + "," +  esh.patient.fName + "," +  str(esh.patient.dob)
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
            patient = {"patient_name":patient_name,"header":esh.id,"events":events} 
            if not 'delete' in pel_temp:
              '''
               If "delete" entry were present, we just discard that user from frontdesk.
              '''
              patients.append(patient) 
            pel_temp = {}
            events = []
        context['patients'] = patients                 
        template = "pdf/reports.htm"
        
    elif pdf_type == 'payments':
        if not request.REQUEST.has_key("clinicID"):
            raise Http404
        clinic_id = request.REQUEST['clinicID']
        #clinic = get_object_or_404(Clinic, id=clinic_id)

        eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart).order_by("dateTime")
        counts=eshs.count()     
        total = {}
        total['cash']=reduce(lambda a,b: a+b.get_cash(), eshs, 0.0)
        total['cc']=reduce(lambda a,b: a+b.get_cc(), eshs, 0.0)
        total['total'] = total['cash'] + total['cc']
        total['positivetotal']=reduce(lambda a,b: a+b.get_positivetotal(), eshs, 0)
        context['total'] = total
        context['clinic']=clinic
        context['events']=eshs
        context['counts']= counts
        
        negativeevents=[]
        for esh in eshs:
          pay=Payment.objects.filter(header=esh) 
          for payment in pay:
              if payment.amount<0:
                  negativeevents.append(esh)
                  break
        context['negativeevents'] = negativeevents   
        negativetotal={}  
        negativetotal['cash'] = reduce(lambda a,b: a+b.get_negcash(),negativeevents,0)  
        negativetotal['cc'] = reduce(lambda a,b: a+b.get_negcc(),negativeevents,0)  
        negativetotal['negativetotal'] = negativetotal['cash'] + negativetotal['cc']
        context['negativetotal'] = negativetotal
        context['nettotal'] = total['positivetotal']+negativetotal['negativetotal']
        template = "pdf/payments.htm"
    else:
        raise Http404()
    
    tpl = loader.get_template(template)
    pdf_source = tpl.render(Context(context))
    response =  HttpResponse(pdf_source)
    response.pdf=True
    return response

#@make_pdf

def print_receipt(request):
    '''
        Here we return the payment receipt of a particular user.
    '''
    headerID = request.REQUEST.get('headerID',None)
    date     = request.REQUEST.get('date',None)
    
    esh = EventSetHeader.objects.get(id=headerID)
    
    payments = Payment.objects.filter(header = esh)
    
    patient_name = get_patient_full_name(esh)#esh.patient.lName + " " +  esh.patient.fName
    
    patient = {'name': patient_name, 'esh': esh, 'date': date, 'payments':payments}
    
    
    template = 'pdf/payment_receipt.htm'
    
        
    #tpl = loader.get_template(template)
    #pdf_resource = tpl.render(Context(patient))
    #response = HttpResponse(pdf_resource)
    
    #response.pdf = True
    
    return direct_to_template(request,'pdf/payment_receipt.htm', patient)
    
    
    #return HttpResponse('OK',mimetype='application/pdf')
    
    
