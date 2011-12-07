#!/bin/bash
source ../python/bin/activate
if test -z "$1"
then
    echo "No command-line arguments - compressed js will be generated"
    java -jar closure-compiler/compiler.jar --js catalogue/static/js/catalogue.uncompressed.js --js_output_file catalogue/static/js/js/catalogue.js
else
    echo "Command line argument given - UNcompressed js will be generated"
    cp catalogue/static/js/catalogue.uncompressed.js catalogue/static/js/catalogue.js
fi
python manage.py collectstatic --noinput
python manage.py runserver_plus -v 2
