from operator import imod
from backend.extensions.db import db
from flask import Flask
import sys

import toml
configs = toml.load("./my_database_config.toml")


app = Flask(__name__)


USERNAME = configs['USERNAME']
PASSWORD = configs['PASSWORD']
HOSTNAME = configs['HOSTNAME']
PORT = configs['PORT']
DATABASE = configs['DATABASE_NAME']


SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

sys.exit()
