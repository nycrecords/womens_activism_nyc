import os
basedir = os.path.abspath(os.path.dirname(__file__))


# mail = Mail()

# app = Flask(__name__)
# mail.init_app(app)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('AKIAI3HES27X3MSXQZEA')
    MAIL_PASSWORD = os.environ.get('AuQQ/mTon4kIKEYl+fkow6IMC68bI7XqxgHr6nk5cVdV')
    FLASKY_MAIL_SENDER = 'Admin <sgong@records.nyc.gov'
    FLASKY_ADMIN = os.environ.get('ADMIN')


   # app.config["MAIL_SERVER"] = 'email-smtp.us-east-1.amazonaws.com'
   # app.config["MAIL_USERNAME"] = 'AKIAI3HES27X3MSXQZEA'
   # app.config["MAIL_PASSWORD"] = 'AuQQ/mTon4kIKEYl+fkow6IMC68bI7XqxgHr6nk5cVdV'
   # app.config["MAIL_PORT"] = 587
   # app.config["MAIL_USE_TLS"] = True
   # mail.init_app(app)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
 #   SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
   #     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
  #  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
 #       'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    pass
  # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
  #      'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
