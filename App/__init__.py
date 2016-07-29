from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

pagedown = PageDown()


def create_app(config_name):
    current_app = Flask(__name__)
    current_app.config.from_object(config[config_name])
    current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    config[config_name].init_app(current_app)

    bootstrap.init_app(current_app)
    mail.init_app(current_app)
    moment.init_app(current_app)
    db.init_app(current_app)
    login_manager.init_app(current_app)
    pagedown.init_app(current_app)

    from .main import main as main_blueprint
    current_app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    current_app.register_blueprint(auth_blueprint)

    from .tags import tags as tags_blueprint
    current_app.register_blueprint(tags_blueprint)

    from .feedback import feedback as feedback_blueprint
    current_app.register_blueprint(feedback_blueprint)

    return current_app
