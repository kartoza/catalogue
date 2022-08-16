#!/bin/bash


export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=$PYTHONPATH:`pwd`
python runClipping.py
