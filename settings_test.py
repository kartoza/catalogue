from settings import *
import os

DATABASES = {
        'default': { #new db that does not mimic acs system
         'ENGINE' : 'sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
         'NAME' : 'test_sac.sqlite',             # Or path to database file if using sqlite3.
         'USER' : '',             # Not used with sqlite3.
         'PASSWORD' : '',         # Not used with sqlite2.
         'HOST' : '',             # Set to empty string for localhost. Not used with sqlite3.
         'PORT' : '',             # Set to empty string for default. Not used with sqlite3.
         },
        'acs': {  #legacy acs port to django
        'ENGINE' : 'sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
         'NAME' : 'test_acs.sqlite',             # Or path to database file if using sqlite3.
         'USER' : '',             # Not used with sqlite3.
         'PASSWORD' : '',         # Not used with sqlite2.
         'HOST' : '',             # Set to empty string for localhost. Not used with sqlite3.
         'PORT' : '',             # Set to empty string for default. Not used with sqlite3.
         }
        }

# Added by Tim - url that holds directories of thumbnails...
THUMBS_ROOT = os.path.join(ROOT_PROJECT_FOLDER, 'catalogue', 'tests' ,'thumbs_out')
# And this is the dir that holds imagery
IMAGERY_ROOT = os.path.join(ROOT_PROJECT_FOLDER, 'catalogue', 'tests' ,'imagery_mastercopies')
