import os

basedir = os.path.abspath(os.path.dirname(__file__))
prefix = "BLOG"


class Config:
    SECRET_KEY = os.environ.get(f"{prefix}_SECRET_KEY") or "hard to guess string ;)"
    POSTS_PER_PAGE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = "Development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        f"{prefix}_DEV_DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data-dev.sqlite')}"


class TestingConfig(Config):
    ENV = "TESTING"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        f"{prefix}_TESTING_DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data-test.sqlite')}"
    ADMIN = "admin@example.com"


class ProductionConfig(Config):
    ENV = "PRODUCTION"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        f"{prefix}_DATABASE_URI") or f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}