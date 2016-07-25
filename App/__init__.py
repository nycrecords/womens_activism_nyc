from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    current_app = Flask(__name__)
    current_app.config.from_object(config[config_name])
    config[config_name].init_app(current_app)

    bootstrap.init_app(current_app)
    mail.init_app(current_app)
    moment.init_app(current_app)
    db.init_app(current_app)

    from .main import main as main_blueprint
    current_app.register_blueprint(main_blueprint)

    return current_app

