import json, os, jsonify
from oslo_log import log
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_oslolog import OsloLog
from matilda_cost.api.controller import api_handler


app = Flask(__name__)
CORS(app)
LOG = OsloLog(app).logger


def prefix_route(route_function, prefix='', mask='{0}{1}'):
    '''
      Defines a new route function with a prefix.
      The mask argument is a `format string` formatted with, in that order:
        prefix, route
    '''
    def newroute(route, *args, **kwargs):
        '''New function to prefix the route'''
        return route_function(mask.format(prefix, route), *args, **kwargs)
    return newroute

#app.route = prefix_route(app.route, '/matilda/cost')

@app.route('/aws_ce', methods=['GET', 'POST'])
def post_json_handler():
    content = json.loads(request.data)
    account_name = request.args.get('account_name')
    resp = api_handler.cost_estimation(req_data=content, account_name=account_name)
    return jsonify(resp)


@app.route('/aws_ce/granularity', methods=['GET'])
def get_granularity():
    resp = api_handler.get_granularity()
    return jsonify(resp)


@app.route('/aws_ce/metrics', methods=['GET'])
def get_metrics():
    resp = api_handler.get_metrics()
    return jsonify(resp)


@app.route('/aws_ce/groupby', methods=['GET'])
def get_group_by():
    # sample http://192.168.20.156:8090/aws_ce/groupby?start=2018-07-10&end=2018-07-17
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    account_name = request.args.get('account_name')
    resp = api_handler.get_group_by(start_date, end_date, account_name)
    return jsonify(resp)


@app.route('/aws_ce/filter', methods=['GET'])
def get_filter():
    # http://192.168.20.156:8090/aws_ce/filter?start=2018-07-10&end=2018-07-17
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    account_name = request.args.get('account_name')
    resp = api_handler.get_filter(start_date, end_date, account_name)
    return jsonify(resp)

@app.route('/', methods=['GET'])
def matilda_cost():
    return 'Welcome to MATILDA COST MANAGEMENT COMPONENT'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6010, debug=True)
