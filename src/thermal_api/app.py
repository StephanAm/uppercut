from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import socket
from uppercut import sharedvars
from uppercut import environment
getVar = environment.getVar
SharedVars = sharedvars.SharedVars

# Connect to Redis
redishost = getVar('REDIS_HOST','localhost')
redis = SharedVars('sousvide/thermo/', host=redishost, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
CORS(app)
api = Api(app)

class SetPoint(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('setpoint',type=int,help='required temperature in degrees Celcius')
    def get(self):
        setpoint = redis.get('setpoint')
        return {
            'setpoint':setpoint
            }
    def post(self):
        args = self.parser.parse_args()
        setpoint = args['setpoint']
        redis.set('setpoint',setpoint)
        return {
            'setpoint':setpoint
            }
class Status(Resource):
    def get(self):
        result = {
            'isOn': redis.get('ison'),
            'elementOn':  redis.get('elementOn'),
            'currentTemp':redis.get("currentTemp"),
            'setPoint':redis.get('setpoint')
            }
        return result

class IsOn(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('isOn',type=bool,help='value indicates whether control should be switched on or off')
    def get(self):
        return {
            'isOn': redis.get('ison')
            }
    def post(self):
        args = self.parser.parse_args()
        isOn = bool(args['isOn'])
        redis.set('ison',isOn)
        return {
            'isOn': isOn
            }
api.add_resource(SetPoint,'/setpoint')
api.add_resource(Status,'/status')
api.add_resource(IsOn,'/ison')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
