import flask

from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy


__version__ = '0.0.1'

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
CORS(app)

import tracker.models
import tracker.api  # noqa

db.create_all()
