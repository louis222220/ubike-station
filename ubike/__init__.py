import os

from flask import Flask
from ubike.db import sqlite
from ubike.routes import station
from ubike.routes import favorite
from ubike.modules.station import init_stations


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'ubike.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sqlite.init_app(app)
    init_stations()

    app.register_blueprint(station.bp)
    app.register_blueprint(favorite.bp)

    return app
