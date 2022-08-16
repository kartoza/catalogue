#!/bin/bash
export PGHOST=elephant
export PGPASSWORD=$1
DB=sac
#createdb sac_test
#createlang plpgsql sac
#ssh -p 8697 elephant "psql $DB < /usr/share/postgresql-8.3-postgis/lwpostgis.sql"
#ssh -p 8697 elephant "psql $DB < /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql"


echo "At the prompt that follows say 'no' when asked if you"
echo "wish to create a superuser"
echo "Press enter to continue"
# Pause to give user time to read above:
read

python manage.py syncdb
psql $DB < catalogue/sql/auth_user.sql                 
psql $DB < catalogue/sql/auth_group.sql                
psql $DB < catalogue/sql/auth_group_permissions.sql    
psql $DB < catalogue/sql/auth_user_groups.sql          
psql $DB < catalogue/sql/auth_permission.sql           
psql $DB < catalogue/sql/auth_user_user_permissions.sql 
psql $DB < catalogue/sql/auth_message.sql              

#pushd .
#cd catalogue/sql_dumps
#./restore.sh
#popd
unset PGPASSWORD
