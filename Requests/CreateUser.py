from flask import request
from flask_restful import Resource
from DatabaseUtility import DatabaseUtility, DBException
import re

class CreateUser(Resource):
    def post(self):
        try:
            _userEmail = request.form['email']
            _userPassword = request.form['password']
            _userName = request.form['userName']
            _userPhone = request.form['phone']
        except KeyError :
            return {'message': 'There are missing arguments in the request.'}, 400

        if(re.search("^[^\\/\?\%\*:\|\"<>\.\s]{1,64}$",_userName) is None): #username should compromise to folder naming standard
            return {'message': "Username should consist only of letters and numbers"},400
        try:
            db = DatabaseUtility()
            db.ChangeDatabase('dbUsers')
            data = db.RunCommand("SELECT EXISTS (SELECT 1 FROM users WHERE Email = '{0}')".format(_userEmail))
            if(data[0][0] == 1):
                return {'message': 'Email already taken'},400
            data = db.RunCommand("SELECT EXISTS (SELECT 1 FROM users WHERE UserName = '{0}')".format(_userName))
            if(data[0][0] == 1):
                return {'message': 'Username already taken'},400
            db.RunCommand("INSERT INTO users (UserName,Email,Password,Phone) values (%s, %s, %s ,%s)",
                          (_userName,_userEmail,_userPassword,_userPhone))
            db.RunCommand("CREATE DATABASE {0}".format(_userName))
            db.ChangeDatabase(_userName)
            db.RunCommand("CREATE TABLE stations (StationID INT NOT NULL, Name varchar(45) NOT NULL, PRIMARY KEY(StationID))")
            db.RunCommand(("CREATE TABLE measurements (StationID INT NOT NULL, temperature DECIMAL(3,1), humidity DECIMAL(4,1), "
                               "lux SMALLINT UNSIGNED, soil DECIMAL(4,1), co2 SMALLINT UNSIGNED, battery DECIMAL(3,0), measurementDate "
                               "TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, FOREIGN KEY (StationID) REFERENCES stations(StationID))"))
            return {'message': 'OK'},200
        except DBException as e:
            return{'message': e.msg}, 400
        except:
            return {'message': "Internal server error"},500