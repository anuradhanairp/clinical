#!/bin/bash

set -e

if [ $1 ]
then

	sqlite3 $1 'delete from signin_payment;delete from signin_patienteventlog;delete from signin_eventsetheader;delete from signin_patient;vacuum;'

	echo "Truncated.. following tables..."

	echo "Payment,EventSetHeader, PatientEventLog, Patient"


else

	echo "Useage : \" \$sqlite_truncate.sh db_file \" "

fi
