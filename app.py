import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user

# load environment variables from .env file
load_dotenv()

# run flask app
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# run database and import database models
db = SQLAlchemy(app)
db.init_app(app)
from models import User, Competition

# run login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

@app.route('/')
def index():

    return 'Welcome to fit-comp API.'

@app.route('/profile')
def profile():

    return 'You are logged in as {}'.format(current_user.name)

@app.route('/login')
def login():

    return 'Login route.'

@app.route('/login', methods=['POST'])
def login_post():
    req = request.json
    email = req['email']
    password = req['password']

    # check if user exists and password hashes match
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):

        return 'Please check your login details and try again.'

    # otherwise create new user
    login_user(user)

    return 'Hello {}'.format(user.name)

@app.route('/signup')
def signup():

    return 'Signup route.'

@app.route('/signup', methods=['POST'])
def signup_post():
    req = request.json
    email = req['email']
    name = req['name']
    password = req['password']

    # check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:

        return 'User with id {} already exists'.format(user.id)

    # otherwise create new user
    new_user = User(email=email, name=name, 
        password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return 'User with id {} created'.format(new_user.id)

@app.route('/new', methods=['POST'])
@login_required
def add_comp():
    req = request.json
    type = req['type']
    start_date = req['start_date']
    end_date = req['end_date']

    try:
        comp = Competition(
            type = type,
            start_date = start_date,
            end_date = end_date
        )
        db.session.add(comp)
        db.session.commit()

        return 'Competition created (id={})'.format(comp.id)
    except Exception as e:

        return str(e)

@app.route('/get/<id_>', methods=['GET'])
@login_required
def get_comp(id_):
    try:
        comp=Competition.query.filter_by(id=id_).first()

        return jsonify(comp.serialize())
    except Exception as e:

        return str(e)

if __name__ == '__main__':
    app.run()
