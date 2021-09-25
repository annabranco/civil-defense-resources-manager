from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from config.setup import setup_db
from config.populate_db import db_drop_and_create_all
from config.models import Volunteer, Role, Group, Vehicle
from config.config import DATE_FORMAT
from datetime import datetime
import os
import constants

app = Flask(__name__)
setup_db(app)
CORS(app)

# --- Uncomment to re/set the db. ALL DATA WILL BE LOST!
# db_drop_and_create_all()

# region CUSTOM ERRORS
class RequestError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return {
            "status": self.status,
            "message": self.message
        }
# endregion

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

# --- ROUTES


@app.route('/')
def ping():
    return ('', 204)

# region VOLUNTEERS
@app.route('/volunteers/')
@app.route('/volunteers')
def get_volunteers():
    db_data = Volunteer.query.all()
    data = [vol.info() for vol in db_data]
    return jsonify({
        'success': True,
        'volunteers': data
        })

@app.route('/volunteers/<int:id>', methods=['GET'])
def get_volunteer(id):
    db_data = Volunteer.query.filter(Volunteer.id==id).one_or_none()
    if db_data is None:
        raise RequestError(404, constants.ERROR_MESSAGES['vol_not_found'])

    data = db_data.info()
    return jsonify({
        'success': True,
        'volunteer': data
        })

@app.route('/volunteers', methods=['POST'])
def create_volunteer():
    try:
        body = request.get_json()
        if body is None:
            raise RequestError(400, constants.ERROR_MESSAGES['body_needed'])
        try:
            name = body['name']
            surnames = body['surnames']
            birthday = body['birthday']
            document = body['document']
            address = body['address']
            email = body['email']
            phone1 = body['phone1']
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

        phone2 = body.get('phone2')

        if any([
            type(name) != str,
            type(surnames) != str,
            type(document) != str,
            type(address) != str,
            type(email) != str,
            type(phone1) != int,
            (phone2 is not None and type(phone2) != int),
        ]):
            raise RequestError(400, constants.ERROR_MESSAGES['wrong_type'])

        try:
            datetime.strptime(birthday, DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['bad_date'])

        role = body.get('role')
        if role is None:
            role = 1
        else:
            try:
                Role.query.filter(Role.id==role).one()
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_role'])

        groups = body.get('groups')
        if groups is None:
            groups = [Group.query.filter(Group.id==7).one()]
        elif type(groups) == int:
            try:
                groups = [Group.query.filter(Group.id==groups).one()]
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_group'])
        else:
            all_groups = []
            if len(groups) > 5:
                raise RequestError(400, constants.ERROR_MESSAGES['max_groups'])
            try:
                for group in groups:
                    all_groups.append(Group.query.filter(Group.id==group).one())
                groups = all_groups
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_list'])

        new_volunteer = Volunteer(name = name,
            surnames = surnames,
            birthday = birthday,
            document = document,
            address = address,
            email = email,
            phone1 = phone1,
            phone2 = phone2,
            active = True,
            groups = groups,
            role = role
        )

        return jsonify({
            'success': True,
            'volunteer': new_volunteer.fullData()
            }), 201

    except RequestError as error:
        raise RequestError(error.status, error.message)
    except:
        abort(422)

