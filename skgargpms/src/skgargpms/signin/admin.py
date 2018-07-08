from django.contrib import admin
from skgargpms.signin.models import *

admin.site.register(Location)
admin.site.register(Event)


class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'start_time', 'end_time')
admin.site.register(Clinic, ClinicAdmin)

admin.site.register(Provider)

admin.site.register(Interrupt)



class Payment_model(admin.ModelAdmin):
           
    list_display = ('header', 'type', 'amount', 'interrupttype', 'dateTime')
    
admin.site.register(Payment, Payment_model)

class AlertAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'clinic', 'from_addr', 'to_addr', 'event_list', 'waiting_time', 'alert_interv', 'dateTime')
admin.site.register(AlertConfiguration, AlertAdmin)


admin.site.register(AlertMailLog)


#admin.site.register(Notifier_Settings)
admin.site.register(EventSetHeader)
# admin.site.register(PatientEventLog)

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'error_message')
admin.site.register(Attribute, AttributeAdmin)


