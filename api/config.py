import json
from datetime import timedelta
from logging.config import dictConfig

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.db_lib.data_access import UniversalDAO

# logging
dictConfig(json.load(open('logging.json')))

# init Flask app
app = Flask(__name__)

# specify parameters
#  sqlalchemy db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_user:test_user@localhost:5432/LibTest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  jwt
app.config['JWT_SECRET_KEY'] = 'secret_made_by_david_totally_impregnable'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_USER_CLAIMS'] = 'identity'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

#  customer
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
