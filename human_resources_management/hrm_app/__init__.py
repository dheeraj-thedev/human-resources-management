from flask import Flask
from os import path
from . import DBHelper

# configuration
DATABASE = path.join(path.dirname(__file__), 'database.db')
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
DB = DBHelper.DBHelper(app.config['DATABASE'])

import hrm_app.views