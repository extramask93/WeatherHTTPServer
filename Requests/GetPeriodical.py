from flask import session
from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
from Requests.LoginRequired import LoginRequired
from flask import jsonify

class GetPeriodical(Resource):
    @LoginRequired
    def get(self):
        try:
          period = request.args.get('period', default='week', type=str)
          type = request.args.get('type', default='temperature', type=str)
          station = request.args.get('station', default='1', type=str)
          nrOfintervals = request.args.get('interval', default='100', type=str)
          intervals = int(nrOfintervals)
        except:
            return {'message' : 'There are missing arguments in the request.'},400
        try:
            db = DatabaseUtility()
            db.ChangeDatabase(session['username'])
            dict = {'day': 1, 'week': 7, '3days': 3, 'month': 31, '3months': 93, 'year': 365}
            minmax = " select timestampdiff(second,min,max) div {0} as seconds from (select min(measurementDate) as min, max(measurementDate) as max" \
                     " from measurements where measurementDate > DATE_SUB(NOW(), INTERVAL {1} DAY) and StationID = {2}) as temp".format(nrOfintervals, dict[period],station)
            response = db.RunCommand(minmax)
            try:
                seconds = int(response[0][0])
            except:
                return {'measurements':[]}
            az = ("select StationID,avg({0}) as {0}, measurementDate from measurements"
                  " where measurementDate between date_sub(now(), interval {1} day) and now() and StationID={2}"
                  " group by measurementDate div {4},StationID").format(type, dict[period], station, nrOfintervals, seconds)
            ay = ("select count(StationID) from measurements where measurementDate between date_sub(now(), interval {0} day)"
                  " and now() and StationID = {1}").format(dict[period], station)
            nr = db.RunCommand(ay)
            if (int(nr[0][0]) <= int(nrOfintervals)):
                rows = db.RunCommand(("select StationID,{0},measurementDate from measurements where measurementDate"
                                      " between date_sub(now(), interval {1} day) and now() and StationID = {2}").format(type, dict[period], station))
            else:
                rows = db.RunCommand(az)
            a = []
            for row in rows:
                message = {}
                message['StationID'] = str(row[0])
                message[type] = str(row[1])
                message['time'] = str(row[2])
                a.append(message)
            resp = jsonify({'measurements': a})
            resp.status_code = 200
            return resp
        except DBException as e:
            return {'message': e.msg}, 400
        except Exception as e:
            return {'message': "Internal server error"}, 500
