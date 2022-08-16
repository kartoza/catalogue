#!/bin/bash

echo "Killing any active postgresql connections"
echo "If this still does not work drop to runlevel 1, "
echo "become postgres and drop the database: "
echo ""
echo "sudo init 1"
echo "(choose prompt with no networking at this point)"
echo "sudo su - postgres"
echo "dropdb sac"
echo "-----"
LIST=`echo "select procpid from pg_stat_activity where datname='sac'" | psql sac | grep -v rows | grep -v "\-\-\-\-\-\-" | grep -v procpid`
for ITEM in $LIST
do 
  # note do not use -9!
  sudo kill $ITEM
done
