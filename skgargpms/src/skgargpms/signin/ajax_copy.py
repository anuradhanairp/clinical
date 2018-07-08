# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings 
from skgargpms.signin.models import *
from django.db.models import Sum
import datetime,time
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.views.generic.simple import direct_to_template

from django.utils import simplejson
from django.core import serializers
from signin.utility import get_patient_full_name
from signin.views import updateDict, get_clinic_event_map, get_event_time , get_local_time, get_request_period

#import get report_function for the realtime update when signin occure.


#Get celeryd messaging support for signin process.
from signin.tasks import  post_signin_process,trigger_event

'''
def get_request_period(request):
    if request.REQUEST.has_key("date"):
        dt = datetime.datetime.strptime(request.REQUEST['date'],"%Y-%m-%d")
    else:
        dt = datetime.datetime.now()
        
    delta = datetime.timedelta(days=1)
    dtStart = datetime.datetime(dt.year, dt.month, dt.day, 0,0,0)
    dtEnd = dtStart + delta
    return dtStart, dtEnd
'''   

def dataSignUp(request):
    
    #return HttpResponse("<status>saved</status>", mimetype="application/xml")
    
    '''
       
        Processing new patient signin here.
        
        return JSON frommat:- 
        
        Possitive result:- 
         {'type':'signin','headerID':header,'from':user,'response':'OK', 'patient':{'name':name ,'event_name':time ...}}
        
        Negative result:-
         {'type':'signin','response':'failed','from':user}
         
         
         #Also Modified to get the genaralizing property.
    '''
    
    post_signin_process.delay(request)
    
    
    return HttpResponse("OK", mimetype="application/text")


def add_payment(request):
    
    header = get_object_or_404(EventSetHeader,id=request.REQUEST.get('header',None))
    amount = request.REQUEST.get("amount","0")
    if not int(amount):
        raise Exception('q');
      
    user = request.REQUEST.get('user',"")
    payment_type = request.REQUEST.get("type","cash")
    cc_info = request.REQUEST.get("cc_info","")
    
    int_id = request.REQUEST.get('interrupt',None)
    
    if int_id:
        interrupt_type = get_object_or_404(Interrupt,id = int_id )
    else:
        interrupt_type = None
    
    
      
    Payment(header=header,type=payment_type, info = cc_info, amount = amount, interrupttype = interrupt_type).save()
    
    event,_ = Event.objects.get_or_create(name="payment")
    #interrupttype=interrupt_type
    PatientEventLog(header=header, event=event, user = user).save()
       
    #msg = {'header':header.id,'amount':amount,'user':request.REQUEST.get('interrupt',None)}
    
    #msg = {'header':header.id}   
    #except Exception, e:
    #    return HttpResponse("0", mimetype="text/plain")
    
   # msg = simplejson.dumps(msg)
   # return HttpResponse(msg,mimetype='application/json')
    return HttpResponse("1", mimetype="text/plain")

def add_provider(request):
    '''
    Add provider to a Patient.
    '''
    
    try:
        header = get_object_or_404(EventSetHeader, id = request.REQUEST.get('header',None))
        provider = get_object_or_404(Provider, id = request.REQUEST.get('provider_id',None))
        header.provider = provider
        header.save()
    except Exception, e:
        return HttpResponse("0",mimetype="text/plain")
    return HttpResponse("1",mimetype="text/plain")

    

def payment_page(request):
    header = get_object_or_404(EventSetHeader,id=request.REQUEST.get("header",None))
    patintr=Payment.objects.filter(header=header)
    result=patintr.values_list('interrupttype','amount','type')
    listofinterrupts=[]
    amount=[]
    type=[]
    c=0
    for i in result:
      c=c+1  
      listofinterrupts.append(i[0]) 
      amount.append(i[1])
      type.append(i[2]) 
      
    
    if not request.REQUEST.has_key("clinicID"):
        raise Http404
    clinic_id = request.REQUEST['clinicID']

    clinic = get_object_or_404(Clinic, id=clinic_id)

    dtStart,dtEnd = get_request_period(request,clinic)
    
    eshs = EventSetHeader.objects.filter(clinic = clinic).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart).order_by("dateTime")
    
    total = {}
    total['cash']=reduce(lambda a,b: a+b.get_cash(), eshs, 0.0)
    total['cc']=reduce(lambda a,b: a+b.get_cc(), eshs, 0.0)
    total['total'] = total['cash'] + total['cc']
    ansDict={}
    ansDict['total'] = total
    ansDict['clinic']=clinic
    ansDict['events']=eshs
    
    ansDict['result']=result
    ansDict['number']=c
    
    return direct_to_template(request,'tools/payment-page.htm',ansDict)
    
