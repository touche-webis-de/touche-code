from datetime import datetime
import getopt
import json
import logging
import os
import sys
from typing import Dict
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from components.core.server_functions import setup, predict_argument

help_string = '\nUsage:  server.py [OPTIONS]' \
              '\n' \
              '\nRequest prediction of the BERT model for all test arguments' \
              '\n' \
              '\nOptions:' \
              '\n  -h, --help               Display help text' \
              '\n  -i, --internal_port int  Specifies the local port where the server listens' \
              '\n  -l, --log str            Log level, any of \'DEBUG\', \'INFO\', \'WARNING\', \'ERROR\'.' \
              '\n                           (default is \'INFO\')' \
              '\n  -p, --prefix_log str     Prefix string for log files (default is \'adam-smith\')' \
              '\n  -t, --threshold float    Ensemble threshold within [0.0; 1.0]'


######################################
# START OF: HTTP response server #####
######################################

def __handle_argument__(argument: str) -> Dict:
    if len(argument) > 0:
        try:
            result = predict_argument(argument=argument)
        except RuntimeError as e:
            logging.error(f'Exception during prediction for argument \'{argument}\':\n' + str(e))
            result = None
        if result is None or not isinstance(result, dict):
            result = {'Status': 'Internal error'}
    else:
        result = {'Status': 'Bad request'}

    return result


class AdamSmithServer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # for local development
        self.end_headers()

    def do_GET(self):
        logging.info(self.command)

        query = parse_qs(urlparse(self.path).query)
        argument_list = query.get('argument', None)

        argument = ""
        if argument_list is not None and len(argument_list) >= 1:
            argument = " ".join(argument_list)

        result = __handle_argument__(argument=argument)

        self._set_headers()
        response = json.dumps(result).encode('utf-8')
        self.wfile.write(response)

    def do_POST(self):
        logging.info(self.command)

        length = int(self.headers.get('content-length'))
        payload = self.rfile.read(length)
        argument = payload.decode('utf-8', errors='ignore')

        result = __handle_argument__(argument=argument)

        self._set_headers()
        response = json.dumps(result).encode('utf-8')
        self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        # Send allow-origin header for preflight POST XHRs.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()

    # silence console log messages
    def log_message(self, format, *args):
        pass


######################################
# END OF: HTTP response server #####
######################################


def run_server(internal_port: int = 8001):
    server_address = ('', internal_port)
    httpd = HTTPServer(server_address, AdamSmithServer)
    logging.info('serving at %s:%d' % (
        len(server_address[0]) > 0 and server_address[0] or 'localhost',
        server_address[1]
    ))
    # console output for safety
    print('[%s] serving at %s:%d' % (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        len(server_address[0]) > 0 and server_address[0] or 'localhost',
        server_address[1]
    ))
    httpd.serve_forever()


def __setup_logging__(log_file: str, loglevel: str):
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(message)s',
        filename=log_file,
        level=getattr(logging, loglevel.upper()),
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main(argv):
    internal_port = None
    threshold = None
    loglevel = 'INFO'
    log_filename_prefix = 'adam-smith'

    log_folder = '/app/logs'

    try:
        opts, args = getopt.gnu_getopt(argv, "hi:l:t:p:", ["help", "internal_port=", "log=", "threshold=", "prefix_log="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_string)
            sys.exit()
        elif opt in ('-i', '--internal_port'):
            try:
                internal_port = int(arg)
                if internal_port < 1:
                    raise ValueError
            except ValueError:
                print(f'Internal port has to be a positive integer. Got "{arg}" instead.')
                sys.exit(2)
        elif opt in ('-l', '--log'):
            numeric_level = getattr(logging, arg.upper(), None)
            if not isinstance(numeric_level, int):
                print(f'Unknown log level "{arg}". Using default level "{loglevel}".')
            else:
                loglevel = arg
        elif opt in ('-t', '--threshold'):
            try:
                threshold = float(arg)
                if threshold < 0.0 or threshold > 1.0:
                    raise ValueError
            except ValueError:
                print(f'Threshold is expected to be a float between 0 and 1. Got "{arg}" instead.')
                sys.exit(2)
        elif opt in ('-p', '--prefix_log'):
            log_filename_prefix = arg.replace('"', '').replace("'", '')

    if internal_port is None or threshold is None:
        print(help_string)
        sys.exit(2)

    # check logging setup
    if not os.path.isdir(log_folder):
        print(f'No logging folder provided to {log_folder}.')
        sys.exit(2)

    if len(log_filename_prefix) > 0 and not log_filename_prefix.endswith('_'):
        log_filename_prefix += '_'
    log_filename = log_filename_prefix + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'

    __setup_logging__(log_file=os.path.join(log_folder, log_filename), loglevel=loglevel)

    # start server functions
    try:
        setup(threshold=threshold)
    except BaseException as e:
        logging.error('Exception while starting server functions: ' + str(e))
        sys.exit(-1)

    # start server
    run_server(internal_port=internal_port)


if __name__ == '__main__':
    main(sys.argv[1:])
