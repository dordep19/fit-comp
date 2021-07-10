from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    name = db.Column(db.String())

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'email': self.email,
            'password': self.password,
            'name': self.name
        }

class Data(db.Model):
    __tablename__ = 'data'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    date = db.Column(db.Date(), primary_key=True)
    steps = db.Column(db.Integer())
    calories = db.Column(db.Integer())
    distance = db.Column(db.Integer())
    weight = db.Column(db.Integer())

    def __init__(self, user_id, date, steps, calories, distance, weight):
        self.user_id = user_id
        self.date = date
        self.steps = steps
        self.calories = calories
        self.distance = distance
        self.weight = weight

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'user_id': self.user_id, 
            'date': self.date,
            'steps': self.steps,
            'calories': self.calories,
            'distance': self.distance,
            'weight': self.weight
        }

class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())

    def __init__(self, type, start_date, end_date):
        self.type = type
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'type': self.type,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

class assignments(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    comp_id = db.Column(db.Integer(), db.ForeignKey('competitions.id'))
    admin = db.Column(db.Boolean())

    def __init__(self, user_id, comp_id, admin):
        self.user_id = user_id
        self.comp_id = comp_id
        self.admin = admin

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'user_id': self.user_id,
            'comp_id': self.comp_id,
            'admin': self.admin
        }
