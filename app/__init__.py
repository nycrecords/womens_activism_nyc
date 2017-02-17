from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app((app))

    from .main import main as main
    app.register_blueprint(main)

    from .story import story as story
    app.register_blueprint(story, url_prefix="/story")

    from .stories import stories as stories_blueprint
    app.register_blueprint(stories_blueprint)

    return app
