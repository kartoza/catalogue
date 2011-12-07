#!/bin/bash
source ../python/bin/activate
python manage.py syncdb
# update the migration definitions with changes to our model (if any)
python manage.py schemamigration catalogue --auto
# apply any schema changes if our model (e.g. if you pulled them via git)
python manage.py migrate catalogue --database=default

deactivate
