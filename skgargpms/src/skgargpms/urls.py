from django.conf.urls.defaults import *
from django.conf import settings 
import os 
from django.views.generic.simple import direct_to_template, redirect_to
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


#Urls for Web version of the work flow application. 
urlpatterns = patterns('',

                       (r'^$', 'signin.views.frontdesk'),
                       (r'^signin/$', 'signin.views.signin'),
                       (r'^reports/$', 'signin.views.reports'),
                       (r'^frontdesk/$', 'signin.views.frontdesk'),
                       (r'^payment/$', 'signin.views.payment'),

                       
                       (r'^ajax/payment/$', 'signin.ajax.payment_page'),
                       (r'^paymenthistory/$', 'signin.ajax.paymenthistory'),
                       (r'^installBase/$', 'signin.views.installBase'),
                       (r'^dataSignUp/$', 'signin.ajax.dataSignUp'),
                       (r'^addPayment/$', 'signin.ajax.add_payment'),
                       (r'^addProvider/$','signin.ajax.add_provider'),
                       (r'^saveappointment/$','signin.ajax.save_appointment'),
                       (r'^patientinterrupts/$','signin.ajax.patient_interrupts'),
                       (r'^getJsonReport/$','signin.ajax.get_json_report'),
                       (r'^handleInterrupt/$','signin.ajax.interrupt_processing'),
                       
                       
                       (r'^pdf/$', 'signin.views.export_pdf'),
                       (r'^printReceipt/$', 'signin.views.print_receipt'),
                       
                       (r'^getFrontDeskClinicListCount/$', 'signin.ajax.getFrontDeskClinicListCount'),
                       (r'^getFrontDeskClinicList/$', 'signin.ajax.getFrontDeskClinicList'),
                       (r'^loadFrontDeskListItem/$', 'signin.ajax.loadFrontDeskListItem'),
                       (r'^sendEvent/$', 'signin.ajax.sendEvent'),
                       (r'^loadReportsListItem/$', 'signin.ajax.loadReportsListItem'),
                       
                       (r'^testpage/$','signin.views.testpage'),
                       (r'^stomptester/$','signin.views.stomptester'),
                       #(r'^listMessages/$', 'mailFrontEnd.views.listMessageNodes'),


                       #(r'^create_account/$', 'pstmail.views.create_account'),
                       #(r'^accounts/login/$', 'pstmail.views.login_required'),

                       #(r'^$','pstmail.views.startPage'),
                       (r'^'+settings.STATIC_URL[1:]+'(?P<path>.*)$', 'django.views.static.serve'),
			
			           #{'document_root': settings.STATIC_ROOT,"show_indexes": True}),


                        # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
                        # to INSTALLED_APPS to enable admin documentation:
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       (r'^accounts/', include('django.contrib.auth.urls')),
                       # (r'^account/', 'djainclude(admin.site.urls)),
                       
                       #General Clinic Design URL's
                       (r'^admin/design_clinics/$','signin.admin_views.clinic_design'),
                       
                       #Event mapping definition for each clinics.
                       (r'^admin/design_clinics/(?P<clinic_id>\d{1,3})/$', 'signin.admin_views.clinic_admin'),
                       (r'^admin/design_clinics/(?P<clinic_id>\d{1,3})/update/$', 'signin.admin_views.clinic_admin'),
                       
                       #Event based form, or appeinding metadatas with each events.
                       (r'admin/assign_attributes/(?P<clinic_id>\d{1,3})/$', 'signin.admin_views.attribute_admin'),
                       (r'admin/assign_attributes/(?P<clinic_id>\d{1,3})/update/$', 'signin.admin_views.attribute_admin'),
                       
                       
                       #Mail Alert settings URL's
                       #(r'^admin/alert_home/$','signin.admin_views.alert_home'),
                       #(r'^admin/alert_home/(?P<conf_id>\d{1,4})/$',redirect_to,{'url':'/admin/signin/alertconfiguration/'}),
                       (r'^admin/signin/alertconfiguration/(?P<conf_id>\d{1,4})/$','signin.admin_views.alert_form_edit'),
                       (r'^admin/signin/alertconfiguration/add/$','signin.admin_views.alert_form_add'),
                       (r'^admin/auth/user/add/$','signin.admin_views.add_user'),
                       (r'^save_new_user/$','signin.admin_views.ajax_savenewuser'), 
                       (r'^fetchClinics/$','signin.admin_views.ajax_get_clinics'),
                       (r'^fetchEventMap/$','signin.admin_views.ajax_get_eventmap'),
                       (r'^alertConfSave/$','signin.admin_views.alert_form_save'),
                       (r'^fetchAttributes/$','signin.admin_views.ajax_get_attrs'),
                       (r'^fetchEventAttributeMap/$','signin.admin_views.ajax_get_event_attr_list'),
                       (r'^GetFullEventAttrMap/$','signin.ajax.getFullEventAttributes'),
                       (r'^SubmitAttrForm/$','signin.ajax.save_attr_form'),
                       
                       (r'^admin/notifier_settings/$','signin.admin_views.Notifier_Settings'),
                      
                       #Django admin  URL's.
                       (r'^admin/', include(admin.site.urls)),
      		       
			           #grappelli django new admin
                       
                       
                       
                       ######################################
                       #                                    #
                       # URL's for the Sproutcore Frontend. #
                       #                                    #
                       ######################################
                       
                       (r'^login/$','signin.sproutcore_views.login'),
                                              
                       
)

