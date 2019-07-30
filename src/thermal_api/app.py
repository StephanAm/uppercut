from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import os
import socket
import uppercut.sharedvars as sharedvars
import uppercut.environment as environment

getVar = environment.getVar

# Connect to Redis
redishost = getVar('REDIS_HOST','localhost')
TempControl = sharedvars.SharedVarStore('TempControl')

class const(object):
    temp='temperature'
    isOn='isOn'
    setTemp='setTemperature'
    elementOn='elementOn'

app = Flask(__name__)
CORS(app)
api = Api(app)

class SetPoint(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(const.setTemp,type=int,help='required temperature in degrees Celcius')
    def get(self):
        setpoint = TempControl.get(const.setTemp)
        return {
            const.setTemp:setpoint
            }
    def post(self):
        args = self.parser.parse_args()
        setpoint = args[const.setTemp]
        TempControl.set(const.setTemp,setpoint)
        return {
            const.setTemp:setpoint
            }
class Status(Resource):
    def get(self):

        result = {
            const.isOn: TempControl.get(const.isOn),
            const.elementOn:  TempControl.get(const.elementOn),
            const.temp:TempControl.get(const.temp),
            const.setTemp:TempControl.get(const.setTemp)
            }
        return result

class IsOn(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(const.isOn,type=bool,help='value indicates whether control should be switched on or off')
    def get(self):
        return {
            const.isOn: TempControl.get(const.isOn)
            }
    def post(self):
        args = self.parser.parse_args()
        isOn = bool(args[const.isOn])
        TempControl.set(const.isOn,isOn)
        return {
            const.isOn: isOn
            }
            
api.add_resource(SetPoint,'/setpoint')
api.add_resource(Status,'/status')
api.add_resource(IsOn,'/ison')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
