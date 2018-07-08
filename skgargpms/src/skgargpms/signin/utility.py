from signin.models import *
import datetime


def gen_report(esh):
    '''
        Returns set of arguments required to display report page properly.
        
        report = {"signinTregistration":timedif, "registrationTtriage":timedif,"triageTprovider":timedif, "providerTcheckout":timedif,"appointment":timedif}
        
    '''
    pels = PatientEventLog.objects.filter(header = esh)
    
    events = {}
    pel_temp = {}
    
    for pel in pels:
        pel_temp[pel.event.name] = pel.dateTime
    
    if 'signin' in pel_temp and 'registration' in pel_temp:
            events['signinTregistration'] = ":".join(str(pel_temp['registration'] - pel_temp['signin']).split(":")[:2])
        
    if 'registration' in pel_temp and 'triage' in pel_temp:
        events['registrationTtriage'] = ":".join(str(pel_temp['triage'] - pel_temp['registration']).split(":")[:2])
        
    if 'triage' in pel_temp and 'provider' in pel_temp:
        events['triageTprovider'] = ":".join(str(pel_temp['provider'] - pel_temp['triage']).split(":")[:2])
      
    if 'provider' in pel_temp and 'checkout' in pel_temp:
        events['providerTcheckout'] = ":".join(str(pel_temp['checkout'] - pel_temp['provider']).split(":")[:2])
        
    if 'appointment' in pel_temp:
        events['appointment'] = ":".join(str(datetime.datetime.now() - pel_temp['appointment'] ).split(":")[:2])

    return events





def get_clinic_event_map(clinicID):
    '''
        return array of (event,position) tupples of a given Clinic or it will return Boolean False. 
    '''
    
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



def get_patient_full_name(header):
    '''
        Accept a header object and construct the patient name as
        
        if dob is required , then name is "LastName, FirstName , DOB"
        if dob is not required, then return "lastName,FirstName".
    '''
    patient_name = "%s, %s" % (header.patient.lName,header.patient.fName)
    
    if header.clinic.location.dob_required:
        if header.patient.dob != None:
            patient_name += ", %s" % (header.patient.dob,)
    
    return patient_name
    
        
        
def check_pending_interrupts(headerID):
    '''
       Check pending Interrupts of Patient under particular clinic.\
       
       It return an Array of tupples with pending interrupt name and its id, or null list.
    '''
    flag = 0
    int_ids = []
    pending_intr = []
    pils = PatientInterruptLog.objects.filter(header=headerID)
    
    #Get all interrupt id's.
    for i in pils:
        int_ids.append(i.interrupt.id)
    
    #removing duplicate id's
    int_ids = list(set(int_ids))
    
    #Check for the pending Interrupts and store it in list.
    for id in int_ids:
        for intr in pils.filter(interrupt__id=id):
            if intr.status == 'started':
                flag += 1
            else:
                flag -= 1          
        if flag > 0:
            pending_intr.append((intr.id,intr.interrupt.name))
        flag = 0
    
    return pending_intr
   
    
def format_time(timedelta):
    
    '''
        receive a time in timedelta format ,
        input <=24hour time delta represendation.
        output - '4h:5m:55s'
    '''
    #convert dateobject in to list of time list of type integer.
    time_list = [int(a) for a in str(timedelta).split('.')[0].split(':')]
    time_format = ['h','m','s']
    
    #Function to map the num to time string.
    def time_str(time,notation) :
        if time == 0:
            return ''
        else:
            return str(time) + notation
    #Use map function to compain the result and return string time represendation back.
    
    return ':'.join([ a for a in map(time_str,time_list,time_format) if a ])
    
    
    
    
    
    