from flask import Flask
from os import path

# configuration
DATABASE = path.join(path.dirname(__file__), 'database.db')
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

import hrm_app.views
