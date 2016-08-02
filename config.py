import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'womensactivismnyc@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = 'doris1234'
    WOMENS_MAIL_SUBJECT_PREFIX = '[Womens Activism NYC]'
    WOMENS_MAIL_SENDER = 'Womens Activism NYC Admin <flasky@example.com>'
    WOMENS_ADMIN = 'womensactivismnyc@gmail.com'
    RECAPTCHA_PUBLIC_KEY = '6LetUSYTAAAAALgTT8Rt2nLZ2OTBNph6Qa1TbrAH'
    RECAPTCHA_PRIVATE_KEY = '6LetUSgYTAAAAAN1pLPLyyIFUh6rEemXczfMFT4um'
    POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost:5432/womens_activism_nyc_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost:5432/womens_activism_nyc_test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost:5432/womens_activism_nyc'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
