#Clinic Software
=== Project Upload steps and required changes ===

1. Stop and move the current server copy from the location /var/sites/twisted/src. 

2. Upload the fresh dev copy to the same location.

3. Change the host name and ports properly under server_working.py and django settings.py file. Make sure that the 
	STATIC PREFIXES of django settings have the correct values.
	
4. Then start the applicaiton in the daemon mode.

== TODO ==

1. Automate the deployment process from localhost to the server.
2. Fix the twisted daemon issues. === FIXED
