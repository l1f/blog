from flask import Flask
from config import config

from .exstensions import db, login_manager, celery


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    celery.conf.update(app.config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .auth import auth
    from .cms import cms
    from .blog import blog
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(cms, url_prefix="/cms")
    app.register_blueprint(blog)

    return app
