from flask_sqlalchemy import SQLAlchemy, request
from app import create_app
from config.setup import setup_db, DATABASE_URL_FOR_TESTING, DB_HOST, DB_PWD, DB_TEST_NAME, DB_USER, TESTING_ACCESS_LEVEL, TESTING_ACCESS_TOKEN
from config.models import Volunteer, Service
import os
import unittest
import json
import constants
from copy import deepcopy

# Test suites are fully executed from Postman. Here's just a reduced sample.

mock_volunteer = {
    "name": "Lara",
    "surnames": "Croft",
    "birthday": "1994-07-21",
    "document": "",
    "address": "Baskerville St. 221b",
    "email": "lara@prote.ww",
    "phone1": 12345678,
    "phone2": 12345678,
    "role": 3,
    "groups": [1,2,3,4]
}
mock_vehicle = {
    "name": "Ambulance Type 2",
    "brand": "Mercedes Benz",
    "license": "1234ATU",
    "year": 2020,
    "next_itv": "2022-04-21",
    "incidents": None,
    "active": True
}
mock_service = {
    "name": "Visit to hospitalized elders",
    "place": "Hospital Europeo Brigid",
    "date": "2021-11-01, 09:20",
    "vehicles_num": 1,
    "vehicles": [1,2],
    "contact_name": "Janus Frota",
    "contact_phone": 12345678,
    "volunteers_num": 2,
    "volunteers": [2,3]
}
headers = {}
created_volunteer_id = None
created_vehicle_id = None
created_service_id = None

if TESTING_ACCESS_TOKEN:
    headers = {
        'Authorization': f'Bearer {TESTING_ACCESS_TOKEN}'
    }

class AppTesting(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = DATABASE_URL_FOR_TESTING or f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_TEST_NAME}'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_ping(self):
        """[GET:/] server is up :D"""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

# region VOLUNTEERS
    def test_read_one_volunteer(self):
        """[volunteers] read one volunteer"""
        res = self.client().get('/volunteers/1', headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'manager':
            self.assertTrue(data['success'])
            self.assertEqual(data['volunteer']['name'], 'Anna')
            self.assertNotIn('document', data['volunteer'].keys())
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'admin':
            self.assertTrue(data['success'])
            self.assertEqual(data['volunteer']['name'], 'Anna')
            self.assertIn('document', data['volunteer'].keys())
            self.assertEqual(data['volunteer']['document'], '12345678-W')

    def test_read_one_volunteer_with_invalid_id(self):
        """[volunteers] read one volunteer with invalid id"""
        res = self.client().get('/volunteers/9999', headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertEqual(res.status_code, 404)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[404])

    def test_create_a_volunteer(self):
        """[volunteers] create a volunteer"""
        global created_volunteer_id
        res = self.client().post('/volunteers', json=mock_volunteer, headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            created_volunteer_id = data['volunteer']['id']
            self.assertEqual(res.status_code, 201)
            self.assertTrue(data['created'])
            self.assertEqual(data['volunteer']['name'], mock_volunteer['name'])

    def test_update_a_volunteer(self):
        """[volunteers] updates a volunteer"""
        global created_volunteer_id
        updated_mock_volunteer = deepcopy(mock_volunteer)
        updated_mock_volunteer['active'] = False
        volunteer_on_db = Volunteer.query.filter(Volunteer.id==created_volunteer_id).one_or_none()

        if not volunteer_on_db:
            created_volunteer_id = 4
        res = self.client().patch(f'/volunteers/{created_volunteer_id}', json=updated_mock_volunteer, headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['updated'])
            self.assertEqual(data['volunteer']['name'], mock_volunteer['name'])
            self.assertEqual(data['volunteer']['active'], False)
        # Reset test changes
        self.client().patch(f'/volunteers/{created_volunteer_id}', json=mock_volunteer, headers=headers)

    def test_delete_a_volunteer(self):
        """[volunteers] deletes a volunteer"""
        global created_volunteer_id
        if not created_volunteer_id:
            created_volunteer_id =  2

        res = self.client().delete(f'/volunteers/{created_volunteer_id}', headers=headers)

        if not TESTING_ACCESS_TOKEN:
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'volunteer'):
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'admin':
            self.assertEqual(res.status_code, 204)
# endregion


# region VEHICLES
    def test_read_one_vehicle(self):
        """[vehicles] read one vehicle"""
        res = self.client().get('/vehicles/1', headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertTrue(data['success'])
            self.assertEqual(data['vehicle']['name'], 'Ambulance Type 1')

    def test_create_a_vehicle(self):
        """[vehicles] read one vehicle with invalid id"""
        global created_vehicle_id
        res = self.client().post('/vehicles', json=mock_vehicle, headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'volunteer'):
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'admin':
            created_vehicle_id = data['vehicle']['id']
            self.assertEqual(res.status_code, 201)
            self.assertTrue(data['created'])
            self.assertEqual(data['vehicle']['name'], mock_vehicle['name'])

    def test_update_a_vehicle(self):
        """[vehicles] updates a vehicle"""
        updated_mock_vehicle = deepcopy(mock_vehicle)
        updated_mock_vehicle['active'] = False
        res = self.client().patch('/vehicles/2', json=updated_mock_vehicle, headers=headers)
        data = json.loads(res.data)
        print(f'$$$ data {data}')

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['updated'])
            self.assertEqual(data['vehicle']['name'], mock_vehicle['name'])
            self.assertEqual(data['vehicle']['active'], False)
        # Reset test changes
        self.client().patch(f'/vehicles/2', json=mock_vehicle, headers=headers)

    def test_delete_a_vehicle(self):
        """[vehicles] deletes a vehicle"""
        global created_vehicle_id
        if not created_vehicle_id:
            created_vehicle_id =  2
        res = self.client().delete(f'/vehicles/{created_vehicle_id}', headers=headers)

        if not TESTING_ACCESS_TOKEN:
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'volunteer'):
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'admin':
            self.assertEqual(res.status_code, 204)
