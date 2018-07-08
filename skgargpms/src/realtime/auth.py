######################################################################### 
# Copyright (C) 2009, 2010 Alex Clemesha <alex@clemesha.org>
# 
# This module is part of Hotdot, and is distributed under the terms 
# of the BSD License: http://www.opensource.org/licenses/bsd-license.php
#########################################################################
import os
import sys
from datetime import datetime

from twisted.cred import checkers, credentials, error
from zope.interface import implements

#To make project path relative
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DJANGO_DIR = os.path.join(PROJECT_DIR,"skgargpms")

# Environment setup for your Django project files:
sys.path.append(DJANGO_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'skgargpms.settings'

from django.contrib.sessions.models import Session


class DatabaseChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def requestAvatarId(self, creds):
        username = self._runQuery(username=creds.username, cookie=creds.password)
        if username is None: 
            return error.UnauthorizedLogin('Incorrect credentials')
        else:
            return username

    def _runQuery(self, username=None, cookie=None):
        """Check User permission based on Session.

        The Session Cookie is equivalent to a temporary
        password but has the benefit of avoiding exposing
        a User's real password, and has a limited lifetime.
        """
        #XXX run in deferToThread?
        try:
            session = Session.objects.get(session_key=cookie)
        except DoesNotExist:
            return None
        if session.expire_date > datetime.now():
            return username
        else:
            return None
