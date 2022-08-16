#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $(basename $0) database_name"
  exit $E_BADARGS
fi

for script in $(ls cleanup*.sql|sort)
do
    echo "Executing script:", $script
    psql -f $script -d $1
done
