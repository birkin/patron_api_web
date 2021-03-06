# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

import flask
from flask import render_template
from flask_basicauth import BasicAuth
from papiweb_code.utils import log_config
from papiweb_code.utils.app_helper import PapiHelper



## setup
app = flask.Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ['papiweb__BASIC_AUTH_USERNAME']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['papiweb__BASIC_AUTH_PASSWORD']
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = os.environ['papiweb__SECRET_KEY']

basic_auth = BasicAuth( app )
papi_helper = PapiHelper()

log = log_config.setup_logger()

# LOG_PATH = os.environ['papiweb__LOG_PATH']
# logging.basicConfig(
#     filename=LOG_PATH,
#     level=logging.DEBUG,
#     format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
#     datefmt='%d/%b/%Y %H:%M:%S'
#     )
# log = logging.getLogger(__name__)
# log.debug( 'log setup' )


@app.route( '/', methods=['GET'] )  # /papiweb
def root_redirect():
    """ Redirects to readme. """
    log.debug( 'starting redirect' )
    return flask.redirect( 'https://github.com/birkin/patron_api_web/blob/master/README.md', code=303 )


@app.route( '/v1', methods=['GET'] )  # /papiweb/v1
@basic_auth.required
def handle_v1():
    """ Grabs barcode, performs lookup, & returns json results. """
    log.debug( 'starting grab' )
    if papi_helper.validate_request( flask.request.args ) == False:
        log.info( 'request invalid, returning 400' )
        flask.abort( 400 )  # `Bad Request`
    jdct = papi_helper.do_lookup( flask.request.args )
    log.debug( 'lib result dct, `%s`' % pprint.pformat(jdct) )
    return_dct = papi_helper.build_response_dct( flask.request.args, jdct )
    return flask.jsonify( return_dct )


if __name__ == '__main__':
    if os.getenv( 'DEVBOX' ) == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
