# -*- coding: utf-8 -*-


"""
Handles log setup.
Assumes system's logrotate.
"""

import logging, os


_logger = None


def setup_logger():
    """ Returns a logger to write to a file.
        Called by papiweb_app.py """
    # if not logging.root.handlers:
    global _logger
    if _logger is None:
        print( 'HERE-A' )
        logger = logging.getLogger( __name__ )
        LOG_PATH = os.environ.get('papiweb__LOG_PATH')
        LOG_LEVEL = os.environ.get('papiweb__LOG_LEVEL')
        # formatter = logging.Formatter( '[%(asctime)s] %(levelname)s | %(module)s->%(funcName)s() | ln %(lineno)d | %(message)s' )
        formatter = logging.Formatter( '[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s' )
        # logger = logging.getLogger( __name__ )
        level_dict = { 'debug': logging.DEBUG, 'info':logging.INFO }
        logger.setLevel( level_dict[LOG_LEVEL] )
        file_handler = logging.FileHandler( LOG_PATH )
        file_handler.setFormatter( formatter )
        logger.addHandler( file_handler )
        logger.debug( 'logger initialized' )
        _logger = logger
    else:
        print( 'HERE-B' )
        logger = _logger
    return logger



# def setup_logger():
#     """ Returns a logger to write to a file.
#         Called by papiweb_app.py """
#     LOG_PATH = os.environ.get('papiweb__LOG_PATH')
#     LOG_LEVEL = os.environ.get('papiweb__LOG_LEVEL')
#     # formatter = logging.Formatter( '[%(asctime)s] %(levelname)s | %(module)s->%(funcName)s() | ln %(lineno)d | %(message)s' )
#     formatter = logging.Formatter( '[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s' )
#     logger = logging.getLogger( __name__ )
#     level_dict = { 'debug': logging.DEBUG, 'info':logging.INFO }
#     logger.setLevel( level_dict[LOG_LEVEL] )
#     file_handler = logging.FileHandler( LOG_PATH )
#     file_handler.setFormatter( formatter )
#     logger.addHandler( file_handler )
#     logger.debug( 'logger initialized' )
#     return logger



