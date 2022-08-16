#!/bin/bash
cd django_project
SETTINGS="--settings=core.settings.dev_${USER}"
python manage.py graph_models catalogue $SETTINGS | dot -Tpng -o ../model_diagram.png ; display ../model_diagram.png
python manage.py graph_models dictionaries $SETTINGS | dot -Tpng -o ../dict_model_diagram.png ; display ../dict_model_diagram.png
python manage.py graph_models search $SETTINGS | dot -Tpng -o ../search_model_diagram.png ; display ../search_model_diagram.png
cd ..
