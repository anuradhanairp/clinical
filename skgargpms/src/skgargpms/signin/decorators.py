'''
    Applications specific Decorators.
'''
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME

def custome_login_required(template_name = "admin/login.html"):
    '''
        A decorator which return actual decorator, after initalizing it properly. 
        
        New decorator similar to admin staff_member_required one, but here we 
        explicit login.html page and we bypassing the authentication middleware functions
    '''
    
    def innerwrap(view_fun):
        def _checklogin(request, *args, **kwargs):
            if request.user.is_active and request.user.is_staff:
                #The user is valid. So grant the access to run view function.
                return view_fun(request, *args, **kwargs)
            
            assert hasattr(request, 'session'), "The Django admin requires session middleware to be installed.\
                                                 Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
            
            #template_name = kwargs.get('template_name', 'admin/login.html')
            
            defaults = {'template_name': template_name,
                        'authentication_form': AdminAuthenticationForm,
                        'extra_context':{'title': _("Log in"),
                                         'app_path' : request.get_full_path(),
                                         REDIRECT_FIELD_NAME: request.get_full_path(),
                                         'STATIC_URL': settings.STATIC_URL,
                                         
                                         },
                        
                        }
                                      
            return login(request, **defaults)
        
        return wraps(view_fun)(_checklogin)
    
    return innerwrap
