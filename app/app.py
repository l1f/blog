from flask import Flask

from config import config

from .exstensions import celery, db, login_manager, mail
from .template_injections import inject_permissions


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    init_celery(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.context_processor(inject_permissions)

    from .auth import auth
    from .blog import blog
    from .cms import cms

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(cms, url_prefix="/cms")
    app.register_blueprint(blog)

    return app


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_BROKER_URL"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
