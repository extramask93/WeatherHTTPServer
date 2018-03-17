from flask import session
from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
from Requests.LoginRequired import LoginRequired
from flask import jsonify

class GetDaily(Resource):
    @LoginRequired
    def get(self):
        try:
            dateStart = request.args.get('date1', default=None, type = str)
            dateEnd = request.args.get('date2', default=None, type=str)
            station = request.args.get('station',default='1', type=str)

            db = DatabaseUtility()
            db.ChangeDatabase(session['username'])
            if(dateEnd is None):
                rows = db.RunCommand("SELECT * from measurements WHERE measurementDate >= (%s) AND StationID = (%s)" ,
                                     (dateStart,station))
            else:
                rows = db.RunCommand("SELECT * from measurements WHERE measurementDate BETWEEN (%s) AND (%s) "
                                     "AND StationID = (%s)", (dateStart, dateEnd, station))
        except DBException as e:
            return {'message': e.msg}, 400
        try:
            a = []
            for row in rows:
                message={}
                message['StationID']=str(row[0])
                message['temperature']=str(row[1])
                message['humidity'] = str(row[2])
                message['lux'] = str(row[3])
                message['soil'] = str(row[4])
                message['co2'] = str(row[5])
                message['battery'] = str(row[6])
                message['measurementDate'] = str(row[7])
                a.append(message)
            resp = jsonify({'measurements': a})
            resp.status_code = 200
            return resp
        except:
            return {'message':'Internal serve error'},500