def paymenthistory(request):
    header = get_object_or_404(EventSetHeader,id=request.REQUEST.get("header",None))
    payments = {
        }
    for s in ('cc','cash'):
        payments.setdefault(s,{})['list'] = Payment.objects.filter(header=header,type=s).order_by('dateTime')
        payments[s]['total'] = reduce(lambda a,b:a+float(b.amount), payments[s]['list'], 0.0)
    return direct_to_template(request,"tools/paymenthistory.htm",{"payments":payments,"header":header,'total':payments['cc']['total'] + payments['cash']['total']})


def sendEvent(request):
    '''
    This function will update the PatientEventLog to indicate patient where move to another event under a clinic. 
    '''
    ansDict = updateDict(request)
    event = request.REQUEST["event"]
    headerID = request.REQUEST["headerID"]
    
    header = EventSetHeader.objects.get(id=headerID)
    event = Event.objects.filter(name=event)[0]
    
    pelCount = PatientEventLog.objects.filter(header = header, event = event).count()
    if pelCount == 0:
        PatientEventLog(header = header, event = event).save()
    
    return HttpResponse("<status>saved</status>", mimetype="application/xml")


def getFrontDeskClinicListCount(request):
    '''
    Return Total count of Patients under a clinicID,it consider only Current day's list only. 
    '''
    
    count = 0 
    clinicID = request.REQUEST["clinicID"]
    dtStart, dtEnd = get_request_period(request)
    
    eshs = EventSetHeader.objects.filter(clinic = Clinic.objects.get(id=clinicID)).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
    
    for esh in eshs:
        count += PatientEventLog.objects.filter(header=esh).count()
    
    outputStr = "<count>%s</count>" % (str(count))
    return HttpResponse(outputStr, mimetype="application/xml") 


def getFrontDeskClinicList(request):
    
    '''
    Returns List of current days "headerID" and total rows in the PatientEventLog( which represents where the 
    the patient right now under that clinic.)  of every patients under a clincID.
    
    '''
    clinicID = request.REQUEST["clinicID"]

    dtStart, dtEnd = get_request_period(request)

    eshs = EventSetHeader.objects.filter(clinic = Clinic.objects.get(id=clinicID)).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
    outputList = list()
    outputList.append("<eventList>")
    for esh in eshs:
        count = PatientEventLog.objects.filter(header=esh).count()
        outputList.append("<li><header>%s</header><count>%s</count></li>" % (esh.id,count))   
    outputList.append("</eventList>")
    return HttpResponse("".join(outputList), mimetype="application/xml")


def loadReportsListItem(request):
    '''
     It will return the details of one patient and their waiting time before every events. HeaderID where used to locate the patient.
    '''
    eshID = request.REQUEST["header"]
    esh = EventSetHeader.objects.get(id = eshID)
    pels = PatientEventLog.objects.filter(header = esh)

    rCompile = dict()
    for pel in pels:
            rCompile[pel.event.name] = pel.dateTime
    rSort = dict()

    if "signin" in rCompile and "registration" in rCompile:
        rSort["signinTregistration"] = rCompile["registration"] - rCompile["signin"]
        
    if "registration" in rCompile and "triage" in rCompile:
        rSort["registrationTtriage"] = rCompile["triage"] - rCompile["registration"]
        
    if "triage" in rCompile and "provider" in rCompile:
        rSort["triageTprovider"] = rCompile["provider"] - rCompile["triage"]
        
    if "provider" in rCompile and "checkout" in rCompile:
        rSort["providerTcheckout"] = rCompile["checkout"] - rCompile["provider"]
        
    if "appointment" in rCompile:
        rSort["appointment"] = rCompile["appointment"] - datetime.datetime.now() 

    outputList = list()
    outputList.append("<reports>")
    outputList.append("<fname>%s</fname><lname>%s</lname><dob>%s</dob>" % (esh.patient.fName,esh.patient.lName,esh.patient.dob))
    for item in rSort: 
            outputList.append("<report>")
            outputList.append("<name>%s</name><time>%s min</time>" % (item, int(rSort[item].seconds/60)))
            outputList.append("</report>")
    outputList.append("</reports>")
    return HttpResponse("".join(outputList), mimetype="application/xml")


