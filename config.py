import os
basedir = os.path.abspath(os.path.dirname(__file__))


<<<<<<< .merge_file_Hja4qp
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'womensactivismnyc@gmail.com'

    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = 'doris1234'
    WOMENS_MAIL_SUBJECT_PREFIX = '[Womens Activism NYC]'
    WOMENS_MAIL_SENDER = 'Womens Activism NYC Admin <flasky@example.com>'
    # WOMENS_ADMIN = os.environ.get('FLASKY_ADMIN')
    WOMENS_ADMIN = 'womensactivismnyc@gmail.com'

    # recaptcha key from womensactivismnyc@gmail.com
    # registered on google's recaptcha

    RECAPTCHA_PUBLIC_KEY = '6LetUSYTAAAAALgTT8Rt2nLZ2OTBNph6Qa1TbrAH'
    RECAPTCHA_PRIVATE_KEY = '6LetUSYTAAAAAN1pLPLyyIFUh6rEemXczfMFT4um'


    POSTS_PER_PAGE = 10
=======
# mail = Mail()

# app = Flask(__name__)
# mail.init_app(app)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    MAIL_USERNAME = 'AKIAI3HES27X3MSXQZEA'
    MAIL_PASSWORD = 'AuQQ/mTon4kIKEYl+fkow6IMC68bI7XqxgHr6nk5cVdV'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SENDER = "Women's Activism <sgong@records.nyc.gov>"
    # MAIL_RECEIVER = "<sgong9570@gmail.com>"
    MAIL_ADMIN = "<sgong9570@gmail.com>"

    RECAPTCHA_PUBLIC_KEY = '6LeaCCYTAAAAAEQgFc258VCfPgu5iLJZb42JBuZ8'
    RECAPTCHA_PRIVATE_KEY = '6LeaCCYTAAAAAApdJTNppVwy7juVd6ucrcA4wsbn'

    @staticmethod
    def init_app(app):
        pass



    # mail.init_app(app)
>>>>>>> .merge_file_HYQRWb

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
<<<<<<< .merge_file_Hja4qp
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost:5432/women'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                          'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
=======
 #   SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
   #     'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
>>>>>>> .merge_file_HYQRWb


class TestingConfig(Config):
    TESTING = True
<<<<<<< .merge_file_Hja4qp
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost:5432/women'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://localhost:5432/women'
=======
  #  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
 #       'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    pass
  # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
  #      'sqlite:///' + os.path.join(basedir, 'data.sqlite')
>>>>>>> .merge_file_HYQRWb


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
<<<<<<< .merge_file_Hja4qp
}
=======
}
>>>>>>> .merge_file_HYQRWb
