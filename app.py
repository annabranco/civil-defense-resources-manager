from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from config.setup import setup_db
from config.populate_db import db_drop_and_create_all
from config.models import Volunteer, Role, Group, Vehicle
import os

app = Flask(__name__)
setup_db(app)
CORS(app)

# --- Uncomment to re/set the db. ALL DATA WILL BE LOST!
# db_drop_and_create_all()

# --- ROUTES

@app.route('/')
def ping():
    return 'Healthy'

@app.route('/anna')
def get_anna():
    db_anna = Volunteer.query.filter(Volunteer.name=='Anna').one_or_none()
    print(db_anna)
    anna = db_anna.info()
    print(anna)
    return jsonify({ 'volunteer': anna })

@app.route('/volunteers/<id>')
def get_volunteer(id):
    db_data = Volunteer.query.filter(Volunteer.id==id).one_or_none()
    data = db_data.info()
    return jsonify({ 'volunteer': data })

@app.route('/roles/<id>')
def get_role(id):
    db_data = Role.query.filter(Role.id==id).one_or_none()
    data = db_data.info()
    return jsonify({ 'Role': data })

@app.route('/groups/<id>')
def get_group(id):
    db_data = Group.query.filter(Group.id==id).one_or_none()
    data = db_data.info()
    return jsonify({ 'Group': data })

@app.route('/vehicles/<id>')
def get_vehicle(id):
    db_data = Vehicle.query.filter(Vehicle.id==id).one_or_none()
    data = db_data.fullData()
    return jsonify({ 'Vehicle': data })

if __name__ == '__main__':
    assert os.path.exists('.env')
    app.run(host='0.0.0.0', port=5000, debug=True if os.environ['FLASK_ENV'] == 'development' else False)