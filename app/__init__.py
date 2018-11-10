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

    from .routes import station
    from .routes import favorite
    app.register_blueprint(station.bp)
    app.register_blueprint(favorite.bp)

    return app
