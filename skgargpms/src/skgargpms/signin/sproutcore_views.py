'''
	This files defines Ajax backend views from all sproutcore connections.
'''

from django.conf import settings
from django.contrib.auth import load_backend
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.http import cookie_date
from django.utils.importlib import import_module
import simplejson
import time



SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'



def login(request):
	'''
		Initial sproutcore login call, it's a POST request 
		
		Sproutcore Specific :-
		
			Bellow method of taking key/value pair from the POST request is possible when we send request from
			Sproutcore, because it behaves non-standard way now and looks like posted key/value pair actually 
			saved under POST dict as a first KEY and empty VALUE filed.
		
		
		The request object is actually passed throw several Middlewares. in which first one is ,
		
		
		1. SessionMidleWare :
		
			This Middleware modify the request object and add a session attribute to the request object.This 
			session object handles all session related operations with session_backend. We pass the sessionid value 
			as constructor to create session object.
			
		2. AuthMiddleware :-
			
			By using the Session object, this middleware check the user logged in or not, if the user is not
			logged in the it attache a AnonimouseUser() object to the request.user field. Otherwise we will
			get the actual user object under request object.
			
			Using this request.user object we can check which user is been logged in currently and other details.
		 
		 
		 response Object:- JSON.
		 
		 a. When already logged in case - 
				 
				 if active cookie is exist.
					 response = { session_active = 'YES' }
				 else
					 response = { session_active = 'NO' }
					 
		 b. User logged in successfully using user/pass pair, we using django middlewares to set the
			session cookie and all.
			
			so response from django will be - 
			response = {session_active: 'YES'}
					 
		 c. User explicit login using username/password and interact via json only replay.
			 
				 if success
					 response = { session_active = 'YES',
								  session_cookie: {	id: new_sessionid',
												  max_age: 'seconds',
												  domain: 'domain_name',
												  path:   'Url path',
												  secure: 'Yes/No',
												  httponly: 'Yes/No'
											   
											 } 
								}
					 
				 if failed:
					 response = {session_active = 'NO', }
				 
		
	'''
	
	#The Post Request is from  Sproutcore, that requires some crazy steps.
	#Special case of the Sproutcore. It sends POST in some wiered manner, instead of key/value parir
	#it only send full content inside key ie; POST = {'content': ''}
	
	post_dict = {}
	if request.POST:
		post_dict = simplejson.loads(request.POST.keys()[0])
	
	
	  
	if not post_dict.get('user',None):
		'''
			The 'user' filed must be null when the initial login with cookie. We now forced to user,
			our own cookie handling at the request time and response time, due to our application may comes
			under, different URL, so the django keep session cookie for '/' only. So the django session middleware
			doesn't support cookie based on other part unless we changed the gloabal settings of django cookie.
			 
			
		'''
		
		#Get Browser cookie from request.
		browser_cookie = post_dict.get('pwd',None)
		
		#Codes from SEssion and Auth middleware
		
		#From Session middleware
		engine = import_module(settings.SESSION_ENGINE)
		session_key = browser_cookie
		request.session = engine.SessionStore(session_key)
		
		#From Auth Middleware
		user_id = request.session[SESSION_KEY]
		backend_path = request.session[BACKEND_SESSION_KEY]
		backend = load_backend(backend_path)
		user = backend.get_user(user_id)
		
		#Reset the Access flag, to prevent middleware to trigger it again.
		request.session.accessed = False
		request.session.modified = False
		
		
		
		if user.is_active:
			'The user session is active.'
			
			response = {'session_active':'YES',
						'request.POST': request.POST,
						'csrftoken': request.COOKIES.get('csrftoken',None),
						'Logged In': request.user.is_active
						}
			
			#response = {'session_active': 'YES'}
			response = simplejson.dumps(response)
			return HttpResponse(response,mimetype='application/json')
		else:
			#Cookie not valid
			
			return HttpResponse(status = 401)
		
	else:
		'''	
			No previous Browser Cookie for session was set.
		'''
		  
		if post_dict:
			'User clicking the signin page.'
		   
			username = post_dict.get('user',None)
			password = post_dict.get('pwd',None)
			user = User.objects.filter(username = username)
			
			if user:
				'User exist.'
				
				user = user[0]
				#from django.contrib.auth import load_backend, get_backend, authenticate
		 
				if user.check_password(password):
					'''
						We successfully authenticated with the django backend.
						
						1. Need to set new session cookie for this user 
						2. update new session cookie back to browser.
						
						Here we Adding the informations to request.session object which was creaed by
						Session Middleware when we receive the request from client.The same middleware
						update and save the cookie data updated in this view when we returning the response
						object.
						
						Above method has one limitation, which force us to set our cookie to the django predefined 
						variable, but we need to be customize according to our url, so we prevent the session
						settings now and we do that explicitly below.
						
					'''
					
					if SESSION_KEY in request.session:
						if request.session[SESSION_KEY] != user.id:
							# To avoid reusing another user's session, create a new, empty
							# session if the existing session corresponds to a different
							# authenticated user.
							request.session.flush()
					else:
						request.session.cycle_key()
					
					request.session[SESSION_KEY] = user.id
					request.session[BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
					
					if hasattr(request, 'user'):
						request.user = user
							   
				   
					
					#Save the session to Backend here itself to prevent it to be done by session Middleware.
					#here we preventing sesion middleware to send a cookie to server, we will explicitly do that
					#task, to manage the 'path' variable of cookie, what ever value we like.
					request.session.save()
					request.session.accessed = False
					request.session.modified = False
					
					#The javascript by default consider 'path', 'domain' from its current URL.
					max_age = request.session.get_expiry_age()
					expires_time = time.time() + max_age
					expires = cookie_date(expires_time)
					
					session_cookie = {
									  'id': request.session.session_key,
									  'max_age': max_age,
									  'expires': expires,
									  'secure': None,
									  'httponly': None
									  
									  
									  }
					
					msg = {'session_active':'YES',
						   'session_cookie' : session_cookie
						  }
					
					msg = simplejson.dumps(msg)
					
					return HttpResponse(msg, mimetype='application/json')
		 
		return HttpResponse(status = 401)
	
   