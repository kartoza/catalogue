#!/bin/bash
txt2tags -t txt index.t2t ../../README
cp ../../README ../project_static_files/
source ../../python/bin/activate
make html
#make latex
#cd build/latex/
#make all-pdf
#cd ..
#cd ..
#cp build/latex/MyGreatCircle-API-Docs.pdf .

# put the docs into the static dir
cp -r build/html ../static/pydoc
# make js docs too
cd jsdoc-toolkit
./generate_docs.sh
cd ..
echo "Docs should now be visible at:"
echo "/static/pydoc/"
echo "/static/jsdoc"

# Postgresql schema docs using postgresql-autodoc (installable via apt)
mkdir ../static/pgdoc
postgresql_autodoc -d sac -f ../static/pgdoc/catalogue -m "catalogue"
