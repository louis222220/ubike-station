from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .routes import station
# from .routes import favorite
from .routes import hello
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    @app.before_first_request
    def before_first_request():
        from .modules.station import check_init_stations
        check_init_stations()

    # app.register_blueprint(station.bp)
    # app.register_blueprint(favorite.bp)

    # FIXME:
    app.register_blueprint(hello.bp)

    return app
