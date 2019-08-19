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
CONFIG_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.dirname( CONFIG_DIR )  # papiweb_code
PROJECT_ENCLOSING_DIR = os.path.dirname( PROJECT_DIR )
for entry in [PROJECT_DIR, PROJECT_ENCLOSING_DIR]:
 if entry not in sys.path:
   sys.path.append( entry )

## load up env vars
SETTINGS_FILE = os.environ['papiweb__SETTINGS_PATH']
import shellvars
var_dct = shellvars.get_vars( SETTINGS_FILE )
for ( key, val ) in var_dct.items():
    os.environ[key.decode('utf-8')] = val.decode('utf-8')

## set up logging
LOG_PATH = os.environ['papiweb__LOG_PATH']
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
    )
log = logging.getLogger(__name__)
log.debug( 'log setup' )

## rock & roll
from papiweb_code.papiweb_app import app as application
