# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Helper for bdpyweb_app.py
"""

import datetime, json, os, pprint, time
import flask
import requests
from p_api import PatronAPI


class PapiHelper( object ):
    """ Helper functions for app->handle_ezb_v1() """

    # def __init__( self, logger ):
    #     self.logger = logger
    #     self.logger.debug( 'papi_helper initialized' )

    ## main functions (called by papiweb_app.py functions)

    def validate_request( self, params ):
        """ Checks params, ip, & auth info; returns boolean.
            Called by papiweb_app.handle_v1() """
        validity = False
        keys_good = self.check_keys( params )
        ip_good = self.check_ip()
        auth_good = self.check_auth( params )
        if keys_good and ip_good and auth_good:
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
        """ Checks required keys; returns boolean.
            Called by validate_request() """
        keys_good = False
        required_keys = [ 'api_authorization_code', 'api_identity', 'isbn',  'user_barcode' ]
        for required_key in required_keys:
            if required_key not in params.keys():
                break
            if required_key == required_keys[-1]:
                keys_good = True
        self.logger.debug( 'keys_good, `%s`' % keys_good )
        return keys_good

    def check_ip( self ):
        """ Checks ip; returns boolean.
            Called by validate_request() """
        LEGIT_IPS = json.loads( unicode(os.environ['bdpyweb__LEGIT_IPS']))
        ip_good = False
        if flask.request.remote_addr in LEGIT_IPS:
            ip_good = True
        else:
            self.logger.debug( 'bad ip, `%s`' % flask.request.remote_addr )
        self.logger.debug( 'ip_good, `%s`' % ip_good )
        return ip_good

    def check_auth( self, params ):
        """ Checks auth params; returns boolean.
            Called by validate_request() """
        API_AUTHORIZATION_CODE = unicode( os.environ['bdpyweb__API_AUTHORIZATION_CODE'] )  # for v1
        API_IDENTITY = unicode( os.environ['bdpyweb__API_IDENTITY'] )  # for v1
        auth_good = False
        if params.get( 'api_authorization_code', 'nope' ) == API_AUTHORIZATION_CODE:
            if params.get( 'api_identity', 'nope' ) == API_IDENTITY:
                auth_good = True
        self.logger.debug( 'auth_good, `%s`' % auth_good )
        return auth_good

    # end class Helper()

