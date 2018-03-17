from flask import session
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
from Requests.LoginRequired import LoginRequired
from flask import jsonify

class GetStations(Resource):
    @LoginRequired
    def get(self):
        try:
            db = DatabaseUtility()
            db.ChangeDatabase(session['username'])
            rows = db.RunCommand("select StationID,Name,refTime,temperature,humidity,"
                                 "lux,soil,battery,co2 from stations")
            a = []
            for row in rows:
                message={}
                message['StationID']=str(row[0])
                message['Name']=str(row[1])
                message['refTime'] = str(row[2])
                message['enableSettings'] = str(row[3])+str(row[4])+str(row[5])+str(row[6])\
                                            +str(row[7])+str(row[8])
                a.append(message)
            resp = jsonify({'stations': a})
            resp.status_code = 200
            return resp
        except DBException as e:
            return {'message': e.msg},400
        except Exception:
            return {'message', "Internal server error"},500