@app.route('/volunteers/<id>', methods=['PATCH'])
def update_volunteer(id):
    try:
        body = request.get_json()
        if body is None:
            raise RequestError(400, constants.ERROR_MESSAGES['body_needed'])

        edited_volunteer = Volunteer.query.filter(Volunteer.id==id).one_or_none()
        if edited_volunteer is None:
            raise RequestError(404, constants.ERROR_MESSAGES['vol_not_found'])

        try:
            name = body['name']
            surnames = body['surnames']
            birthday = body['birthday']
            document = body['document']
            address = body['address']
            email = body['email']
            phone1 = body['phone1']
            phone2 = body.get('phone2')
            role = body['role']
            groups = body['groups']
            active = body['active']
            stringified_date_on_server = edited_volunteer.birthday.strftime(DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

        try:
            stringified_date_on_body = datetime.strptime(birthday, DATE_FORMAT).strftime(DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['bad_date'])

        if all([
            name == edited_volunteer.name,
            surnames == edited_volunteer.surnames,
            stringified_date_on_body == stringified_date_on_server,
            document == edited_volunteer.document,
            address == edited_volunteer.address,
            email == edited_volunteer.email,
            phone1 == edited_volunteer.phone1,
            active == edited_volunteer.active
        ]):
            return jsonify({
            'success': False,
            'message': constants.ERROR_MESSAGES['no_change']
            }), 200

        if any([
            type(name) != str,
            type(surnames) != str,
            type(document) != str,
            type(address) != str,
            type(email) != str,
            type(phone1) != int,
            type(active) != bool,
            (phone2 is not None and type(phone2) != int),
        ]):
            raise RequestError(400, constants.ERROR_MESSAGES['wrong_type'])

        try:
            Role.query.filter(Role.id==role).one()
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['invalid_role'])

        if type(groups) == int:
            try:
                groups = [Group.query.filter(Group.id==groups).one()]
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_group'])
        else:
            all_groups = []
            if len(groups) > 5:
                raise RequestError(400, constants.ERROR_MESSAGES['max_groups'])
            try:
                for group in groups:
                    all_groups.append(Group.query.filter(Group.id==group).one())
                groups = all_groups
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_list'])

        edited_volunteer = Volunteer(
            name = name,
            surnames = surnames,
            birthday = birthday,
            document = document,
            address = address,
            email = email,
            phone1 = phone1,
            phone2 = phone2,
            active = active,
            groups = groups,
            role = role
        )

        return jsonify({
            'success': True,
            'volunteer': edited_volunteer.fullData()
            })
    except RequestError as error:
        raise RequestError(error.status, error.message)
    except:
        abort(422)

@app.route('/volunteers/<int:id>', methods=['DELETE'])
def delete_volunteer(id):
    db_data = Volunteer.query.filter(Volunteer.id==id).one_or_none()
    if db_data is None:
        raise RequestError(404, constants.ERROR_MESSAGES['vol_not_found'])
    return ('', 204)

# endregion

# region ROLES
@app.route('/roles/')
@app.route('/roles')
def get_roles():
    db_data = Role.query.all()
    data = [gr.info() for gr in db_data]
    return jsonify({
        'success': True,
        'roles': data
        })

@app.route('/roles/<int:id>')
def get_role(id):
    db_data = Role.query.filter(Role.id==id).one_or_none()
    if db_data is None:
        raise RequestError(404, constants.ERROR_MESSAGES['rol_not_found'])
    data = db_data.info()
    return jsonify({
        'success': True,
        'role': data
        })
# endregion

# region GROUPS
@app.route('/groups/')
@app.route('/groups')
def get_groups():
    db_data = Group.query.all()
    data = [gr.info() for gr in db_data]
    return jsonify({
        'success': True,
        'groups': data
        })

@app.route('/groups/<int:id>')
def get_group(id):
    db_data = Group.query.filter(Group.id==id).one_or_none()
    if db_data is None:
        raise RequestError(404, constants.ERROR_MESSAGES['gr_not_found'])
    data = db_data.info()
    return jsonify({
        'success': True,
        'group': data
    })
# endregion

# region VEHICLES
@app.route('/vehicles/')
@app.route('/vehicles')
def get_vehicles():
    db_data = Vehicle.query.all()
    data = [veh.info() for veh in db_data]
    return jsonify({
        'success': True,
        'vehicles': data
        })

@app.route('/vehicles/<int:id>')
def get_vehicle(id):
    db_data = Vehicle.query.filter(Vehicle.id==id).one_or_none()
    if db_data is None:
        raise RequestError(404, constants.ERROR_MESSAGES['veh_not_found'])

    data = db_data.info()
    return jsonify({
        'success': True,
        'Vehicle': data
        })

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    try:
        body = request.get_json()
        if body is None:
            raise RequestError(400, constants.ERROR_MESSAGES['body_needed'])
        try:
            name = body['name']
            brand = body['brand']
            license_num = body['license']
            year = body['year']
            next_itv = body['next_itv']
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

        if any([
            type(name) != str,
            type(brand) != str,
            type(license_num) != str,
            type(year) != int,
        ]):
            raise RequestError(400, constants.ERROR_MESSAGES['wrong_type'])

        try:
            datetime.strptime(next_itv, DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['bad_date'])

        incidents = body.get('incidents')

        new_vehicle = Vehicle(
            name = name,
            brand = brand,
            license = license_num,
            year = year,
            next_itv = next_itv,
            incidents = incidents,
            active = True,
        )

        return jsonify({
            'success': True,
            'volunteer': new_vehicle.fullData()
            }), 201

    except RequestError as error:
        raise RequestError(error.status, error.message)
    except:
        abort(422)

