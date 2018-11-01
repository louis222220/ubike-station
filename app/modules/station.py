import requests
from ubike.db import sqlite

UBIKE_TAIPEI_URL = 'http://data.taipei/youbike'


def get_ubike_json():
    res = requests.get(UBIKE_TAIPEI_URL)
    if res.status_code == 200:
        return res.json()
    return {'error': 'Ubike server no response'}


def is_station(station_number):
    station = sqlite.db.execute(
        'SELECT *'
        ' FROM stations WHERE stationNo = ?',
        (station_number, )
    ).fetchone()
    return station is not None


def init_stations():
    station_data = get_ubike_json()
    for key in station_data["retVal"].keys():
        sqlite.db.execute(
            'INSERT INTO stations (stationNo)'
            ' VALUES (?)',
            (key, )
        )
    sqlite.db.commit()
