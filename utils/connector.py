# -*- coding: utf-8 -*-

import json, logging, os, pprint, re
import requests


## log to console
LOG_PATH = os.environ['papiweb__LOG_PATH']
LOG_LEVEL = os.environ.get('papiweb__LOG_LEVEL')
level_dict = { 'debug': logging.DEBUG, 'info':logging.INFO }
logging.basicConfig(
    filename=LOG_PATH,
    level=level_dict[LOG_LEVEL],
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
    )
log = logging.getLogger(__name__)
log.debug( 'connector log setup' )


class PatronAPI( object ):
    """ Grabs & parses patron-api output. """

    def __init__( self, defaults ):
        self.url_pattern = defaults['PATRON_API_URL_PATTERN']
        log.debug( 'PatronAPI instantiated' )

    # def grab_data( self, barcode ):
    #     """ Grabs and parses patron-api html. """
    #     html = self.grab_raw_data( barcode )
    #     d = self.parse_data( html )
    #     output = json.dumps( d, sort_keys=True, indent=2 )
    #     return output

    def grab_data( self, barcode ):
        """ Grabs and parses patron-api html. """
        result_dct = self.grab_raw_data( barcode )
        if result_dct['status_code'] is not 200:
            d = { 'problem': f'status_code, `{result_dct["status_code"]}`; content, ```{result_dct["content"]}```; see logs for more info.' }
        else:
            d = self.parse_data( result_dct['content'] )
        output = json.dumps( d, sort_keys=True, indent=2 )
        return output

    def grab_raw_data( self, barcode ):
        """ Makes http request.
            Called by grab_data() """
        url = self.url_pattern.replace( 'BARCODE', barcode )
        log.debug( f'url, `{url}`' )
        r = requests.get( url )
        log.debug( f'type-status-code, `{type(r.status_code)}`' )
        return_dct = {
            'status_code': r.status_code, 'content': r.content }
        log.debug( f'return_dct, ```{pprint.pformat(return_dct)}```' )
        return return_dct

    # def grab_raw_data( self, barcode ):
    #     """ Makes http request.
    #         Called by grab_data() """
    #     url = self.url_pattern.replace( 'BARCODE', barcode )
    #     log.debug( 'url, `%s`' % url )
    #     r = requests.get( url )
    #     html = r.text
    #     log.debug( 'html, ```%s```' % html )
    #     return html

    def parse_data( self, html ):
        """ Converts html to dct.
            Called by grab_data() """
        lines = html.split( '\n' )
        trimmed_lines = self.trim_lines( lines )
        dct = {}
        for line in trimmed_lines:
            value_dct = self.parse_line( line )
            key = value_dct['label'].lower().replace( ' ', '_' )
            dct[key] = value_dct
        return_dct = self.add_conversions( dct )
        log.debug( 'return_dct, `%s`' % pprint.pformat(return_dct) )
        return dct

    def trim_lines( self, lines ):
        """ Trims and slices lines.
            Called by parse_data() """
        trimmed_lines = []
        sliced_lines = lines[1:-2]
        for line in sliced_lines:
            trimmed_lines.append( line.strip() )
        log.debug( 'trimmed_lines, `%s`' % pprint.pformat(trimmed_lines) )
        return trimmed_lines

    def parse_line( self, line ):
        """ Parses line into key and dct-value.
            Called by parse_data() """
        label = self.parse_label( line )
        updated_line = line[ len(label): ]
        log.debug( 'updated_line, `%s`' % updated_line )
        ( code, sliced_code ) = self.parse_code( updated_line )
        updated_line = updated_line[ len(code): ]
        log.debug( 'updated_line2, `%s`' % updated_line )
        value = self.parse_value( updated_line )
        dct = { 'label': label, 'code': sliced_code, 'value': value }
        log.debug( 'dct, `%s`' % pprint.pformat(dct) )
        return dct

    def parse_label( self, line ):
        """ Parses and returns label.
            Example: in line `PATRN NAME[pn]=Demolast, Demofirst<BR>`, returns 'PATRN NAME'.
            Called by parse_line() """
        regex_pattern = """
            [A-Z0-9]*     # label text
            \s*           # space
            \-*           # hyphen
            [A-Z0-9]*     # label text
            """
        label_result = re.search( regex_pattern, line, re.VERBOSE )
        label = label_result.group()
        log.debug( 'label, `%s`' % label )
        return label

    def parse_code( self, updated_line ):
        """ Parses and returns code.
            Example: in updated_line `[pn]=Demolast, Demofirst<BR>`, returns ('[pn]', pn').
            Called by parse_line() """
        regex_pattern = """
            (\[p)           # start
            [a-z0-9\!\^]*   # code
            (\])            # end
            """
        code_result = re.search( regex_pattern, updated_line, re.VERBOSE )
        code = code_result.group()
        sliced_code = code[1: -1]
        log.debug( 'code, `%s`; sliced_code, `%s`' % (code, sliced_code) )
        return ( code, sliced_code )

    def parse_value( self, updated_line ):
        """ Parses and returns value.
            Example: in updated_line `=Demolast, Demofirst<BR>`, returns 'Demolast, Demofirst'.
            Called by parse_line() """
        start = len( '=' )
        end = len( '<BR>' )
        value = updated_line[ start: -end ]
        log.debug( 'value, `%s`' % value )
        return value

    def add_conversions( self, dct ):
        """ Enhances barcode data.
            Called by parse_line() """
        start = dct['p_barcode']['value']
        converted_value = start.replace( ' ', '' )
        dct['p_barcode']['converted_value'] = converted_value
        log.debug( 'dct after conversions, `%s`' % pprint.pformat(dct) )
        return dct

    # end class PatronAPI
