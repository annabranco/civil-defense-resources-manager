from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv, find_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Connect to the database
DB_HOST = env.get('DB_HOST', '127.0.0.1:5432')
DB_USER = env.get('DB_USER', 'postgres')
DB_PWD = env.get('DB_PWD', 'postgres')
DB_NAME = env.get('DB_NAME', 'postgres')
DB_TEST_NAME = env.get('DB_TEST_NAME', 'postgres')
DATABASE_URL = env.get('DATABASE_URL')
DATABASE_URL_FOR_TESTING = env.get('DATABASE_URL_FOR_TESTING')

database_path = DATABASE_URL or f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}/{DB_NAME}'

db = SQLAlchemy()

def setup_db(app,db_path=database_path ):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
