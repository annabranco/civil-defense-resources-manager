from flask_sqlalchemy import SQLAlchemy
from app import create_app
from config.setup import setup_db, DB_TEST_NAME, DATABASE_URL_FOR_TESTING, DB_USER, DB_PWD, DB_HOST
print(f'$$$ DB_TEST_NAME {DB_TEST_NAME}')

print(f'$$$ DATABASE_URL_FOR_TESTING {DATABASE_URL_FOR_TESTING}')

import os
import unittest
import json

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
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'The server is up! :D')

# region VOLUNTEERS
    def test_read_one_volunteer(self):
        """[volunteers] read volunteer"""
        res = self.client().get('/volunteers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['volunteer']['name'], 'Anna')
        self.assertEqual(data['volunteer']['role'], 'Commander')
        self.assertEqual(data['volunteer']['groups'][0], 'EMS')

# endregion

# region GROUPS
    def test_read_one_group(self):
        """[groups] read group"""
        res = self.client().get('/groups/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['group']['name'], 'EMS')

# endregion

# region ROLES
    def test_read_one_role(self):
        """[roles] read role"""
        res = self.client().get('/roles/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['role']['name'], 'Volunteer')

# endregion

# region VEHICLES
    def test_read_one_vehicle(self):
        """[vehicles] read vehicle"""
        res = self.client().get('/vehicles/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['vehicle']['name'], 'Ambulance Type 1')

# endregion

# region SERVICES
    def test_read_one_service(self):
        """[services] read service"""
        res = self.client().get('/services/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['service']['name'], 'Preventive service on football match')
# endregion
