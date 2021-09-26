from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from config.setup import setup_db
from config.populate_db import db_drop_and_create_all
from config.models import Group, Role, Service, Vehicle, Volunteer
from config.config import DATE_FORMAT, FULL_DATE_FORMAT
from datetime import datetime
import os
import constants

def create_app(test_config=None):
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
        return jsonify({
            'success': True,
            'message': "The server is up! :D"
            })

    # region VOLUNTEERS
    @app.route('/volunteers/')
    @app.route('/volunteers')
    def get_volunteers():
        db_data = Volunteer.query.all()
        data = [vol.fullData() for vol in db_data]
        return jsonify({
            'success': True,
            'volunteers': data
            })

    @app.route('/volunteers/<int:id>', methods=['GET'])
    def get_volunteer(id):
        db_data = Volunteer.query.filter(Volunteer.id==id).one_or_none()
        if db_data is None:
            raise RequestError(404, constants.ERROR_MESSAGES['vol_not_found'])

        data = db_data.fullData()
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
                phone1 = body['phone1']
                dummy_data = body.get('dummy_data')
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

            phone2 = body.get('phone2')
            email = body.get('email')

            if any([
                type(name) != str,
                type(surnames) != str,
                type(document) != str,
                type(address) != str,
                type(phone1) != int,
                (phone2 is not None and type(phone2) != int),
                (email is not None and type(email) != str),
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

            new_volunteer = Volunteer(
                name = name,
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

            if not dummy_data:
                new_volunteer.insert()

            return jsonify({
                'created': False if dummy_data else True,
                'volunteer': new_volunteer.fullData()
                }), 200 if dummy_data else 201

        except RequestError as error:
            raise RequestError(error.status, error.message)
        except:
            abort(422)

    @app.route('/volunteers/<id>', methods=['PATCH'])
    def update_volunteer(id):
        if int(id) <= 3:
            raise RequestError(403, constants.ERROR_MESSAGES['forbidden_upd'])
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
                active == edited_volunteer.active,
                groups == [gr.id for gr in edited_volunteer.groups],
                role == edited_volunteer.role,
                phone2 == edited_volunteer.phone2
            ]):
                return jsonify({
                'updated': False,
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

                edited_volunteer.name = name
                edited_volunteer.surnames = surnames
                edited_volunteer.birthday = birthday
                edited_volunteer.document = document
                edited_volunteer.address = address
                edited_volunteer.email = email
                edited_volunteer.phone1 = phone1
                edited_volunteer.phone2 = phone2
                edited_volunteer.active = active
                edited_volunteer.groups = groups
                edited_volunteer.role = role

            edited_volunteer.update()

            return jsonify({
                'updated': True,
                'volunteer': edited_volunteer.fullData()
                })
        except RequestError as error:
            raise RequestError(error.status, error.message)
        except:
            abort(422)

    @app.route('/volunteers/<int:id>', methods=['DELETE'])
    def delete_volunteer(id):
        if id <= 4:
            raise RequestError(403, constants.ERROR_MESSAGES['forbidden_del'])
        db_data = Volunteer.query.filter(Volunteer.id==id).one_or_none()

        if db_data is None:
            raise RequestError(404, constants.ERROR_MESSAGES['vol_not_found'])
        print(f'$$$ db_data {db_data}')

        db_data.delete()
        return ('', 204)

    # endregion

    # region ROLES
    @app.route('/roles/')
    @app.route('/roles')
    def get_roles():
        db_data = Role.query.all()
        data = [rol.info() for rol in db_data]
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
        data = [veh.fullData() for veh in db_data]
        return jsonify({
            'success': True,
            'vehicles': data
            })

    @app.route('/vehicles/<int:id>')
    def get_vehicle(id):
        db_data = Vehicle.query.filter(Vehicle.id==id).one_or_none()
        if db_data is None:
            raise RequestError(404, constants.ERROR_MESSAGES['veh_not_found'])

        data = db_data.fullData()
        return jsonify({
            'success': True,
            'vehicle': data
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

            new_vehicle.insert()

            return jsonify({
                'created': True,
                'vehicle': new_vehicle.fullData()
                }), 201

        except RequestError as error:
            raise RequestError(error.status, error.message)
        except:
            abort(422)

    @app.route('/vehicles/<id>', methods=['PATCH'])
    def update_vehicle(id):
        if int(id) == 1:
            raise RequestError(403, constants.ERROR_MESSAGES['forbidden_upd'])
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
                'updated': False,
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

            edited_vehicle.name = name
            edited_vehicle.brand = brand
            edited_vehicle.license = license_num
            edited_vehicle.year = year
            edited_vehicle.next_itv = next_itv
            edited_vehicle.incidents = incidents
            edited_vehicle.active = active

            edited_vehicle.update()

            return jsonify({
                'updated': True,
                'vehicle': edited_vehicle.fullData()
                })

        except RequestError as error:
            raise RequestError(error.status, error.message)
        except:
            abort(422)

    @app.route('/vehicles/<int:id>', methods=['DELETE'])
    def delete_vehicle(id):
        if id <= 2:
            raise RequestError(403, constants.ERROR_MESSAGES['forbidden_del'])
        db_data = Vehicle.query.filter(Vehicle.id==id).one_or_none()
        if db_data is None:
            raise RequestError(404, constants.ERROR_MESSAGES['veh_not_found'])
        db_data.delete()

        return ('', 204)
    # endregion


    # region SERVICES
    @app.route('/services/')
    @app.route('/services')
    def get_services():
        db_data = Service.query.all()
        data = [ser.fullData() for ser in db_data]
        return jsonify({
            'success': True,
            'services': data
            })

    @app.route('/services/<int:id>', methods=['GET'])
    def get_service(id):
        db_data = Service.query.filter(Service.id==id).one_or_none()
        if db_data is None:
            raise RequestError(404, constants.ERROR_MESSAGES['ser_not_found'])

        data = db_data.details()
        return jsonify({
            'success': True,
            'service': data
            })

    @app.route('/services', methods=['POST'])
    def create_service():
        try:
            body = request.get_json()
            if body is None:
                raise RequestError(400, constants.ERROR_MESSAGES['body_needed'])
            try:
                name = body['name']
                place = body['place']
                date = body['date']
                vehicles_num = body['vehicles_num']
                volunteers_num = body['volunteers_num']
                contact_name = body.get('contact_name')
                contact_phone = body.get('contact_phone')
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

            if any([
                type(name) != str,
                type(place) != str,
                type(vehicles_num) != int,
                type(volunteers_num) != int,
                (contact_name is not None and type(contact_name) != str),
                (contact_phone is not None and type(contact_phone) != int),
            ]):
                raise RequestError(400, constants.ERROR_MESSAGES['wrong_type'])

            try:
                datetime.strptime(date, FULL_DATE_FORMAT)
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['bad_full_date'])

            new_service = Service(
                name = name,
                place = place,
                date = date,
                vehicles_num = vehicles_num,
                volunteers_num = volunteers_num,
                contact_name = contact_name,
                contact_phone = contact_phone,
                vehicles = [],
                volunteers = [],
            )

            new_service.insert()

            return jsonify({
                'created': True,
                'service': new_service.fullData()
                }), 201

        except RequestError as error:
            raise RequestError(error.status, error.message)
        except:
            abort(422)

    @app.route('/services/<id>', methods=['PATCH'])
    def update_service(id):
        try:
            body = request.get_json()
            if body is None:
                raise RequestError(400, constants.ERROR_MESSAGES['body_needed'])

            edited_service = Service.query.filter(Service.id==id).one_or_none()
            if edited_service is None:
                raise RequestError(404, constants.ERROR_MESSAGES['ser_not_found'])

            print(f'$$$ edited_service.date {edited_service.date}')
            print(f'$$$ datetime.now() {datetime.now()}')
            print(f'$$$ edited_service.date < datetime.now() {edited_service.date < datetime.now()}')

            if edited_service.date < datetime.now():
                raise RequestError(403, constants.ERROR_MESSAGES['forbidden_date_upd'])

            try:
                name = body['name']
                place = body['place']
                date = body['date']
                vehicles_num = body['vehicles_num']
                volunteers_num = body['volunteers_num']
                vehicles = body['vehicles']
                volunteers = body['volunteers']
                contact_name = body.get('contact_name')
                contact_phone = body.get('contact_phone')
                stringified_date_on_server = edited_service.date.strftime(FULL_DATE_FORMAT)
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['missing_data'])

            try:
                stringified_date_on_body = datetime.strptime(date, FULL_DATE_FORMAT).strftime(FULL_DATE_FORMAT)
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['bad_full_date'])

            if all([
                name == edited_service.name,
                place == edited_service.place,
                stringified_date_on_body == stringified_date_on_server,
                vehicles_num == edited_service.vehicles_num,
                volunteers_num == edited_service.volunteers_num,
                contact_name == edited_service.contact_name,
                contact_phone == edited_service.contact_phone,
                vehicles == [veh.id for veh in edited_service.vehicles],
                volunteers == [vol.id for vol in edited_service.volunteers],
            ]):
                return jsonify({
                'updated': False,
                'message': constants.ERROR_MESSAGES['no_change']
                }), 200

            if any([
                type(name) != str,
                type(place) != str,
                type(vehicles_num) != int,
                type(volunteers_num) != int,
                (contact_name is not None and type(contact_name) != str),
                (contact_phone is not None and type(contact_phone) != int),
            ]):
                raise RequestError(400, constants.ERROR_MESSAGES['wrong_type'])

            all_volunteers = []
            try:
                for volunteer in volunteers:
                    all_volunteers.append(Volunteer.query.filter(Volunteer.id==volunteer).one())
                volunteers = all_volunteers
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_list'])

            all_vehicles = []
            try:
                for vehicle in vehicles:
                    all_vehicles.append(Vehicle.query.filter(Vehicle.id==vehicle).one())
                vehicles = all_vehicles
            except:
                raise RequestError(400, constants.ERROR_MESSAGES['invalid_list'])

            edited_service.name = name
            edited_service.place = place
            edited_service.date = date
            edited_service.vehicles_num = vehicles_num
            edited_service.volunteers_num = volunteers_num
            edited_service.contact_name = contact_name
            edited_service.contact_phone = contact_phone
            edited_service.vehicles = vehicles
            edited_service.volunteers = volunteers

            edited_service.update()

            return jsonify({
                'updated': True,
                'service': edited_service.fullData()
                })
        except RequestError as error:
            raise RequestError(error.status, error.message)
        except:
            abort(422)

    @app.route('/services/<int:id>', methods=['DELETE'])
    def delete_service(id):
        if int(id) <= 3:
            raise RequestError(403, constants.ERROR_MESSAGES['forbidden_del'])
        db_data = Service.query.filter(Service.id==id).one_or_none()
        if db_data is None:
            raise RequestError(404, constants.ERROR_MESSAGES['ser_not_found'])
        db_data.delete()

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

    return app

app = create_app()

if __name__ == '__main__':
    app.run()