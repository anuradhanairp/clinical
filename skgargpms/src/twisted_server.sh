#!/bin/bash

#Startup Script to start the Twisted server.


#Error correction mode.
set -e


#Include project Configuration File.

#Import global settings.
CURRENT_DIR=`dirname $0`

. $CURRENT_DIR/GLOBALS.sh

#PROJECT_HOME_DIR=$PROJECT_HOME_DIR  #Exclude leading "/".

PROJECT_CONF='server_working.py'
KILL_CELEREY_SCRIPT='killStaleTwisted.py'
TWISTED_PID="$PROJECT_HOME_DIR/logs/twistd.pid"
TWISTED_LOG="$PROJECT_HOME_DIR/logs/twistd.log"

restart_server()
{


              echo  "Restarting Twisted Server ..."

                #Kill the Twisted Process.

                  if [ -f ./twisted_server.sh ]
                  then
		 	echo "stopping twisted server"
                        #sh twisted_server.sh stop
			stop_server
			echo "sleep 10 after stop"
			sleep 10
			echo "start twisted server"
		        #sh twisted_server.sh start
			start_server
	
                  fi
		
		sh tracd restart




}

start_server() 
{
	echo  "Starting Twisted Server ... "
	#Starting the server with project configuration.
	#twistd -y "$PROJECT_HOME_DIR/$PROJECT_CONF" --pidfile=$TWISTED_PID  --logfile=$TWISTED_LOG
	
	twistd -y "$PROJECT_HOME_DIR/$PROJECT_CONF"
	if [ $? -eq 0 ] 
        then
          echo -e '\033[32m Aplication Started ... !'
	else
	  echo -e '\033[31m Error while starting the server !'

	fi
	
	if [ -f $PROJECT_HOME_DIR/celeryd ]
	then
	 	sh $PROJECT_HOME_DIR/celeryd start

        fi
	if [ -f $PROJECT_HOME_DIR/celerybeat ]
        then
  
		sh $PROJECT_HOME_DIR/celerybeat start

        fi
	
	sh $PROJECT_HOME_DIR/tracd start

}

stop_server() {
	      echo  "Stoping Twisted Server ..."

                #Kill the Twisted Process.
                kill -9 `cat $TWISTED_PID`
		
		  if [ -f $PROJECT_HOME_DIR/celeryd ]
	          then
			sh $PROJECT_HOME_DIR/celeryd stop

	          fi
			
	          if [ -f $PROJECT_HOME_DIR/celerybeat ]
	          then
          	      sh $PROJECT_HOME_DIR/celerybeat stop
	          fi

 	          if [ -f $PROJECT_HOME_DIR/killStaleTwisted.py ]
                  then

			/usr/bin/env python $PROJECT_HOME_DIR/killStaleTwisted.py

                  fi
		
		sh $PROJECT_HOME_DIR/tracd stop

 }


case "$1" in
	start)
		start_server	
	;;
	
	stop)
		stop_server
	;;
	
	restart)
                 	
		echo  "Restarting ... "
		restart_server		
#		kill -9 `cat $TWISTED_PID` &> /dev/null
#		
#		start_server

	;;
	
	*)
		echo  "Invalid Option, Script only support start , stop and restart."
		
	esac
	



#cd $PROJECT_HOME




