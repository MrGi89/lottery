from flask import Flask
from flask_mysqldb import MySQL
from flask_restful import Api
from controllers.user_controller import UserController
from controllers.ticket_controller import TicketController
from controllers.lottery_controller import LotteryController


app = Flask(__name__)
api = Api(app)

app.secret_key = b'`eKYqPUAyTPov?(n?:@4ts14_&/'
mysql = MySQL(app)

api.add_resource(UserController, '/user/<action>/<user_id>')
api.add_resource(TicketController, '/ticket/<action>/<ticket_id>')
api.add_resource(LotteryController, '/lottery/<action>/<lottery_id>')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == '__main__':
    app.run(debug=True)
