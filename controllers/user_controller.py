from flask import request, session
from flask_restful import Resource

from classes.user import User


class UserController(Resource):

    def get(self, action, user_id):

        if action == 'get':
            user = User.get(user_id)
            if user is None:
                return 'User doesn\'t exists', 500
            return user.__dict__

        if action == 'get_all':
            pass

    def post(self, action, user_id):

        if action == 'create':
            
            user = User.create(**request.json)
            return user.__dict__
