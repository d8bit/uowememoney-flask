from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from User import User
from Expense import Expense

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/money'
db = SQLAlchemy()


@app.route("/")
def index():
    return 'Flask roolz'

@app.route("/users")
def users_list():
    users = User.query.all()
    response = []
    for user in users:
        response.append(user.serialize())

    return jsonify(response)

@app.route("/expenses")
def expenses():
    if 'POST' == request.method:
        response = new_expense()

    if 'GET' == request.method:
        response = list_expenses()

    return jsonify(response)

def list_expenses():
    expenses = Expense.query.all()
    response = []
    for expense in expenses:
        response.append(expense.serialize())

    return response

def new_expense():
    return 'yolo'


db.init_app(app)
if __name__ == "__main__":
    app.run(debug = True)
