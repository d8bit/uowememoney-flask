from flask import Flask, jsonify, request, abort, session
from flask_sqlalchemy import SQLAlchemy

from User import User
from Expense import Expense

from datetime import datetime
import bcrypt


app = Flask(__name__)
app.secret_key = '$2a$12$5WzlzoUaY0kO2Z2WWKeXe.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/money'
db = SQLAlchemy()

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=request.form['email']).first()
    if None != user:
        hash = bcrypt.hashpw(password, user.password)
        if hash == user.password:
            user.remember_token = bcrypt.gensalt()
            db.session.commit()
            response = user.serialize()
            return jsonify(response)

    return 'Unauthorized', 401

@app.route('/logout')
def logout():
    token = request.headers.get('token')
    user = User.query.filter_by(remember_token=token).first()
    if None != user:
        user.remember_token = ''
        db.session.commit()
        return ''

    return 'Unauthorized', 401

@app.route("/users")
def users_list():
    if not authorized():
        return 'Unauthorized', 401
    users = User.query.all()
    response = []
    for user in users:
        response.append(user.serialize())

    return jsonify(response)

@app.route("/expenses", methods=['GET', 'POST'])
def expenses():
    if not authorized():
        return 'Unauthorized', 401
    if 'POST' == request.method:
        response = new_expense(request)

    if 'GET' == request.method:
        response = list_expenses()

    return jsonify(response)

def list_expenses():
    expenses = Expense.query.all()
    response = []
    for expense in expenses:
        response.append(expense.serialize())

    return response

def new_expense(request):
    for (key, value) in request.form.items():
        if "" == value:
            return 'Empty value for %s' % (key)

    expense = Expense(request.form['name'], request.form['amount'], request.form['paid_by'])
    current_date = datetime.now()
    expense.created_at = current_date.strftime('%Y-%m-%d %H:%M:%S')

    expense.created_by = request.form['created_by']
    expense.modified_by = request.form['created_by']
    expense.date = request.form['date']
    expense.shared = request.form['shared']

    db.session.add(expense)
    db.session.commit()

    return ''

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