def loadFrontDeskListItem(request):
    '''
    This will return the details of the patients and event status.
    
    '''
    eshID = request.REQUEST["header"]
    esh = EventSetHeader.objects.get(id = eshID)
    pels = PatientEventLog.objects.filter(header = esh)
    outputList = list()
    outputList.append("<events>")
    outputList.append("<fname>%s</fname><lname>%s</lname><dob>%s</dob>" % (esh.patient.fName,esh.patient.lName,esh.patient.dob))
    payment_amount = reduce(lambda a,b:a + b.amount, Payment.objects.filter(header=esh), 0)
    # raise Exception(payment_amount)
    outputList.append("<payment>%s</payment>" % str(payment_amount))
    # print outputList
    for pel in pels:
            outputList.append("<event>")
            outputList.append("<name>%s</name><time>%s:%s</time>" % (pel.event.name,pel.dateTime.hour,pel.dateTime.minute))
            outputList.append("</event>")
    outputList.append("</events>")
    return HttpResponse("".join(outputList), mimetype="application/xml")


    
def get_json_report(request):
    '''
    Implemented to send the report page information via json form.
    
    Json data fromat:- 
    
    Default user:- msg =  {'user':user,'clinicID':clinicID,'patients':[{'headerID':headerID,'patient':{'name':name,'eventTevent':time,...}},... ]}
    
    '''
    user = request.POST['user']
    clinicID = request.POST['clinicID']
    
    clinic = Clinic.objects.get(id = clinicID)
    
    msg = {'user':user, 'clinicID':clinicID}
    
    #msg = simplejson.dumps(msg)
    
    if user == 'default':
        
        
        #Featch the initial Report from the server itself rather than go for axaj method.
        dtStart, dtEnd = get_request_period(request,clinic)
        eshs = EventSetHeader.objects.filter(clinic = clinicID).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
        
        patients = []
        patient = {}
        events = {}
        pel_temp = {}
        patient_full = {} 
        
        for esh in eshs:
           
            pels = PatientEventLog.objects.filter(header = esh)
            patient_name = get_patient_full_name(esh) #esh.patient.lName + "," +  esh.patient.fName + "," +  str(esh.patient.dob)
            
            
            for pel in pels:
                pel_temp[pel.event.name] = pel.dateTime
            
            #Get Event map function from the views module.
            
            event_map = get_clinic_event_map(clinicID)
            
            #Get the time based on the event order from the clinic design
            for i in range(len(event_map)):
                '''
                    Get time interval between events.
                '''
                if (i+1) < len(event_map):
                    if event_map[i][1] in pel_temp and event_map[i+1][1] in pel_temp:
                        events[event_map[i][1]+'T'+event_map[i+1][1]] = ":".join(str(pel_temp[event_map[i+1][1]] - pel_temp[event_map[i][1]]).split(":")[:2])
                else:
                    if event_map[i][1] in pel_temp:
                        events[event_map[i][1]] = ":".join(str(datetime.datetime.now() - pel_temp[event_map[i][1]] ).split(":")[:2])

                    
            
            '''
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
            '''
            
            #some adjustment in the json datatype to make it similar structure of comet based integrations. 
            patient = {"name":patient_name}
            patient.update(events)
            
            patient_full = {"headerID":esh.id,"patient":patient}
            
            if not 'delete' in pel_temp:
                '''
                   If "delete" entry were present, we just discard that user from frontdesk.
                '''
                patients.append(patient_full)
                           
            #Clear old values.
            pel_temp = {}
            events = {}
        
        #patients.reverse(), Dont need to reverse here, because we adding rows to the table via jquery.
        
        #name = {"name":patient_name}
        #patient = {"name":patient_name,"headerID":esh.id,"events":events}
        #patients = []
        #patients = [{'headerID': 354, 'name': 'suresh', 'events': {'signinTregistration': '20:33'}}]
        
        msg['patients'] = patients

    else:
        '''
        Other users; Here we have to return the events of a particular User.
        JSON message format:-
        
        msg = {'user':user,'clinicID':clinicID,'patients':[{'headerID':headerID,'patient':{'name':name,'event':time,...}}, ...]}
        '''
        
        #user = request.POST['user']
        #Featch the initial Report from the server itself rather than go for axaj method.
        dtStart, dtEnd = get_request_period(request,clinic)
        eshs = EventSetHeader.objects.filter(clinic = clinicID).exclude(dateTime__gte=dtEnd).filter(dateTime__gte=dtStart)
        
        local_timezone = eshs[0].clinic.location.timezone
        
        
        #patients = [{'headerId': 433, 'patient': {u'name':u'test',u'signin': datetime.datetime(2011, 3, 23, 13, 40, 13, 407482), 'name': 'adf', u'registration': datetime.datetime(2011, 3, 23, 14, 2, 52, 31204)}}]
        
        for esh in eshs:
            patient_full = {'headerID':esh.id}

            pels = PatientEventLog.objects.filter( header = esh , user = user )
            
            #If empty.
            if not pels: 
                continue
            patient_name = get_patient_full_name(esh) #esh.patient.lName + "," +  esh.patient.fName + "," +  str(esh.patient.dob)
            
            patient = {'name': patient_name}

            for pel in pels:
                patient[pel.event.name] = get_local_time(local_timezone,pel.dateTime) #str(pel.dateTime.hour) + ":" + str(pel.dateTime.minute)
                
            patient_full['patient'] = patient
            #List of Patients.
            patients.append(patient_full)
            
            #Clear Previous user datas.
            patient = {}
            patient_full = {}
        
            
            
        msg['patients'] = patients
        
        #endof else block
    
    msg = simplejson.dumps(msg)
    return HttpResponse(msg,mimetype="application/json")


