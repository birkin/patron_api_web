# -*- coding: utf-8 -*-

"""
Helper for papiweb_app.py
"""

import datetime, json, logging, os, pprint, time

import flask, requests
from papiweb_code.utils.p_api import PatronAPI


# logger = logging.getLogger(__name__)


class PapiHelper( object ):
    """ Helper functions for app->handle_ezb_v1() """

    def __init__( self, logger ):
        self.logger = logger
        self.defaults = {
            'PATRON_API_URL_PATTERN': os.environ['papiweb__PATRON_API_URL_PATTERN'],
            }

    ## main functions (called by papiweb_app.py functions)

    def validate_request( self, params ):
        """ Checks params, ip, & auth info; returns boolean.
            Called by papiweb_app.handle_v1() """
        self.logger.debug( 'starting validate..., params, `%s`' % params )
        validity = False
        keys_good = self.check_keys( params )
        ip_good = self.check_ip( flask.request.remote_addr )
        if keys_good and ip_good:
            validity = True
        self.logger.debug( 'validity, `%s`' % validity )
        return validity

    def do_lookup( self, params ):
        """ Runs lookup; returns patron-api html output.
            Called by papiweb_app.handle_v1() """
        self.logger.debug( "params['patron_barcode'], `%s`" % params['patron_barcode'] )
        papi = PatronAPI( self.defaults )
        self.logger.debug( 'a' )
        try:
            papi_json = papi.grab_data( params['patron_barcode'] )
            self.logger.debug( 'b' )
            self.logger.debug( 'papi_json, `%s`' % papi_json )
            self.logger.debug( 'c' )
            jdct = json.loads( papi_json )
            self.logger.debug( 'jdct, `%s`' % pprint.pformat(jdct) )
        except Exception as e:
            jdct = self.build_error_dict( e )
        return jdct

    def build_response_dct( self, params, jdct ):
        """ Assembles request and response parts of the returned response.
            Called by papiweb_app.handle_v1() """
        request_dct = {
            'timestamp': unicode( datetime.datetime.now() ),
            'patron_barcode': params['patron_barcode']
            }
        return_dct = {
            'request': request_dct,
            'response': jdct
            }
        return return_dct

    ## helper functions (called by above functions)

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

    def build_error_dict( self, e ):
        """ Builds error dict.
            Called by self.do_lookup() """
        dct = { 'error': unicode(repr(e)) }
        return dct

    # end class PapiHelper()

