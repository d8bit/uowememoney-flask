from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    email = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode, unique=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.password = password

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name
                }

