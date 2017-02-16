from flask import Flask
from flask_bootstrap import Bootstrap
from flask_elasticsearch import FlaskElasticsearch
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
es = FlaskElasticsearch


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main
    app.register_blueprint(main)

    from .story import story as story
    app.register_blueprint(story, url_prefix="/story")

    return app
