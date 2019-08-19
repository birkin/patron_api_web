# -*- coding: utf-8 -*-

""" Prepares application environment.
    Variables assume project setup like:
    some_enclosing_directory/
        papiweb_code/
            config/
            papiweb_app.py
        env3_papiweb/
     """

import logging, os, pprint, sys


## become self-aware, padawan
current_directory = os.path.dirname( os.path.abspath(__file__) )

## vars
# ACTIVATE_FILE = os.path.abspath( '%s/../../env3_papiweb/bin/activate_this.py' % current_directory )
PROJECT_DIR = os.path.abspath( '%s/../../papiweb_code' % current_directory )
PROJECT_ENCLOSING_DIR = os.path.abspath( '%s/../..' % current_directory )
SITE_PACKAGES_DIR = os.path.abspath( '%s/../../env3_papiweb/lib/python3.6/site-packages' % current_directory )

## load virtual env
# execfile( ACTIVATE_FILE, dict(__file__=ACTIVATE_FILE) )

## sys.path additions
for entry in [PROJECT_DIR, PROJECT_ENCLOSING_DIR, SITE_PACKAGES_DIR]:
 if entry not in sys.path:
   sys.path.append( entry )

## load up env vars
SETTINGS_FILE = os.environ['papiweb__SETTINGS_PATH']  # set in activate_this.py, and activated above
import shellvars
var_dct = shellvars.get_vars( SETTINGS_FILE )
for ( key, val ) in var_dct.items():
    # os.environ[key] = val
    os.environ[key.decode('utf-8')] = val.decode('utf-8')

## set up logging
LOG_PATH = os.environ['papiweb__LOG_PATH']
logging.basicConfig(
    filename=LOG_PATH, level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
    )
log = logging.getLogger(__name__)
log.debug( 'log setup' )

## rock & roll
from papiweb_code.papiweb_app import app as application
