from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
<<<<<<< .merge_file_Sgedsv
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

=======
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
>>>>>>> .merge_file_QNMNbo

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

<<<<<<< .merge_file_Sgedsv
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .tag import tags as tag_blueprint
    app.register_blueprint(tag_blueprint)

    from .feedback import feedback as feedback_blueprint
    app.register_blueprint(feedback_blueprint)

    from .flags import flags as flags_blueprint
    app.register_blueprint(flags_blueprint)

    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)

    return app
=======

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

>>>>>>> .merge_file_QNMNbo
