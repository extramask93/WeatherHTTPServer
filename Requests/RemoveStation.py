from flask import session
from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
from Requests.LoginRequired import LoginRequired

class RemoveStation(Resource):
    @LoginRequired
    def post(self):
        try:
            _stationID = request.form['StationID']
        except KeyError as e:
            return {'message': 'There are missing arguments in the request.'}, 400
        try:
            db = DatabaseUtility()
            db.ChangeDatabase(session['username'])
            db.RunCommand("DELETE FROM measurements where StationID = %s", (_stationID,))
            db.RunCommand("DELETE FROM stations WHERE StationID = (%s)", (_stationID,))
            return {'message': 'OK'}, 200
        except DBException as e:
            return {'message': e.msg}, 400
        except Exception:
            return {'message': 'Internal server error'},500