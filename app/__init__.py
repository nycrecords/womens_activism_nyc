from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_elasticsearch import FlaskElasticsearch
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config

bootstrap = Bootstrap()
csrf = CSRFProtect()
db = SQLAlchemy()
es = FlaskElasticsearch()
moment = Moment()

# for auth admin login (page 95 from the book for reference)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    es.init_app(app, use_ssl=app.config['ELASTICSEARCH_USE_SSL'])
    db.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("error/generic.html", status_code=400,
                               message=e.description or None)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error/generic.html", status_code=403)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error/generic.html", status_code=404)

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error/generic.html", status_code=500)

    from .main import main as main
    app.register_blueprint(main)

    from .share import share as share
    app.register_blueprint(share, url_prefix="/share")

    from .stories import stories as stories
    app.register_blueprint(stories)

    from .search import search as search
    app.register_blueprint(search, url_prefix="/search")

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .edit import edit as edit
    app.register_blueprint(edit)

    return app
