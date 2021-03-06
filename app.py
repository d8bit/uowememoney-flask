import os
from flask import Flask, jsonify, request, abort, session
from flask_sqlalchemy import SQLAlchemy

from User import User
from Expense import Expense

from datetime import datetime
import bcrypt
import logging

# Needed to allow cross-origin requests
from flask_cors import CORS, cross_origin


# Database conection
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
CORS(app)
app.secret_key = os.environ["MONEY_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/money'
db = SQLAlchemy()

# Login
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if None != user:
        hash = bcrypt.hashpw(data['password'], user.password)
        if hash == user.password:
            user.remember_token = bcrypt.gensalt()
            db.session.commit()
            response = user.serialize()
            return jsonify(response), 200

        return 'Unauthorized', 401
    else:
        return '', 200


# Logout
@app.route('/logout')
def logout():
    token = request.headers.get('token')
    user = User.query.filter_by(remember_token=token).first()
    if None != user:
        user.remember_token = ''
        db.session.commit()
        return ''

    return 'Unauthorized', 401

# List users
@app.route("/users")
def users_list():
    if not authorized():
        return 'Unauthorized', 401
    users = User.query.all()
    response = []
    for user in users:
        response.append(user.serialize())

    return jsonify(response)

# Expenses
@app.route("/expenses", methods=['GET', 'POST'])
def expenses():
    if not authorized():
        return 'Unauthorized', 401
    if 'POST' == request.method:
        response = new_expense(request)

    if 'GET' == request.method:
        response = list_expenses()

    return jsonify(response)

# Get expenses from logged user
def list_expenses():
    expenses = Expense.query.all()
    response = []
    for expense in expenses:
        response.append(expense.serialize())

    return response

# Add new expense
def new_expense(request):
    # logging.getLogger('flask_cors').level = logging.DEBUG
    data = request.get_json()
    for (key, value) in data.items():
        print value
        if "" == value:
            return 'Empty value for %s' % (key)

    expense = Expense(data['name'], data['amount'], data['paid_by'])
    current_date = datetime.now()
    expense.created_at = current_date.strftime('%Y-%m-%d %H:%M:%S')

    expense.created_by = data['created_by']
    expense.modified_by = data['created_by']
    expense.date = data['date']
    expense.shared = data['shared']

    db.session.add(expense)
    db.session.commit()

    return ''

# Check logged in
def authorized():
    token = request.headers.get('token')
    user = User.query.filter_by(remember_token=token).first()
    if None != user:
        return True
    return False

@app.errorhandler(404)
def page_not_found(error):
    return 'Page not found', 404

db.init_app(app)
if __name__ == "__main__":
    app.run(debug = True)
