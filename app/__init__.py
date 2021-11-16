from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()


# login_manager = LoginManager()
# login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # login_manager.init_app(app)

    from .cms import cms
    from .blog import blog
    app.register_blueprint(cms, url_prefix="/cms")
    app.register_blueprint(blog)

    return app
