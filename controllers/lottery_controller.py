from flask import jsonify
from flask import request
from flask_restful import Resource
from classes.lottery import Lottery


class LotteryController(Resource):

    def get(self, action, lottery_id):

        if action == 'get':
            pass

        if action == 'make_draw':
            lottery = Lottery.get(lottery_id)
            if lottery is None:
                return 'Lottery doesn\'t exists'
            next_lottery = lottery.handle_lottery_draw()
            return 'Numbers have been successfully drawn, winners has been selected, ' \
                   'next lottery will be drawn on {}'.format(next_lottery.lottery_date)

    def post(self, action, lottery_id):

        if action == 'create':
            lottery = Lottery.create(**request.json)
            return jsonify(lottery.__dict__)
