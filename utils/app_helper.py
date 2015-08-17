# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Helper for papiweb_app.py
"""

import datetime, json, logging, os, pprint, time
import flask
import requests
from p_api import PatronAPI


# logger = logging.getLogger(__name__)


class PapiHelper( object ):
    """ Helper functions for app->handle_ezb_v1() """

    def __init__( self, logger ):
        self.logger = logger

    ## main functions (called by papiweb_app.py functions)

    def validate_request( self, params ):
        """ Checks params, ip, & auth info; returns boolean.
            Called by papiweb_app.handle_v1() """
        self.logger.debug( 'starting validate..., params, `%s`' % params )
        validity = False
        keys_good = self.check_keys( params )
        ip_good = self.check_ip( flask.request.remote_addr )
        # auth_good = self.check_auth_key( params )
        if keys_good and ip_good:
            validity = True
        self.logger.debug( 'validity, `%s`' % validity )
        return validity

    def do_lookup( self, params ):
        """ Runs lookup; returns patron-api html output.
            Called by papiweb_app.handle_v1() """
        defaults = self.load_papi_defaults()
        papi = PatronAPI( defaults )
        papi_json = papi.grab_data( params['user_barcode'] )
        self.logger.debug( 'papi_json, `%s`' % papi_json )
        jdct = json.loads( papi_json )
        return jdct

    ## helper functions (called by above functions)

    def load_papi_defaults( self ):
        """ Loads up non-changing patron_api defaults.
            Called by do_lookup() """
        defaults = {
            'PATRON_API_URL_PATTERN': unicode( os.environ['PAPI__PATRON_API_URL_PATTERN'] ),
            }
        self.logger.debug( 'defaults, `%s`' % defaults )
        return defaults

    def check_keys( self, params ):
        """ Checks required params; returns boolean.
            Called by validate_request() """
        keys_good = False
        patron_barcode = params.get( 'patron_barcode', '' )
        self.logger.debug( 'patron_barcode, `%s`' % patron_barcode )
        if len( patron_barcode ) > 5:
            keys_good = True
        self.logger.debug( 'keys_good, `%s`' % keys_good )
        return keys_good

    # def check_keys( self, params ):
    #     """ Checks required keys; returns boolean.
    #         Called by validate_request() """
    #     self.logger.debug( 'params.keys(), `%s`' % params.keys() )
    #     ( keys_good, match_found ) = ( False, 'init' )
    #     required_keys = [ 'patron_barcode' ]
    #     for required_key in required_keys:
    #         if required_key not in params.keys():
    #             match_found = 'no'
    #             break
    #         if match_found == 'init':
    #             keys_good = True
    #     self.logger.debug( 'keys_good, `%s`' % keys_good )
    #     return keys_good

    # def check_keys( self, params ):
    #     """ Checks required keys; returns boolean.
    #         Called by validate_request() """
    #     self.logger.debug( 'params.keys(), `%s`' % params.keys() )
    #     keys_good = False
    #     required_keys = [ 'patron_barcode' ]
    #     for required_key in required_keys:
    #         if required_key not in params.keys():
    #             break
    #         if required_key == required_keys[-1]:
    #             keys_good = True
    #     self.logger.debug( 'keys_good, `%s`' % keys_good )
    #     return keys_good

    # def check_ip( self, perceived_ip ):
    #     """ Checks ip; returns boolean.
    #         Called by validate_request() """
    #     ip_good = False
    #     for user in self.LEGIT_USERS:
    #         if user['ip'] == perceived_ip:
    #             ip_good = True
    #             self.user_dct = user
    #             break
    #     if ip_good is not True:
    #         self.logger.debug( 'bad ip, `%s`' % flask.request.remote_addr )
    #     self.logger.debug( 'ip_good, `%s`' % ip_good )
    #     return ip_good

    def check_ip( self, perceived_ip ):
        """ Checks ip; returns boolean.
            Called by validate_request() """
        LEGIT_IPS = json.loads( unicode(os.environ['papiweb__LEGIT_IPS']))
        ip_good = False
        if perceived_ip in LEGIT_IPS:
            ip_good = True
        else:
            self.logger.debug( 'bad ip, `%s`' % flask.request.remote_addr )
        self.logger.debug( 'ip_good, `%s`' % ip_good )
        return ip_good

    # def check_ip( self ):
    #     """ Checks ip; returns boolean.
    #         Called by validate_request() """
    #     LEGIT_IPS = json.loads( unicode(os.environ['papiweb__LEGIT_IPS']))
    #     ip_good = False
    #     if flask.request.remote_addr in LEGIT_IPS:
    #         ip_good = True
    #     else:
    #         self.logger.debug( 'bad ip, `%s`' % flask.request.remote_addr )
    #     self.logger.debug( 'ip_good, `%s`' % ip_good )
    #     return ip_good

    # def check_auth_key( self, params ):
    #     """ Checks auth key; returns boolean.
    #         Called by validate_request() """
    #     auth_good = False
    #     if self.user_dct is not None:
    #         if params.get( 'api_auth_key', 'nope' ) == self.user_dct['api_auth_key']:
    #             auth_good = True
    #     self.logger.debug( 'auth_good, `%s`' % auth_good )
    #     return auth_good

    # def check_auth( self, params ):
    #     """ Checks auth params; returns boolean.
    #         Called by validate_request() """
    #     API_AUTHORIZATION_CODE = unicode( os.environ['papiweb__API_AUTHORIZATION_CODE'] )  # for v1
    #     API_IDENTITY = unicode( os.environ['papiweb__API_IDENTITY'] )  # for v1
    #     auth_good = False
    #     if params.get( 'api_authorization_code', 'nope' ) == API_AUTHORIZATION_CODE:
    #         if params.get( 'api_identity', 'nope' ) == API_IDENTITY:
    #             auth_good = True
    #     self.logger.debug( 'auth_good, `%s`' % auth_good )
    #     return auth_good

    # end class Helper()

