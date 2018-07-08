import re

#Read values from global file GLOBALS.sh, used with the python settings files

import sys,os
#print sys.path
#Get the absolute path of the global configuration file, this will remove resolution problems to this conf file.
global_conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'GLOBALS.sh')

global_file = open(global_conf_file,'r')

global_vars = global_file.read()

#HTTP PORT, or Default port of the python clinic workflow project.
reg_port = re.compile('''PORT=([^\n ]+)''')

try:
	PORT = int(reg_port.findall(global_vars)[0])

except IndexError:
	PORT = 80


#HOST name of the machine  or IP address
reg_host = re.compile('''HOST_NAME=['"]([^\n "']+)''')

try:
	HOST_NAME = reg_host.findall(global_vars)[0]
except IndexError:
	HOST_NAME = 'localhost'



