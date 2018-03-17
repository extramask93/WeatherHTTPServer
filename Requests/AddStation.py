from flask import session
from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
from Requests.LoginRequired import LoginRequired

class AddStation(Resource):
    @LoginRequired
    def post(self):
        try:
            _stationID = request.form['StationID']
            _stationName = request.form['Name']
            _stationrefTime = request.form['refTime']
            _stationSettings = request.form['settings']
        except KeyError:
            return {'message': 'There are missing arguments in the request.'}, 400
        try:
            db = DatabaseUtility()
            db.ChangeDatabase(session['username'])
            rowCnt = db.RunCommand("SELECT EXISTS (SELECT 1 FROM stations WHERE StationID = %s)", (_stationID,))
            if(rowCnt[0][0] == 0):
                db.RunCommand("INSERT INTO stations (StationID, Name, refTime, temperature, humidity,"
                              " lux, soil, battery, co2) values ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))",
                           (_stationID, _stationName,_stationrefTime,_stationSettings[0],_stationSettings[1],
                            _stationSettings[2],_stationSettings[3],_stationSettings[4]
                            ,_stationSettings[5]))
                return {'message': 'OK'}, 200
            else:
                return {'message': 'Station already exist'}, 400
        except DBException as e:
            return {'message':e.msg},400
        except Exception:
            return {'message': 'Internal server error.'},500