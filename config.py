import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("BLOG_SECRET_KEY") or "hard to guess string ;)"
    POSTS_PER_PAGE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    BLOG_MAIL_SUBJECT_PREFIX = os.environ.get("BLOG_MAIL_SUBJECT_PREFIX") or "blog"
    BLOG_MAIL_SENDER = os.environ.get("BLOG_MAIL_SENDER") or "example@example.com"

    # Celery
    CELERY_BROKER_URL = os.environ.get("BLOG_TASK_BROKER")
    RESULT_BACKEND = os.environ.get("BLOG_TASK_RESULT")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = "Development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "BLOG_DEV_DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data-dev.sqlite')}"


class TestingConfig(Config):
    ENV = "TESTING"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "BLOG_TESTING_DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data-test.sqlite')}"
    ADMIN = "admin@example.com"


class ProductionConfig(Config):
    ENV = "PRODUCTION"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "BLOG_DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
