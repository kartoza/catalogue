#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Usage: $(basename $0) database_name"
  exit $E_BADARGS
fi

for script in $(ls *[0-9].sh|sort)
do
    echo "Executing script:", $script
    bash $script $1
done
