import json
from datetime import timedelta
from logging.config import dictConfig
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.db_lib.data_access import UniversalDAO

# logging
dictConfig(json.load(open('api/logs/logging.json')))


class BaseConfig(object):
    # SECRET_KEY = os.environ['SECRET_KEY']
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASS']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )


# init Flask app
app = Flask(__name__)

# specify parameters
#  sqlalchemy db connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(BaseConfig)

#  jwt
app.config['JWT_SECRET_KEY'] = 'secret_made_by_david_totally_impregnable'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_USER_CLAIMS'] = 'identity'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

#  custom
app.config['MAX_AMOUNT_OF_TIME_AT_GYM_PER_WEEK'] = timedelta(hours=3)
app.config['MAX_INACTIVITY_TIME'] = timedelta(days=180)

# init db
db = SQLAlchemy(app)
dao = UniversalDAO(db)

# init marshmallow
ma = Marshmallow(app)

# init api
api = Api(app)

# init jwt
jwt = JWTManager(app)
