import os, sys, datetime
# Django settings for skgargpms project.

#Adding the parent directory to the ptyhon path, so that from any context this file has access to the files from parent dir.
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print PROJECT_PATH + "=== > PROJECT PATH"

sys.path.insert(0,PROJECT_PATH)
#Import the global settings from the Project Home directory.
import conf
#print conf.PORT, conf.HOST_NAME
STOMP_PORT = 9999
STATIC_PORT = conf.PORT
INTERFACE = conf.HOST_NAME


MAIL_FROM  = 'server@skgargpms.com'
MAIL_TO    = 'sureshk@practiceservellc.com'
EVENT_THRESHOLD = datetime.timedelta(minutes = 1)

#---details for the notifier module ----#
ENABLE_NOTIFIER = "no"       #--- yes for enabling notification and no for disabling the notification ---#
FROM_ADDR = MAIL_FROM
RCPT_TO   = 'sureshk@practiceservellc.com'
EMAIL_SUBJ= 'Alert :- Patient {fname} is still waiting to be  processed...' 
TIMELIMIT=1 #--- The time in minutes , if a patient is still waiting in the queue for more than TIMELIMIT, the notification mail will be triggered
TIMEFRAME=2  #--- The time in hours , on each time the notifier module gets called , the patient data from the last 'TIMEFRAME' hurs will be grouped and then processed 

#-----------------------------------------#


#### Celery Configurations ####

import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"


###  End of Celery Configuration. ###
import settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
      ('Suresh K', 'sureshk@practiceservellc.com'),
      ('Saumya', 'saumya@practiceservellc.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(os.path.dirname(__file__),'db').replace('\\','/') + '/test.db',  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
# TIME_ZONE = 'America/Yakutat'

#Our projects default timezone is UTC , Never change this to any other one. We are takeing this as base timezone.
TIME_ZONE = 'UTC'
EVENING_TIME = '12:35'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static_media').replace('\\','/')


# URL that handles the static files served from STATICFILES_ROOT.
# Example: "http://static.lawrence.com/", "http://example.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = 'http://%s:%s/static/adm/' % (INTERFACE, STATIC_PORT)
#ADMIN_MEDIA_PREFIX = 'http://ditchyourip.com/static/grappelli/'
# A list of locations of additional static files
STATICFILES_DIRS = (
     os.path.join(os.path.dirname(__file__),'static_media').replace('\\','/'),
#    "/var/sites/skgargpms/static_<p align="center">&copy; 2011 PracticeServe</p>media/admin/",
#    "/var/sites/skgargpms/static_media/index_htm_files/"
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$9x5jilr$#_1fheuwave5bzd(+53nqo_cfny(j5kw!d99&n-wd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'skgargpms.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#           os.path.abspath( __file__ )[:-12] + "templates"
)




LOGIN_REDIRECT_URL = '/admin/';

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    
    #Third party apps.
    'djcelery', 
    'south',
    
    #Our Apps.
    'signin',
    'inventory',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
try:
    from extras import *
except ImportError, e:
    print "import extras failed :: " + `e`




