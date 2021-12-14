from celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
celery = Celery()
toolbar = DebugToolbarExtension()
