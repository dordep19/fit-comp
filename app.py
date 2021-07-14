import os
from datetime import date, datetime
from sqlalchemy.orm import exc
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, json, request, jsonify, make_response
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
from models import User, Competition, Assignment, Data

# run login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

@app.route('/')
def index():
    rsp = {
        'timestamp': datetime.now(),
        'status': 200,
        'messsage': 'Welcome to fit-comp API!',
        'path': '/'
    }

    return jsonify(rsp)

@app.route('/profile')
def profile():
    rsp = {
        'timestamp': datetime.now(),
        'status': 200,
        'messsage': 'You are logged in as {}.'.format(current_user.name),
        'path': '/profile'
    }

    return jsonify(rsp)

@app.route('/login')
def login():
    rsp = {
        'timestamp': datetime.now(),
        'status': 200,
        'messsage': 'This is the login route.',
        'path': '/login'
    }

    return jsonify(rsp)

@app.route('/login', methods=['POST'])
def login_post():
    req = request.json
    email = req['email']
    password = req['password']

    try:
        # check if user exists and password hashes match
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            rsp = {
                'timestamp': datetime.now(),
                'status': 401,
                'error': 'Unauthorized',
                'messsage': 'Invalid username/password combination.',
                'path': '/login'
            }

            return jsonify(rsp)
        # otherwise create new user
        login_user(user)

        rsp = {
                'timestamp': datetime.now(),
                'status': 200,
                'messsage': 'Hello {}'.format(user.name),
                'path': '/login'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/create'
        }

        return jsonify(rsp)

@app.route('/signup')
def signup():
    rsp = {
        'timestamp': datetime.now(),
        'status': 200,
        'messsage': 'This is the signup route.',
        'path': '/signup'
    }

    return jsonify(rsp)

@app.route('/signup', methods=['POST'])
def signup_post():
    req = request.json
    email = req['email']
    name = req['name']
    password = req['password']

    try:
        # check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            rsp = {
                'timestamp': datetime.now(),
                'status': 409,
                'error': 'Conflict',
                'messsage': 'User with email {} already exists'.format(user.email),
                'path': '/signup'
            }

            return jsonify(rsp)
        # otherwise create new user
        new_user = User(email=email, name=name, 
            password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'messsage': 'User with email {} created'.format(new_user.email),
            'path': '/signup'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/signup'
        }

        return jsonify(rsp)

@app.route('/create', methods=['POST'])
@login_required
def create_comp():
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

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'messsage': 'Competition with id {} created'.format(comp.id),
            'path': '/create'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/create'
        }

        return jsonify(rsp)

@app.route('/upload', methods=['POST'])
@login_required
def upload_data():
    # check if data already entered
    data = Data.query.filter_by(user_id=current_user.id, 
        date=datetime.today().date()).first()
    if data:
        rsp = {
            'timestamp': datetime.now(),
            'status': 409,
            'error': 'Conflict',
            'messsage': 'Data already entered today',
            'path': '/upload'
        }

        return jsonify(rsp)
    # otherwise insert new data
    req = request.json
    user_id = current_user.id
    steps = req['steps']
    calories = req['calories']
    distance = req['distance']
    weight = req['weight']
    date = datetime.today().date()

    try:
        new_data = Data(
            user_id=user_id,
            steps = steps,
            calories = calories,
            distance = distance,
            weight = weight,
            date = date
        )
        db.session.add(new_data)
        db.session.commit()

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'messsage': 'Data entered on {}'.format(new_data.date),
            'path': '/upload'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/create'
        }

        return jsonify(rsp)

