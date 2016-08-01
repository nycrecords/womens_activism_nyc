from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
<<<<<<< HEAD
from flask_login import LoginManager
=======
>>>>>>> remotes/origin/feature/WOM-12_2

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

<<<<<<< HEAD
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

=======
>>>>>>> remotes/origin/feature/WOM-12_2

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
<<<<<<< HEAD

=======
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
>>>>>>> remotes/origin/feature/WOM-12_2
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
<<<<<<< HEAD
    login_manager.init_app(app)
=======
>>>>>>> remotes/origin/feature/WOM-12_2

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

<<<<<<< HEAD
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

=======
>>>>>>> remotes/origin/feature/WOM-12_2
    return app