def interrupt_processing(request):
    
     header = request.POST['header']
     int_id = request.POST['int_id']
     status = request.POST['status']
     username = request.POST['username']
     #username = request.REQUEST.get("username",None)
     
     #Update the PatientInterrupt table with this interrupt and time of occerence.
     
     
     header_obj = EventSetHeader.objects.get(id=header)
     
     local_timezone = header_obj.clinic.location.timezone
     
     interrupt = Interrupt.objects.get(id=int_id)
     
    # pil = PatientInterruptLog(header=header_obj,interrupt=interrupt ,user = username,status = status)
     if username == 'null' :
         pil = PatientInterruptLog(header=header_obj,interrupt=interrupt ,status = status)
         
     else:
         pil = PatientInterruptLog(header = header_obj,interrupt = interrupt,user = username,status = status) 
         
           
     pil.save()
     
     #get local time.
     dateTime = get_local_time(local_timezone,pil.dateTime)
     
     msg = {'header':header,'int_id':int_id,'status':status,'user':username,'dateTime':dateTime}
     
     #Convert python object to json object before send back.
     msg = simplejson.dumps(msg)
     return HttpResponse(msg,mimetype="application/json")
 
 
def patient_interrupts(request):
    
     patientheader=request.REQUEST.get("header")
     interrupts = PatientInterruptLog.objects.filter(header=patientheader,status="started")
     interruptslist=interrupts.values_list('header','interrupt')
     result=[]
     for i in interruptslist:
         p=Payment.objects.filter(header=i[0],interrupttype=i[1])
         if not p:
             result.append(i[1])
     interruptname=[]
     interruptid=[]
     for i in result:
         c=Interrupt.objects.get(id=i)
         interruptname.append(c.name)
         interruptid.append(i)
        
     if interruptname:    
      msg={'paymentprocedureinterrupts':interruptname,'interruptid':interruptid}  
     else:
      msg= {'paymentprocedureinterrupts':'','interruptid':''}    
     msg=simplejson.dumps(msg)                
     #result={'interrupts':'ok'}
     #json = simplejson.dumps(result)

     #msg={'header':patientheader}
     #msg={'header':patientheader}
    # msg=simplejson.dumps(msg)
     return HttpResponse(msg,mimetype="application/json")
     #data=serializers.serialize("json", interrupts.object_list)
     #return HttpResponse(jsonify({'interrupts':interrupts}))