@app.route('/join', methods=['POST'])
@login_required
def join_comp():
    req = request.json
    comp_id = req['comp_id']
    admin = True if req['admin'] == 'True' else False

    try:    
        # check if user already enrolled in competition
        assignment = Assignment.query.filter_by(user_id=current_user.id, 
            comp_id=comp_id).first()
        if assignment:
            rsp = {
                'timestamp': datetime.now(),
                'status': 409,
                'error': 'Conflict',
                'messsage': 'User {} already enrolled in competition {}'.format(current_user.email, comp_id),
                'path': '/join'
            }

            return jsonify(rsp)
        # otherwise enroll user
        new_assignment = Assignment(user_id=current_user.id, comp_id=comp_id, admin=admin)
        db.session.add(new_assignment)
        db.session.commit()

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'messsage': 'User {} enrolled in competition {}'.format(new_assignment.id, 
                new_assignment.comp_id),
            'path': '/join'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/join'
        }

        return jsonify(rsp)

@app.route('/get_competitions', methods=['GET'])
@login_required
def get_comps():
    try:
        comps = Assignment.query.filter_by(user_id=current_user.id).all()

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'competitions': list(map(lambda comp: comp.serialize(), comps)),
            'path': '/get_competitions'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/get_competitions'
        }

        return jsonify(rsp)
   
@app.route('/get_info/<id_>', methods=['GET'])
@login_required
def get_info(id_):
    try:
        comp = Competition.query.filter_by(id=id_).first()

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'competition': comp.serialize(),
            'path': '/get_info/<id_>'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/get_info/<id_>'
        }

        return jsonify(rsp)

@app.route('/get_members/<id_>', methods=['GET'])
@login_required
def get_members(id_):
    try:
        members = Assignment.query.filter_by(comp_id=id_).all()

        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'members': list(map(lambda member: member.serialize(), members)),
            'path': '/get_members/<id_>'
        }

        return jsonify(rsp)
    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/get_members/<id_>'
        }

        return jsonify(rsp)

# parse database field name of chosen metric
def get_metric(metric):
    switcher = {
        'Distance': 'distance',
        'Calories': 'calories',
        'Steps': 'steps',
        'Weight': 'weight'
    }

    return switcher.get(metric, 'Invalid metric')

@app.route('/get_leaderboard/<id_>', methods=['GET'])
@login_required
def get_leaderboard(id_):
    try:
        comp = Competition.query.filter_by(id=id_).first()
        metric = get_metric(comp.type)
        start_date = comp.start_date
        end_date = comp.end_date
        leaderboard = {}

        # get all members participating in competition
        members = Assignment.query.filter_by(comp_id=id_).all()

        for member in members:
            # get data of each member for the duration of the competition
            data = Data.query.filter_by(user_id=member.user_id).filter(Data.date <= end_date, 
                Data.date >= start_date).all()
            data = list(map(lambda elem: elem.serialize(), data))

            # check if metric focuses on sum total
            if metric in ['distance', 'calories', 'steps']:
                total = 0

                for elem in data:
                    total += elem[metric]
                leaderboard[member.user_id] = total

            # otherwise it is weight loss
            else:
                # get the weight on the first day and latest day of competition
                start_weight = data[0]
                curr_weight = data[-1]

                # compute weight loss
                total = start_weight['weight'] - curr_weight['weight']
                leaderboard[member.user_id] = total

        # order user scores and generate rankings
        ordered = sorted(leaderboard, key=leaderboard.get, reverse=True)
        rankings = []
        rank = 1
        
        for user_id in ordered:
            rankings += [{'position': rank, 'user_id': user_id, 'score': leaderboard[user_id]}]
            rank += 1
        
        rsp = {
            'timestamp': datetime.now(),
            'status': 200,
            'leaderboard': rankings,
            'path': '/get_leaderboard/<id_>'
        }

        return jsonify(rsp)

    except Exception as e:
        rsp = {
            'timestamp': datetime.now(),
            'status': 500,
            'error': 'Internal Server Error',
            'messsage': str(e),
            'path': '/get_leaderboard/<id_>'
        }

        return jsonify(rsp)

if __name__ == '__main__':
    app.run()