#Spart mobile version.
jquerymobile_urls = patterns('signin.jqmobile_views',
                             (r'^jqmobile/$','jqmobile_home'),
                             (r'^jqmobile/clinic/(?P<clinic_id>\d{1,3})/$','jqmobile_station_summary'),
                             #(r'^jqmobile/shadow/(?P<patient_header>\d{1,3})/$','jqmobile_shadowwindow'),
                             
                             #main patient summary '/jqmobile/clinic/1/patients/'
                             (r'^jqmobile/clinic/(?P<clinic_id>\d{1,3})/patients/$','jqmobile_patient_summary'),
                             
                             # Event specific patient summary.'/jqmobile/clinic/1/event/2/patients/'
                             (r'^jqmobile/clinic/(?P<clinic_id>\d{1,3})/event/(?P<event_id>\d{1,3})/patients/$','jqmobile_event_patient_summary'),
                             
                             # Event specific patient summary.'/jqmobile/patient/4/'
                             (r'^jqmobile/patient/(?P<header_id>\d{1,5})/$','jqmobile_patient_stations'),
                             
                             # List Event informations of a patient. '/jqmobile/patient/4/event_name/'
                             (r'^jqmobile/patient/(?P<header_id>\d{1,5})/event/(?P<event_order>\d{1,2})/$','jqmobile_patient_station'),
                             
                             
                             
                             ##### URL's for special Ajax calls #####
                             
                             (r'^jqmobile/submit_attribute/$','jqmobile_submit_event_attr'),

                             (r'^jqmobile/procedures/(?P<header_id>\d{1,5})/$','jqmobile_procedures'),
                             
                             (r'^jqmobile/event_finished/$','jqmobile_event_finished'),
                             
                             (r'^jqmobile/jqmobile_handle_procedure/$','jqmobile_process_interrupt'),
                             
                             
                    )


#URL for the Tablet machines.
jquerymobile_urls += patterns('signin.jqmtab_views',
                             (r'^jqmtab/$','jqmtab_home'),
                             #(r'^jqmtab/clinic/(?P<clinic_id>\d{1,3})/$','jqmtab_frontdesk'),
                             
                             (r'^jqmtab/clinic/$','jqmtab_frontdesk'),
                             #urls for shadowwindow
                             
                             (r'^jqmtab/patient/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow'),
                             
                             (r'jqmtab/shadow_payment/(?P<patient_header>\d{1,6})/$', 'jqmtab_shadowwindow_payment'),
                              
                             (r'^jqmtab/shadow_provider/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow_provider'),
                             
                             (r'^jqmtab/shadow_edit/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow_edit'),
                             
                             (r'^jqmtab/shadow_procedures/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow_procedures'),
                             
                             (r'^jqmtab/shadow_remove/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow_remove'),
                             
                             (r'^jqmtab/shadow_payment_procedure/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow_payment_procedure'),
                             
                             (r'^jqmtab/shadow_appointment/(?P<patient_header>\d{1,6})/$','jqmtab_shadowwindow_appintment'),
                             
                             (r'^jqmtab/reports/$', 'jqmtab_reports'),
                             
                             (r'^jqmtab/payment/$', 'jqmtab_payment'),
                             
                             (r'^jqmtab/signin/$', 'jqmtab_signin'),
                             
                             (r'^jqmtab/changedate/$', 'jqmtab_changedate'),
                             
                                  
                             ### Specific Backend Ajax Calls ###
                             
                             (r'^jqmtab/move_patient/$','jqmtab_move_patient'),
                             (r'^jqmtab/remove_patient/$','jqmtab_remove_patient'),
                             
                             #(r'^jqmtab/pdf/$', 'jqmtab_export_pdf'),
                                                          
                             )


#Specially for jquery logout.
jquerymobile_urls += patterns('',
                             
                             url(r'^jqmtab/logout/$', "django.contrib.auth.views.logout",{'template_name':'jqmtab/logout.html'},name = "jqmtab_logout_url", prefix = ""),
                             url(r'^jqmobile/logout/$', "django.contrib.auth.views.logout",{'template_name':'jqmobile/logout.html'},name = "jqmobile_logout_url", prefix = ""),
                             
                             )


#Full Url list.
urlpatterns += jquerymobile_urls

