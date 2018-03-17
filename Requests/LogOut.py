from flask import session
from flask_restful import Resource
import gc
from Requests.LoginRequired import LoginRequired


class LogOut(Resource):
    @LoginRequired
    def get(self):
        session.clear()
        gc.collect()
        return {'message':'Logged Out'},200