#def queryresult(patientheader):
    #interrupts=PatientInterruptLog.objects.filter(header=patientheader)
    #sg=simplejson.dumps(interrupts)
    #return msg
def save_appointment(request):
    user=request.REQUEST.get("user")
   # year = request.REQUEST.get("year")
    #month = request.REQUEST.get("month")
    #date = request.REQUEST.get("date")
    date = request.REQUEST.get("newdate")
    old_header = get_object_or_404(EventSetHeader,id=request.REQUEST.get('header',None))
    newheader = EventSetHeader(patient=old_header.patient,clinic=old_header.clinic,dateTime=datetime.datetime.strptime(date,"%Y-%m-%d"))
    newheader.save()
    new_header_id = get_object_or_404(EventSetHeader, id =newheader.id)
    event,_=Event.objects.get_or_create(name="appointment")
    new_patient_event_log = PatientEventLog(event=event,header=new_header_id,user=user)
    new_patient_event_log.save()
    return HttpResponse("1", mimetype="text/plain")


def getFullEventAttributes(request):
    '''
        Returnt the full event-to-attribute map of a clinic in json format.
        
        json format:- 
        
        {'clinicID':id, 'event_name':[{'mapID':id,'attr_name':name, 'required':True, 'hidden':False, 'error_msg': msg},{},etc..], ... }
        
    '''
    
    
    clinicID = request.GET['clinicID'];
    
    clinic_event_attr_map = {'clinicID':clinicID}
   
    
    #All Event-to-attribute mapping records from the DB.
    event_attrs = EventAttributeMap.objects.filter(clinic = clinicID)
    
    #Events of this clinic.
    event_map = get_clinic_event_map(clinicID)
    
    for ev_name in event_map:
        
        attrs = event_attrs.filter(event__name=ev_name[1])
        
        attr_list = []            
        for attr in attrs:
            attr_list.append({'mapID': attr.id, 'attr_name': attr.attribute.name, 'required': attr.required, 'hidden': attr.hidden, 'error_msg': attr.attribute.error_message })
        
        clinic_event_attr_map.update({ev_name[1]: attr_list})
            
    
    
    json_msg = simplejson.dumps(clinic_event_attr_map)
    
    return HttpResponse(json_msg,mimetype='application/json')
            
        
def save_attr_form(request):
    '''
        Save the attributes values entered by the frontdesk user, under corresponding event-to-attribute entry.
        
        TODO:-
            We can extend this get the stomp client updation of these form updates back to other front-desks also.
     
    '''
    
    
    get_data = request.GET
    
    headerID = get_data.get('headerID',None)
    #Header object.
    
    header = get_object_or_404(EventSetHeader,id = headerID )
    
    #initialize the response
    msg = {}
    
    #Check whether request were came from jqmtab,
    if get_data.get('jqmtab',None) == 'YES':
        #Due to the special case we triggering the event to backend stomp channel here.
        event_name = get_data.get('event_name',None)
        username = get_data.get('username','suresh')
        password = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        
        #prepare credantails 
        credantials = {'username': username, 'password': password}
        
        #Trigger the Event via celery task,
        trigger_event.delay(event_name,headerID,credantials)
        
        msg.update({'clinic_url':'/jqmtab/clinic/?clinicID=' + str(header.clinic.id) })
    
    
    for attr_name in get_data.iterkeys():

        if attr_name.find('attr_name') == 0:
            #Get the Data from the form field.
            attr_value = get_data[attr_name]
            
            # Attribute name is of the form "attr_name34", where 34 is the id of eventAttribute table.
            attr_id = int(attr_name.split('attr_name')[1])
            
            #Get the EventAttribute Map object.
            attr_map = EventAttributeMap.objects.get(id = attr_id)
            
            #Save value of that object. Use 'filter' instead of 'get', the later one throw an exception in the no record case.
            attr_log = EventSetAttributeLog.objects.filter(header = header, attr_map = attr_map)
            
            if attr_log:
                
                attr_log = attr_log[0]
                attr_log.value = attr_value
                attr_log.save()
                
            else:
                EventSetAttributeLog(header = header, attr_map = attr_map, value = attr_value).save()
    
    msg.update({'status': 'OK'})
    msg = simplejson.dumps(msg)
    return HttpResponse(msg,mimetype='application/json')
    
