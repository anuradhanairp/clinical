# -*- coding: utf-8 -*-
######################################################################### 
# Copyright (C) 2009, 2010 Alex Clemesha <alex@clemesha.org>
# 
# This module is part of Hotdot, and is distributed under the terms 
# of the BSD License: http://www.opensource.org/licenses/bsd-license.php
#########################################################################
"""
Start all server components of Hotdot.

Each component is a 'Twisted Service':
    - Django (using twisted.web.wsgi)
    - Orbited (using the orbited 'cometsession' and 'proxy' modules)
    - Stomp pub/sub server (using the 'morbid' module from MorbidQ)
    - RestQMessageProxy (Orbited messages filter/logger/modifier)
"""
import sys,os

#Get the Project Main Directory, that should be intependent to the current path of the python.
PROJECT_DIR =  os.path.dirname(os.path.abspath(__file__))

#Include project directory to the Python path.
sys.path.insert(0,PROJECT_DIR)

#Include twisted modules.
from twisted.web import static, resource, server
from twisted.application import internet, service
import twisted.web.proxy as twisted_proxy

from morbid import StompFactory


# Config
#from orbited import logging, config
#import logging as logging
import logging
logging.basicConfig()
from orbited import config

#logging.setup(config.map)

#Taking Values from global python file ``conf.py``.
from conf import PORT, HOST_NAME
INTERFACE = HOST_NAME


#Runtime config, is there a cleaner way?:
config.map["[access]"]={(INTERFACE, 9999):"*"}

STATIC_PORT = PORT
RESTQ_PROXY_PORT = 5000
STOMP_PORT = 9999


#The below depend on Orbited's logging.setup(...), from above.
from orbited import cometsession
from orbited import proxy

#local imports
from skgargpms.twisted_wsgi import get_root_resource
from realtime.stompfactory import get_stomp_factory
from realtime.message_handlers import MESSAGE_HANDLERS
from realtime.restq import RestQMessageProxy

#Create Twisted Application.
application = service.Application('skgargpms')

# make a new MultiService to hold the thread/web services, add its parent as twisted application.
multi = service.MultiService()
multi.setServiceParent(application)


# Django and static file server, Common HTTP server.:
root_resource = get_root_resource(multi)

#Default Webserver which server the Django project files.
static_media = os.path.join(os.path.dirname(__file__),'skgargpms/static_media').replace('\\','/')
root_resource.putChild("static", static.File(static_media))
favicon = os.path.join(os.path.dirname(__file__),'skgargpms/static_media/favicon.ico').replace('\\','/')
root_resource.putChild('favicon.ico',static.File(favicon))

#Sproutcore Mobile application URL.
root_resource.putChild('mobile',static.File(os.path.join(os.path.dirname(__file__),'skgargpms/static_media/mobile').replace('\\','/')))


#Reverse proxy setup - fdesk.ditchyourip.com/clinic_workflow* ---> fdesk.ditchyourip.com:9000/clinic_workflow* 
root_resource.putChild('clinic_workflow',twisted_proxy.ReverseProxyResource(INTERFACE,9000,"clinic_workflow"))

http_factory = server.Site(root_resource, logPath=PROJECT_DIR + "/logs/http.log")
tcpServ = internet.TCPServer(STATIC_PORT, http_factory, interface=INTERFACE).setServiceParent(multi)

# Orbited server: For Commetsession -
proxy_factory = proxy.ProxyFactory()
internet.GenericServer(cometsession.Port, factory=proxy_factory, resource=root_resource, childName="tcp", interface=INTERFACE).setServiceParent(multi)


# Stomp server:
stomp_factory = get_stomp_factory(INTERFACE, RESTQ_PROXY_PORT)
internet.TCPServer(STOMP_PORT,stomp_factory, interface=INTERFACE).setServiceParent(multi)

# RestQMessageProxy (message filter/logger/modifier):
restq_resource = RestQMessageProxy(MESSAGE_HANDLERS)
restq_proxy_factory = server.Site(restq_resource, logPath=PROJECT_DIR + "/logs/restqproxy.log")
internet.TCPServer(RESTQ_PROXY_PORT, restq_proxy_factory, interface=INTERFACE).setServiceParent(multi)


