from datetime import datetime
import getopt
import json
import sys
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from components.core.server_functions import setup, predict_argument

help_string = '\nUsage:  server.py [OPTIONS]' \
              '\n' \
              '\nRequest prediction of the BERT model for all test arguments' \
              '\n' \
              '\nOptions:' \
              '\n  -h, --help              Display help text' \
              '\n  -i, --internal_port     Directory with \'arguments.tsv\' file' \
              '\n  -t, --threshold         Directory for writing the \'predictions.tsv\' file to'


# Adapted from https://gist.github.com/nitaku/10d0662536f37a087e1b
class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # for local development
        self.end_headers()

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        arguments = query.get('argument', None)

        if arguments is not None and len(arguments) == 1:
            argument = arguments[0]
            try:
                result = predict_argument(argument=argument)
            except RuntimeError as e:
                # log<w
                result = None
            if result is None:
                result = {'Status': 'Internal error'}
        else:
            result = {'Status': 'Bad request'}

        self._set_headers()
        response = json.dumps(result).encode('utf-8')
        self.wfile.write(response)

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        payload = self.rfile.read(length)
        message_string = payload.decode('utf-8', errors='ignore')

        if len(message_string) > 0:
            try:
                result = predict_argument(argument=message_string)
            except RuntimeError as e:
                # log
                result = None
            if result is None:
                result = {'Status': 'Internal error'}
        else:
            result = {'Status': 'Bad request'}

        print(result)
        print(type(result))

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


def run_server(internal_port: int = 8001, threshold: float = 0.27):
    print('Loading server functions...')
    try:
        setup(threshold=threshold, verbose=True)
    except BaseException as e:
        print(e)
        sys.exit(-1)

    server_address = ('', internal_port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('[%s] serving at %s:%d' % (
        datetime.now(),
        len(server_address[0]) > 0 and server_address[0] or 'internal',
        server_address[1]
    ))
    httpd.serve_forever()


def main(argv):
    internal_port = None
    threshold = None

    try:
        opts, args = getopt.gnu_getopt(argv, "hi:t:", ["help", "internal_port=", "threshold="])
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
        elif opt in ('-t', '--threshold'):
            try:
                threshold = float(arg)
                if threshold < 0.0 or threshold > 1.0:
                    raise ValueError
            except ValueError:
                print(f'Threshold is expected to be a float between 0 and 1. Got "{arg}" instead.')
                sys.exit(2)

    if internal_port is None or threshold is None:
        print(help_string)
        sys.exit(2)

    run_server(internal_port=internal_port, threshold=threshold)


if __name__ == '__main__':
    main(sys.argv[1:])
