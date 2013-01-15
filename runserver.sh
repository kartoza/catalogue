#!/bin/bash
echo "Run $0 -d to run standard runserver in debugger mode"
source ../python-live/bin/activate
#python manage.py collectstatic --noinput

if [ $# -ne 1 ] 
then
  echo "Running using runserver_plus"
  python manage.py runserver_plus
else
  echo "Running using runserver --pdb"
  echo "Note: does not currently work with django 1.3 static_files app"
  #pdb option below requires installation of django-pdb and 
  #will break at the start of each view
  # alternatively add 
  # import pdb; pdb.set_trace()
  # anywhere in the source to force a breakpoint
  # doesnt work with runserver_plus
  python manage.py runserver
  #--pdb
fi
