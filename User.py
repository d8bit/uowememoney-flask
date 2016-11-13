from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    email = db.Column(db.Unicode, unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name
                }

