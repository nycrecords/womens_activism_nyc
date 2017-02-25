from flask import Flask
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from flask_elasticsearch import FlaskElasticsearch
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
es = FlaskElasticsearch()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    es.init_app(app, use_ssl=app.config['ELASTICSEARCH_USE_SSL'])
    db.init_app(app)
    moment.init_app((app))

    from .main import main as main
    app.register_blueprint(main)

    from .share import share as share
    app.register_blueprint(share, url_prefix="/share")

    from .stories import stories as stories
    app.register_blueprint(stories, url_prefix="/stories")

    from .search import search as search
    app.register_blueprint(search, url_prefix="/search")

    return app