#!/usr/bin/env python
import os
import signal

# Change this to your process name

print "Checking for Stale Celery Queue Processes"
processname = 'twistd'
for line in os.popen("ps xa"):
        fields = line.split()
        pid = fields[0]

        if line.find(processname) > 0 :
                #print fields
                #print pid

                # Kill the Process. Change signal.SIGHUP to signal.SIGKILL if you like
                os.kill(int(pid), signal.SIGKILL)

                # Do something else here
                print "Kill Stale Process"

                # Restart the process
                #os.system(processname)

                # Hop out of loop
