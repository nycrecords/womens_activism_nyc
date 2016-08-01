import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    # MAIL_USERNAME = 'AKIAI3HES27X3MSXQZEA'
    # MAIL_PASSWORD = 'AuQQ/mTon4kIKEYl+fkow6IMC68bI7XqxgHr6nk5cVdV'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'womensactivismnyc@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = 'doris1234'

    # MAIL_SENDER = "Women's Activism <sgong@records.nyc.gov>"
    # FLAG_MAIL_ADMIN = "Women's Activism Flag<jmo@records.nyc.gov>"
    WOMENS_MAIL_SUBJECT_PREFIX = '[Womens Activism NYC]'
    WOMENS_MAIL_SENDER = 'Womens Activism NYC Sender <womensactivismnyc@gmail.com>'
    # WOMENS_ADMIN = os.environ.get('FLASKY_ADMIN')
    WOMENS_ADMIN = 'Womens Activism NYC Admin <womensactivismnyc@gmail.com>'

    # RECAPTCHA_PUBLIC_KEY = '6LemCCYTAAAAAK99u6ze-TTRr5eXfIBnIJUUoncO'
    # RECAPTCHA_PRIVATE_KEY = '6LemCCYTAAAAADPl7wdf5iE8yFgUKor1B8geMhlV'
    # RECAPTCHA_USE_SSL = False
    # RECAPTCHA_PUBLIC_KEY = 'public'
    # RECAPTCHA_PRIVATE_KEY = 'private'
    # RECAPTCHA_OPTIONS = {'theme': 'white'}

    # recaptcha key from womensactivismnyc@gmail.com
    # registered on google's recaptcha
    RECAPTCHA_PUBLIC_KEY = '6LexECYTAAAAAFaNYELFVlBX_ARf8_4QETX9SjYK'
    RECAPTCHA_PRIVATE_KEY = '6LexECYTAAAAAEHJZpWG41ASelOpb4VCTAtbuwLr'


    POSTS_PER_PAGE = 10


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                          'postgresql://localhost:5432/women'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                          'postgresql://localhost:5432/women'


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}