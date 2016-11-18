from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), primary_key=True)
    amount = db.Column(db.Float, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    paid_by = db.Column(db.Integer, primary_key=True)
    shared = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, primary_key=True)
    modified_by = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, primary_key=True)
    updated_at = db.Column(db.Date, primary_key=True)

    def __init__(self, name, amount, paid_by):
        self.name = name
        self.amount = amount
        self.paid_by = paid_by

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'amount': float(self.amount),
                'date': self.date,
                'paid_by': self.paid_by,
                'shared': self.shared,
                'created_by': self.created_by,
                'modified_by': self.modified_by,
                'created_at': self.created_at,
                'updated_at': self.updated_at
                }

