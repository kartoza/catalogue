#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $(basename $0) database_name"
  exit $E_BADARGS
fi

for script in $(ls pycsw_integration*.sql|sort)
do
    echo "Executing script:", $script
    psql -h db -U postgres -d gis -f "$script"
done
