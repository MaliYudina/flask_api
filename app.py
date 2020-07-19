"""
App module runs the main logic of flask api
"""
import argparse
import logging
from logging.config import fileConfig

from flask import Flask, jsonify, request

log = logging.getLogger('werkzeug')  # to exclude flask internal logs
app = Flask(__name__)
fileConfig('log_config.cfg')


@app.errorhandler(404)
def not_found_error(error):
    """Function to handle the wrong url path or non-existing page"""
    app.logger.error(f'{request.method} method for {request.url}, page not found')
    return jsonify(message='404. Sorry, we could not find the page'), 200


@app.errorhandler(405)
def prohibited_method_error(error):
    """Function to handle all the methods except GET method"""
    app.logger.error(f'{request.method} method for {request.url} is prohibited')
    return jsonify(message=f'{request.method} method is prohibited'), 200


@app.route('/api', methods=['GET'], provide_automatic_options=False)
def api_query():
    """Handling the main api path and children pathes with params"""
    if request.method != 'GET':
        app.logger.error(f'{request.method} method for {request.url} is prohibited')
    else:
        app.logger.info(f'{request.method} method for {request.url}, params: "{request.query_string.decode("utf-8")}"')
        try:
            if 'invalid' in request.args and request.args['invalid'] == '1':
                raise Exception('Parameter "invalid=1"')
            process1(request.args)
            process2(request.args)
            process3(request.args)
            return jsonify(message=f'main page for api'), 200
        except Exception as e:
            app.logger.error(f'Error params: "{request.query_string.decode("utf-8")}" for {request.base_url}')
            return e.__str__()


def process1(args):
    """Method stub for some process #1"""
    app.logger.info('Process 1 is being performed')


def process2(args):
    """Method stub for some process #2"""
    app.logger.info('Process 2 is being performed')
    if 'notawaiting' in args and args['notawaiting'] == '1':
        raise Exception('Parameter "notawaiting=1"')


def process3(args):
    """"Method stub for some process #3"""
    app.logger.info('Process 3 is being performed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", help="please define the port (i.e. 8001)", required=False, default=5000)
    args = parser.parse_args()
    app.run(port=args.port, debug=True)
