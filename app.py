from flask import Flask, jsonify, request, abort, session
from flask_sqlalchemy import SQLAlchemy

from User import User
from Expense import Expense
from Middleware import Middleware

from datetime import datetime
import bcrypt


app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)
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
            session['username'] = user.email
            response = user.serialize()
            return jsonify(response)

    abort(401)

@app.route('/logout/<int:user_id>')
def logout(user_id):
    user = User.query.filter_by(id=user_id).first()
    if None != user:
        if 'username' in session:
            session.pop('username', None)
            return ''
    abort(401)

@app.route("/users")
def users_list():
    users = User.query.all()
    response = []
    for user in users:
        response.append(user.serialize())

    return jsonify(response)

@app.route("/expenses", methods=['GET', 'POST'])
def expenses():
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

    return 'done'

@app.errorhandler(404)
def page_not_found(error):
    return 'Page not found', 404

def userLoggedIn():
    if 'username' in session:
        return True
    return False

db.init_app(app)
if __name__ == "__main__":
    app.run(debug = True)
