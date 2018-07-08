###########################################################
#             General notification script(test)           #
#             Author : Robert -Spark                      #
# conventions used '###' for testing intermediate values  #
# '#----#' for comments etc..                             #
###########################################################
import datetime
from signin.models import *
from signin.smtp import *
import time
#creating two blank lists ,which will be used later in the module..
total_patient_ids=[]
checkd_out_ids=[]
active_patient_ids=[]
last_event=None
count=None
d=datetime.datetime.now()
def messager(message,from_address='vishnu@ditchyourip.com',rcpt_to='vishnu@sparksupport.com',user=''):
        mailer=Smtp();
        mailer.rcpt_to(rcpt_to)
        mailer.from_addr(from_address)
        mailer.message(message)
        mailer.subject('Alert')
        print vars()
        #mailer.send()
        time.sleep(3)
    
def msg_replace(valuedic):
    x=open('templates/email-message.txt','r')
    msg_txt=x.read()
    for i,j in valuedic.iteritems():
        msg_txt=msg_txt.replace(str(i),str(j))
    return msg_txt

                
def get_time_difer(qry_grp=None,activeid=None):
    """function for getting the time difference between the last event time and current time
       for each active id's in the list
       arguments are the query group consisting of all the active events and there id's"""
    
    try:
       #--getting the length of the active_patient_ids list---  
       count=len(active_patient_ids)
       ###print count
       
       ###print "current time%s" % datetime.datetime.now()
       #---looping through each active patient id's to find the last event,time difference etc...---#
       for i in range(count):
           print activeid[i]
           print i
           
           qry_grp1=qry_grp.filter(header__patient__id__exact=activeid[i])
           print "....."
	   ###print qry_grp1
           for j in qry_grp1:
              last_event=j.event.name
           print last_event
           #---finding difference in time b/w last event and current time---#
           
	   qry_grp2=qry_grp1.filter(event__name=last_event)
           #print qry_grp2
	   for j in qry_grp2: 
                time_last_event=j.dateTime
		if j.dateTime <= datetime.datetime(d.year,d.month,d.day,d.hour,d.minute,d.second)-datetime.timedelta(minutes=10):
		  print j.header.dateTime
                  print qry_grp2
		  for k in qry_grp2:
                     valuedict=dict()
	             valuedict['{patient-id}']=k.header.patient.id
                     valuedict['{fname}']=k.header.patient.fName
                     valuedict['{lname}']=k.header.patient.lName
                     valuedict['{time}']=k.dateTime
                     valuedict['{event}']=k.event.name
                     valuedict['{location}']=k.header.clinic.location.name
                     valuedict['{clinic-id}']=k.header.clinic.name
             
                     ###print "yes"
                     ###print valuedict
                     ###return valuedict
                     # print "Passing the details to message function ...."
                     #message=msg_replace(valuedict)
                     #print message
                     #messager(message)
             
             
                else:
                     print "no - %s " %  time_last_event
                     ###return qry_grp2
                                   
                  
               
              
       #---return last_event---#
                      
           
    except TypeError:
        return None
        
    
#---query set grouping all events from the PatientEventLog---#
query_grp1=PatientEventLog.objects.all
#-----finding all active paients in the queue from the last n hours ------#
for i in query_grp1():
	if i.dateTime >= datetime.datetime(d.year,d.month,d.day,d.hour,d.minute,d.second)-datetime.timedelta(hours=4):
		total_patient_ids.append(i.header.patient.id)
		total_patient_ids=list(set(total_patient_ids))
#---getting the id of all checked out patients to a list called checkd_out_ids---#
for i in PatientEventLog.objects.filter(header__patient__id__in=total_patient_ids):
    if i.event.name=="checkout":
           checkd_out_ids.append(i.header.patient.id)
           #---removing duplicate entries from the list---#
           checkd_out_ids=list(set(checkd_out_ids))
	   #print checkd_out_ids
#---query set for grouping all other active patient ids to a list called active_patient_ids---#
query_grp2=PatientEventLog.objects.filter(header__patient__id__in=total_patient_ids).exclude(header__patient__id__in=checkd_out_ids)
for i in query_grp2: 
    #print i
    active_patient_ids.append(i.header.patient.id)
    #---removing all duplicate entries from the list---#
    active_patient_ids=list(set(active_patient_ids))
