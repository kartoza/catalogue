Django 1.2 -> 1.4 migration guide
=================================

.. note:: This this applies only to repository tagged as *pre-django-1.4*


Preparatory work
----------------

  * we moved a lot of files around so it's good to remove all ``*.pyc`` files::

      find . -type f -iname '*.pyc' -print0| xargs -0 rm


Migration procedure
-------------------

  #. update repository and checkout master HEAD: ``git pull; git checkout master``
  #. update python packages::

      pip install --upgrade django==1.4.2 django-debug-toolbar==0.9.4

  #. move ``settings_local.py`` to ``core``::

      mv settings_local.py core/

  #. update ``settings_local.py`` according to ``settings_local.py.templ``

  * Optionally:

    * regenerate documentation: ``cd docs/sphinx; make clean; make html; cd -``
    * move non-tracked ``geoip_data`` to ``core/geoip_data``::

        mv geoip_data/* core/geoip_data/


Run tests and development server
--------------------------------

  * to run full test suite execute::

     python manage.py test --settings=core.settings_test catalogue.tests

  * to run development server execute ``python manage.py runserver``

.. note:: Django 1.4 introduced a project folder contains settings.py, urls.py, templates, static files, ...
          When using non default settings file (like for testing), we need to specify that project folder