from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from config.setup import setup_db
from config.populate_db import db_drop_and_create_all
import os

app = Flask(__name__)
setup_db(app)
CORS(app)

# --- Uncomment to re/set the db. ALL DATA WILL BE LOST!
# db_drop_and_create_all()

# --- ROUTES

@app.route('/')
def callback():
    return 'Healthy'

if __name__ == '__main__':
    assert os.path.exists('.env')
    app.run(host='0.0.0.0', port=5000, debug=True if os.environ['FLASK_ENV'] == 'development' else False)