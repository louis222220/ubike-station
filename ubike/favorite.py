import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.exceptions import abort
import json

from .db import get_db
from .station import isStation

bp = Blueprint('favorite', __name__, url_prefix='/favorite')

@bp.route('/')
def index():
    db = get_db()

    favoriteStationRows = db.execute(
        'SELECT stationNo FROM favoriteStation'
        ' ORDER BY stationNo ASC'
    ).fetchall()

    favoriteStations = [ row[0] for row in favoriteStationRows]
    jsonFavoriteStations = { "favoriteStations": favoriteStations }
    return json.dumps( jsonFavoriteStations )


@bp.route('/insert/<int:stationNo>')
def insertFavoriteStation(stationNo):
    if not isStation(stationNo):
        return "station {} doesn't exist" . format(stationNo)
    else:
        db = get_db()

        if db.execute(
            'SELECT * FROM favoriteStation WHERE stationNo = ?',
            (stationNo, )
        ).fetchone() is not None:
            return "station {} already in table" . format(stationNo)

        db.execute(
            'INSERT INTO favoriteStation (stationNo)'
            ' VALUES (?)',
            (stationNo, )
        )
        db.commit()
        return "success in inserting"
        

@bp.route('/delete/<int:stationNo>')
def deleteFavoriteStation(stationNo):
    if not isStation(stationNo):
        return "station {} doesn't exist" . format(stationNo)
    else:
        db = get_db()

        if db.execute(
            'SELECT * FROM favoriteStation WHERE stationNo = ?',
            (stationNo, )
        ).fetchone() is None:
            return "station {} is not in table" . format(stationNo)

        db.execute(
            'DELETE FROM favoriteStation'
            ' WHERE stationNo = ?',
            (stationNo, )
        )
        db.commit()
        return "success in deleting"