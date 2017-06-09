from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from rq import Queue
from worker import conn


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

twitter_db = SQLAlchemy(app)
q = Queue(connection=conn)

from twitterapp.views import view
from twitterapp.models import model
