import functools

from flask import Blueprint, jsonify
from werkzeug.exceptions import abort
import json

from ubike.db import sqlite
from ubike.modules.station import is_station

bp = Blueprint('favorite', __name__, url_prefix='/favorite')


@bp.route('/')
def index():
    favorite_station_rows = sqlite.db.execute(
        'SELECT stationNo FROM favoriteStation'
        ' ORDER BY stationNo ASC'
    ).fetchall()

    favorite_stations = [row['stationNo'] for row in favorite_station_rows]
    return jsonify({"favorite_stations": favorite_stations})


@bp.route('/insert/<int:stationNo>')
def insertFavoriteStation(stationNo):
    if not is_station(stationNo):
        return "station {} doesn't exist" . format(stationNo)
    else:
        if sqlite.db.execute(
            'SELECT * FROM favoriteStation WHERE stationNo = ?',
            (stationNo, )
        ).fetchone() is not None:
            return "station {} already in table" . format(stationNo)

        sqlite.db.execute(
            'INSERT INTO favoriteStation (stationNo)'
            ' VALUES (?)',
            (stationNo, )
        )
        sqlite.db.commit()
        return "success in inserting"


@bp.route('/delete/<int:stationNo>')
def deleteFavoriteStation(stationNo):
    if not is_station(stationNo):
        return "station {} doesn't exist" . format(stationNo)
    else:
        if sqlite.db.execute(
            'SELECT * FROM favoriteStation WHERE stationNo = ?',
            (stationNo, )
        ).fetchone() is None:
            return "station {} is not in table" . format(stationNo)

        sqlite.db.execute(
            'DELETE FROM favoriteStation'
            ' WHERE stationNo = ?',
            (stationNo, )
        )
        sqlite.db.commit()
        return "success in deleting"