from flask import jsonify
from flask import request
from flask_restful import Resource
from classes.ticket import Ticket


class TicketController(Resource):

    def get(self, action, ticket_id):

        if action == 'get_all':
            return jsonify(Ticket.get_all(ticket_id))

    def post(self, action, ticket_id):

        if action == 'create':
            ticket = Ticket.create(**request.json)
            return jsonify(ticket.__dict__)
