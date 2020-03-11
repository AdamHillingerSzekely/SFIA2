from flask import Flask
import os
import requests
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

from application import routes

