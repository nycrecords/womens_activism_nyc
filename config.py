import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, ".env")
load_dotenv(dotenv_path)


class Config:
    # Flask-WTF
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "postgresql://localhost:5432/womens_activism"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # remove once this becomes the default
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Data Path to Files
    FEATURED_DATA = os.environ.get("FEATURED_DATA") or os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data", "featured.csv"
    )

    # Elasticsearch Settings
    ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST") or "localhost:9200"
    ELASTICSEARCH_ENABLED = os.environ.get("ELASTICSEARCH_ENABLED") == "True"
    ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX") or "stories"
    ELASTICSEARCH_USE_SSL = os.environ.get("ELASTICSEARCH_USE_SSL") == "True"
    ELASTICSEARCH_USERNAME = os.environ.get("ELASTICSEARCH_USERNAME")
    ELASTICSEARCH_PASSWORD = os.environ.get("ELASTICSEARCH_PASSWORD")
    ELASTICSEARCH_HTTP_AUTH = (
        (ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
        if ELASTICSEARCH_USERNAME and ELASTICSEARCH_PASSWORD
        else None
    )
    # Recatpcha Keys
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    # Flask-Mail Settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', "True") == "True"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL")
        or "postgresql://developer@localhost:5432/womens_activism"
    )

    # Elasticsearch settings
    ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST") or "localhost:9200"
    ELASTICSEARCH_ENABLED = os.environ.get("ELASTICSEARCH_ENABLED") == "True"
    ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX") or "stories"
    ELASTICSEARCH_USE_SSL = os.environ.get("ELASTICSEARCH_USE_SSL") == "True"
    ELASTICSEARCH_USERNAME = os.environ.get("ELASTICSEARCH_USERNAME")
    ELASTICSEARCH_PASSWORD = os.environ.get("ELASTICSEARCH_PASSWORD")
    ELASTICSEARCH_HTTP_AUTH = (
        (ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
        if ELASTICSEARCH_USERNAME and ELASTICSEARCH_PASSWORD
        else None
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL")
        or "postgresql://localhost:5432/womens_activism_test"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://localhost:5432/womens_activism_nyc_v2"
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
