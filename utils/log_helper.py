# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Handles log setup.
Assumes system's logrotate.
"""

import logging, os


def setup_logger():
    """ Returns a logger to write to a file.
        Called by papiweb_app.py """
    LOG_PATH = unicode( os.environ.get('papiweb__LOG_PATH') )
    LOG_LEVEL = unicode( os.environ.get('papiweb__LOG_LEVEL') )
    formatter = logging.Formatter( '[%(asctime)s] %(levelname)s | %(module)s->%(funcName)s() | ln %(lineno)d | %(message)s' )
    logger = logging.getLogger( __name__ )
    level_dict = { 'debug': logging.DEBUG, 'info':logging.INFO }
    logger.setLevel( level_dict[LOG_LEVEL] )
    file_handler = logging.FileHandler( LOG_PATH )
    file_handler.setFormatter( formatter )
    logger.addHandler( file_handler )
    return logger
