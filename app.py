import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User, Competition, InvalidUsage

@app.route('/')
def root():
    return 'Welcome to fit-comp'

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/users/add', endpoint='add-user')
def add_user():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    gender = request.args.get('gender')
    try:
        user = User(
            first_name = first_name,
            last_name = last_name,
            gender = gender
        )
        db.session.add(user)
        db.session.commit()
        return 'User added (id={})'.format(user.id)
    except Exception as e:
	    raise InvalidUsage(str(e), status_code=500)

@app.route('/users/remove/<id_>', endpoint='remove-user')
def remove_user(id_):
    try:
        user = User.query.filter_by(id=id_).one()
        db.session.delete(user)
        db.session.commit()
        return 'User removed (id={})'.format(user.id)
    except NoResultFound:
        raise InvalidUsage('User not found', status_code=404)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)

@app.route('/competitions/add', endpoint='add-comp')
def add_comp():
    type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    try:
        comp = Competition(
            type = type,
            start_date = start_date,
            end_date = end_date
        )
        db.session.add(comp)
        db.session.commit()
        return 'Competition added (id={})'.format(comp.id)
    except Exception as e:
	    raise InvalidUsage(str(e), status_code=500)

@app.route('/competitions/remove/<id_>', endpoint='remove-comp')
def remove_user(id_):
    try:
        comp = Competition.query.filter_by(id=id_).one()
        db.session.delete(comp)
        db.session.commit()
        return 'Competition removed (id={})'.format(comp.id)
    except NoResultFound:
        raise InvalidUsage('Competition not found', status_code=404)
    except Exception as e:
        raise InvalidUsage(str(e), status_code=500)


if __name__ == '__main__':
    app.run()