# endregion


# region SERVICES
    def test_read_all_services(self):
        """[volunteers] read all services"""
        res = self.client().get('/services', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['services']), 3)

        if not TESTING_ACCESS_TOKEN:
            self.assertNotIn('volunteers_num', data['services'][0].keys())
            self.assertNotIn('vehicles_num', data['services'][0].keys())
            self.assertNotIn('contact_name', data['services'][0].keys())
            self.assertNotIn('contact_phone', data['services'][0].keys())
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertIn('volunteers_num', data['services'][0].keys())
            self.assertIn('vehicles_num', data['services'][0].keys())
            self.assertNotIn('contact_name', data['services'][0].keys())
            self.assertNotIn('contact_phone', data['services'][0].keys())
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertIn('volunteers_num', data['services'][0].keys())
            self.assertIn('vehicles_num', data['services'][0].keys())
            self.assertIn('contact_name', data['services'][0].keys())
            self.assertIn('contact_phone', data['services'][0].keys())

    def test_read_one_service(self):
        """[services] read one service"""
        res = self.client().get('/services/1', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        if not TESTING_ACCESS_TOKEN:
            self.assertNotIn('volunteers_num', data['service'].keys())
            self.assertNotIn('vehicles_num', data['service'].keys())
            self.assertNotIn('contact_name', data['service'].keys())
            self.assertNotIn('contact_phone', data['service'].keys())
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertIn('volunteers_num', data['service'].keys())
            self.assertIn('vehicles_num', data['service'].keys())
            self.assertNotIn('contact_name', data['service'].keys())
            self.assertNotIn('contact_phone', data['service'].keys())
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertIn('volunteers_num', data['service'].keys())
            self.assertIn('vehicles_num', data['service'].keys())
            self.assertIn('contact_name', data['service'].keys())
            self.assertIn('contact_phone', data['service'].keys())

    def test_read_one_service_with_invalid_id(self):
        """[services] read one service with invalid id"""
        res = self.client().get('/services/9999', headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], constants.HTTP_RESPONSES[404])

    def test_create_a_service(self):
        """[services] create a service"""
        global created_service_id
        res = self.client().post('/services', json=mock_service, headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertEqual(res.status_code, 201)
            self.assertTrue(data['created'])
            self.assertEqual(data['service']['name'], mock_service['name'])
            created_service_id = data['service']['id']

    def test_update_a_service(self):
        """[services] updates a service"""
        global created_service_id

        updated_mock_service = deepcopy(mock_service)
        updated_mock_service['contact_name'] = 'Anna Branco'
        updated_mock_service['vehicles'] = [1]
        updated_mock_service['volunteers'] = [1]
        service_on_db = Service.query.filter(Service.id==created_service_id).one_or_none()
        if not service_on_db:
            created_service_id = 3

        res = self.client().patch(f'/services/{created_service_id}', json=updated_mock_service, headers=headers)
        data = json.loads(res.data)

        if not TESTING_ACCESS_TOKEN:
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'volunteer':
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'admin'):
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['updated'])
            self.assertEqual(data['service']['name'], mock_service['name'])
            self.assertEqual(data['service']['contact_name'], 'Anna Branco')
        # Reset test changes
        self.client().patch(f'/services/{created_service_id}', json=mock_service, headers=headers)

    def test_delete_a_service(self):
        """[services] deletes a service"""
        global created_service_id
        if not created_service_id:
            created_service_id =  2
        res = self.client().delete(f'/services/{created_service_id}', headers=headers)

        if not TESTING_ACCESS_TOKEN:
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 401)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[401])
        elif TESTING_ACCESS_TOKEN and (TESTING_ACCESS_LEVEL == 'manager' or TESTING_ACCESS_LEVEL == 'volunteer'):
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 403)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], constants.HTTP_RESPONSES[403])
        elif TESTING_ACCESS_TOKEN and TESTING_ACCESS_LEVEL == 'admin':
            self.assertEqual(res.status_code, 204)
# endregion
