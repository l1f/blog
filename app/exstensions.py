from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
