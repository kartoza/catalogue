#!/bin/bash
cd /home/web/sac
tar cfz python.tar.gz python
mv sac_catalogue ../catalogue
virtualenv --relocatable python
mv python ../catalogue/venv
cd ../catalogue
rm catalogue.log
find . -iname '*.pyc' -exec rm {} \;
virtualenv venv
