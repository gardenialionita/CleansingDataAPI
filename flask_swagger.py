from distutils.command.config import config
import sqlite3
from tabnanny import check
import pandas as pd
from flask import Flask, request, jsonify, make_response
from data_cleansing import process_file, process_text
from flask_swagger_ui import get_swaggerui_blueprint

#Init app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#Database
db_conn = sqlite3.connect('cleansingdata.db', check_same_thread=False)
db_conn.row.factory = sqlite3.row()
mycursor = db_conn.cursor()

#Flask swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'Twiclin!'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

#Homepage