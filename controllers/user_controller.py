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
            return User.get_all()

    def post(self, action, user_id):

        if action == 'create':
            user = User.create(**request.json)
            return user.__dict__

    def put(self, action, user_id):

        if action == 'update':
            user = User.get(user_id)
            if user is None:
                return 'User doesn\'t exists', 500
            user.update(**request.json)
            return 'User successfully updated'

    def delete(self, action, user_id):

        if action == 'set_inactive':
            user = User.get(user_id)
            if user is None:
                return 'User doesn\'t exists', 500
            user.set_inactive()
            return 'User successfully set inactive'
