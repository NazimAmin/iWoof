#!flask/bin/python
import logging
import os
import urlfetch
import urllib
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import json, xmltodict
from binascii import *
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
CORS(app)


@app.route('/')
def default():
    # simple get request
    try:
        #sms('14849290653', 'hey this is a test from pennapps')
        return status()
    except Exception as e:
        logging.info(e)
        abort(500)

@app.route('/sms') # sms example
def sms():
    params = {
        'api_key': 'c76e6310',
        'api_secret': 'e801a86852c6efd7',
        'to': '1484929####',
        'from': '1267405####',
        'text': 'try from pennapps'
    }
    url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)
    res = urlfetch.fetch(url, method='GET')
    return json.loads(res)

@app.route('/bark', methods=['GET']) # ['GET', 'POST']
def bark():
    # get request on url
    return status()

@app.route('/bark/<string:woof>', methods=['GET']) #woof is the payload
# you can also send as /bark/<type:woof>/<type:woof2>
# each of the woof is parameter of bark function bark(woof, woof1)
def barkwithwoof(woof=None):
    if woof is not None:
        return jsonify({'status': 'you send '+ woof})
    else:
        abort(404)

# we can use class
class Bark(Resource):
    def __init__(self):
        super(Bark, self).__init__()
    def get(self):
        ''' payload example:
        {
            "woof": 10
        }

        # or you can use get(self, woof)
        payload example would be
        /Bark/10
        '''
        try:
            input = request.get_json(force=True)
            # get the payload data you can also force check
            # that the correct payload is provided by
            #self.reqparse = reqparse.RequestParser()
            #self.reqparse.add_argument('key', type = str, required=True, help='you missed 'key'', location='json')
            #do something with input
            result = input * 100
            return result
        except Exception as e:
            abort(500)

    def post(self):
        pass
    def delete(self):
        pass


def status():
    return jsonify({'status': 'success'})
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify( { 'err': '500'} ), 500)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'err': '404' } ), 404)

api.add_resource(Bark, '/barking', endpoint='barking')
#api.add_resource(Bark,'/bark')
#api.add_resource(Bark,'/bark/<string:woof>') # if you decide to use get(self, woof)
#api.add_resource(Bark, '/bark', endpoint="barking") # you must specify endpoint if the path is same for multiple resource
if __name__ == '__main__':
    app.run(debug = True)
