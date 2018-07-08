###########################################################################################

#The Main Global veriables used with the Startup Scripts in the project environment.
#So ue this as the global settings for all other areas of the project.


#********** NO TRAILING '/' FOR EVERY DIRECTORY PATHS ******************

############################# CLINIC WORKFLOW GLOBAL SETTINGS ############################


#Main Project HOME directory, Change this according to the directory where we put our project.
#To get the absolute path of this folder use the following methods.
temp_cur_dir=`dirname $0`
PROJECT_HOME_DIR=`cd $temp_cur_dir; pwd`

#echo $PROJECT_HOME_DIR
#Give hostname or IP here.., Based on the our current hosts IP or its name, Default value is 'localhost'
HOST_NAME='localhost'


#Main Website PORT, Default port is 80
PORT=8000




########  Additional variables -- No need to edit here #########
#Django Project Home directory.
DJANGO_PROJ_DIR="$PROJECT_HOME_DIR/skgargpms"