@app.route('/vehicles/<id>', methods=['PATCH'])
def update_vehicle(id):
    try:
        body = request.get_json()
        if body is None:
            raise RequestError(400, constants.ERROR_MESSAGES['body_needed'])

        edited_vehicle = Vehicle.query.filter(Vehicle.id==id).one_or_none()
        if edited_vehicle is None:
            raise RequestError(404, constants.ERROR_MESSAGES['veh_not_found'])

        try:
            name = body['name']
            brand = body['brand']
            license_num = body['license']
            year = body['year']
            next_itv = body['next_itv']
            incidents = body.get('incidents')
            active = body['active']
            stringified_date_on_server = edited_vehicle.next_itv.strftime(DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

        try:
            stringified_date_on_body = datetime.strptime(next_itv, DATE_FORMAT).strftime(DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['bad_date'])
        print('here')

        if all([
            name == edited_vehicle.name,
            brand == edited_vehicle.brand,
            incidents == edited_vehicle.incidents,
            stringified_date_on_body == stringified_date_on_server,
            license_num == edited_vehicle.license,
            year == edited_vehicle.year,
            active == edited_vehicle.active
        ]):
            return jsonify({
            'success': False,
            'message': constants.ERROR_MESSAGES['no_change']
            }), 200

        if any([
            type(name) != str,
            type(brand) != str,
            type(license_num) != str,
            type(year) != int,
            type(active) != bool,
            (incidents is not None and type(incidents) != str),

        ]):
            raise RequestError(400, constants.ERROR_MESSAGES['wrong_type'])
        try:
            datetime.strptime(next_itv, DATE_FORMAT)
        except:
            raise RequestError(400, constants.ERROR_MESSAGES['bad_date'])


        new_vehicle = Vehicle(
            name = name,
            brand = brand,
            license = license_num,
            year = year,
            next_itv = next_itv,
            incidents = incidents,
            active = active,
        )

        return jsonify({
            'success': True,
            'volunteer': new_vehicle.fullData()
            })

    except RequestError as error:
        raise RequestError(error.status, error.message)
    except:
        abort(422)

@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    db_data = Vehicle.query.filter(Vehicle.id==id).one_or_none()
    if db_data is None:
        raise RequestError(404, constants.ERROR_MESSAGES['veh_not_found'])
    return ('', 204)
# endregion

# region ERRORS HANDLING
@app.errorhandler(RequestError)
def custom_bad_request(error):
    return jsonify({
        'success': False,
        'error_code': error.status,
        'error': constants.HTTP_RESPONSES[error.status],
        'message': error.message
    }), error.status

@app.errorhandler(AuthError)
def authorization_error(error):
    error_details = error.to_json()

    return jsonify({
        'success': False,
        'error_code': error_details['details']['code'],
        'error': error_details['details']['error'],
        'message': error_details['details']['description'],
    }), error_details['status']

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
    'success': False,
    'error_code': 400,
    'error': 'Bad Request',
    'message': 'Your request is incorrect and cannot be processed. Please double check it.'
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
    'success': False,
    'error_code': 404,
    'error': 'Not Found',
    'message': 'Resource not found on database.'
    }), 404

@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
    'success': False,
    'error_code': 405,
    'error': 'Method not Allowed',
    'message': 'Are you handling the correct endpoint?'
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
    'success': False,
    'error_code': 422,
    'error': 'Unprocessable Entity',
    'message': 'Your request could not be processed. Are you sure your request is correct?'
    }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
    'success': False,
    'error_code': 500,
    'error': 'Server Error',
    'message': 'That\'s very embarassing, but something has failed on the backend... :('
    }), 500
# endregion

if __name__ == '__main__':
    app.run()