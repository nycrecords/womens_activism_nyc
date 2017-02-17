import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # remove once this becomes the default

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL') or
                               'postgresql://localhost:5432/womens_activism_dev')

    # Elasticsearch settings
    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST') or "localhost:9200"
    ELASTICSEARCH_INDEX = os.environ.get('ELASTICSEARCH_INDEX') or "stories"
    ELASTICSEARCH_USE_SSL = os.environ.get('ELASTICSEARCH_USE_SSL') == "True"
    ELASTICSEARCH_USERNAME = os.environ.get('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD = os.environ.get('ELASTICSEARCH_PASSWORD')
    ELASTICSEARCH_HTTP_AUTH = ((ELASTICSEARCH_USERNAME,
                                ELASTICSEARCH_PASSWORD)
                               if ELASTICSEARCH_USERNAME and ELASTICSEARCH_PASSWORD
                               else None)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('TEST_DATABASE_URL') or
                               'postgresql://localhost:5432/womens_activism_test')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'postgresql://localhost:5432/womens_activism_prod')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}