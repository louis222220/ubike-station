from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

    api_url_prefix = '/api/v1'
    from .api import station
    from .api import favorite
    app.register_blueprint(
        station.bp, url_prefix=api_url_prefix + station.bp.url_prefix)
    app.register_blueprint(
        favorite.bp, url_prefix=api_url_prefix + favorite.bp.url_prefix)

    return app
