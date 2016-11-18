from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from User import User
from Expense import Expense

from datetime import datetime

# import hashlib
import bcrypt
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/money'
db = SQLAlchemy()


@app.route("/")
def index():
    return 'Flask roolz'

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # password = hashlib.new('sha1', password)
    # password = password.hexdigest()
    salt = bcrypt.gensalt()
    salt = '5SYhnwwHt3vwilmLAYNqA92bGtvoCfVU9cAdCyru0I4='
    salt = base64.b64encode(salt)
    return salt
    hash = bcrypt.hashpw('test', salt)
    return hash
    user = User.query.filter_by(email=request.form['email'], password=password).first();
    if None != user:
        return user.name

    return 'User not found'

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


db.init_app(app)
if __name__ == "__main__":
    app.run(debug = True)
