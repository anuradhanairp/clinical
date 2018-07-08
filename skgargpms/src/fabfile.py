from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, lcd
from fabric.contrib.console import confirm


'''
	Use 'cd' to keep change directory context while operate with remote systems, and 'lcd' for local machines.

	Use `run` for remote shell command execution.. and `local` for local machine shell executions..
	
'''
def host_type():
    local('uname -a')

def svn_checkout():
	with lcd('/home/users/haridas/fabric'):
		#local('pwd')		
		print 'SVN Check out process ...'
		local('rm -rf skgargpms')
		local('svn co svn://localhost/home/users/haridas/svnrepo/skgargpms')



def server_intial_conf():
	'test..'









