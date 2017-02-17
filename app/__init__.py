from flask import Flask, render_template
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

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("error/generic.html", status_code=400)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error/generic.html", status_code=403)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error/generic.html", status_code=404)

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error/generic.html", status_code=500)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .stories import stories as stories_blueprint
    app.register_blueprint(stories_blueprint)

    return app
