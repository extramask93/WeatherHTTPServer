from Requests.LogOut import LogOut
from Requests.GetPeriodical import GetPeriodical
from Requests.RemoveStation import RemoveStation
from Requests.AddItem import AddItem
from Requests.GetStations import GetStations
from Requests.AddStation import AddStation
from Requests.ModifyStation import ModStation
from Requests.GetDaily import GetDaily
from Requests.CreateUser import CreateUser
from Requests.AuthenticateUser import AuthenticateUser
from flask import Flask
from flask_restful import Api
import logging

#setup logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key = "It ain't no secret"
api = Api(app)
api.add_resource(CreateUser, '/CreateUser')
api.add_resource(AuthenticateUser, '/LogIn')
api.add_resource(LogOut,'/LogOut')
api.add_resource(AddItem, '/AddItem')
api.add_resource(GetDaily, '/GetDaily')
api.add_resource(GetStations, '/GetStations')
api.add_resource(GetPeriodical,'/GetPeriodical')
api.add_resource(ModStation, '/ModStation')
api.add_resource(AddStation, '/AddStation')
api.add_resource(RemoveStation, '/RemoveStation')

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
