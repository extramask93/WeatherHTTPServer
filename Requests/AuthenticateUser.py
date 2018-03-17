from flask import session
from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException

class AuthenticateUser(Resource):
    def post(self):
        try:
            _userEmail = request.form['email']
            _userPassword = request.form['password']
        except KeyError:
            return {'message': 'There are missing arguments in the request.'}, 400
        try:
            db = DatabaseUtility()
            db.ChangeDatabase('dbUsers')
            data = db.RunCommand("SELECT * FROM users WHERE Email = %s",(_userEmail,))
        except DBException as e:
            return {'message': e.msg}, 400
        try:
            if(_userPassword == str(data[0][3])):
                session['logged_in'] = True
                session['username'] = str(data[0][1])
                return {'message':'OK'},200
        except:
            pass
        finally:
            return {'message': 'Wrong username or password'}, 400