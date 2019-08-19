# -*- coding: utf-8 -*-

"""
Helper for papiweb_app.py
"""

import datetime, json, logging, os, pprint, time

import flask, requests
from papiweb_code.utils.connector import PatronAPI


log = logging.getLogger(__name__)


class PapiHelper( object ):
    """ Helper functions for app->handle_ezb_v1() """

    def __init__( self ):
        self.defaults = {
            'PATRON_API_URL_PATTERN': os.environ['papiweb__PATRON_API_URL_PATTERN'],
            }

    ## main functions (called by papiweb_app.py functions)

    def validate_request( self, params ):
        """ Checks params, ip, & auth info; returns boolean.
            Called by papiweb_app.handle_v1() """
        log.debug( 'starting validate..., params, `%s`' % params )
        validity = False
        keys_good = self.check_keys( params )
        ip_good = self.check_ip( flask.request.remote_addr )
        if keys_good and ip_good:
            validity = True
        log.debug( 'validity, `%s`' % validity )
        return validity

    def do_lookup( self, params ):
        """ Runs lookup; returns patron-api html output.
            Called by papiweb_app.handle_v1() """
        log.debug( "params['patron_barcode'], `%s`" % params['patron_barcode'] )
        cleaned_patron_barcode = self.clean_barcode( params['patron_barcode'] )
        log.debug( f'cleaned_patron_barcode, `{cleaned_patron_barcode}`' )
        papi = PatronAPI( self.defaults )
        log.debug( 'a' )
        try:
            papi_json = papi.grab_data( cleaned_patron_barcode )
            log.debug( 'b' )
            log.debug( 'papi_json, `%s`' % papi_json )
            log.debug( 'c' )
            jdct = json.loads( papi_json )
            log.debug( 'jdct, `%s`' % pprint.pformat(jdct) )
        except Exception as e:
            log.exception( 'exception on lookup; traceback follows; processing will continue...' )
            jdct = self.build_error_dict( e )
        return jdct

    def clean_barcode( self, initial_barcode ):
        """ Handles barcode with spaces. In separate function to be testable.
            Called by do_lookup() """
        log.debug( f'initial_barcode, `{initial_barcode}`' )
        cleaned_patron_barcode = initial_barcode.replace( ' ', '' )
        log.debug( f'cleaned_patron_barcode, `{cleaned_patron_barcode}`' )
        return cleaned_patron_barcode

    def build_response_dct( self, params, jdct ):
        """ Assembles request and response parts of the returned response.
            Called by papiweb_app.handle_v1() """
        request_dct = {
            'timestamp': str( datetime.datetime.now() ),
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
        log.debug( 'patron_barcode, `%s`' % patron_barcode )
        if len( patron_barcode ) > 5:
            keys_good = True
        log.debug( 'keys_good, `%s`' % keys_good )
        return keys_good

    def check_ip( self, perceived_ip ):
        """ Checks ip; returns boolean.
            Called by validate_request() """
        LEGIT_IPS = json.loads( os.environ['papiweb__LEGIT_IPS'] )
        ip_good = False
        if perceived_ip in LEGIT_IPS:
            ip_good = True
        else:
            log.debug( 'bad ip, `%s`' % flask.request.remote_addr )
        log.debug( 'ip_good, `%s`' % ip_good )
        return ip_good

    def build_error_dict( self, e ):
        """ Builds error dict.
            Called by self.do_lookup() """
        dct = { 'error': repr(e) }
        return dct

    # end class PapiHelper()

