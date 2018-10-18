from flask import jsonify
from flask import request
from flask_restful import Resource
from classes.lottery import Lottery


class LotteryController(Resource):

    def get(self, action, lottery_id):

        if action == 'get':
            pass

    def post(self, action, lottery_id):

        if action == 'create':
            lottery = Lottery.create(**request.json)
            return jsonify(lottery.__dict__)
