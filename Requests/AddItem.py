from flask import session
from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
from Requests.LoginRequired import LoginRequired

class AddItem(Resource):
    @LoginRequired
    def post(self):
        try:
            _stationID = str(request.form['stationID'])
            _temperature = str(request.form['temperature'])
            _humidity = str(request.form['humidity'])
            _lux = str(request.form['lux'])
            _soil = str(request.form['soil'])
            _co2 = str(request.form['co2'])
            _battery = str(request.form['battery'])
        except KeyError:
            return {'message':'There are missing arguments in the request.'},400
        try:
            db = DatabaseUtility()
            db.ChangeDatabase(session['username'])
            db.RunCommand("INSERT INTO measurements (StationID,temperature,humidity,lux,soil,co2,battery)"
                          " VALUES ((%s), (%s), (%s), (%s), (%s), (%s), (%s))",
                          (_stationID,_temperature,_humidity,_lux,_soil,_co2,_battery))
            return {'message': 'OK'}, 200
        except DBException as e:
            return {'message': e.msg},400
        except Exception:
            return {'message': 'Internal server error'},500
