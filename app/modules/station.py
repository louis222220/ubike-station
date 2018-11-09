import requests
from ..__init__ import db
from ..models import Station

UBIKE_TAIPEI_URL = 'https://tcgbusfs.blob.core.windows.net/' \
                   'blobyoubike/YouBikeTP.gz'


def get_ubike_json():
    res = requests.get(UBIKE_TAIPEI_URL)
    if res.status_code == 200:
        return res.json()
    return {'error': 'Ubike server no response'}


def is_station(station_number):
    station = Station.query.filter_by(station_no=station_number).first()
    return station is not None


def check_init_stations():
    station = Station.query.first()
    if station is None:
        init_stations()


def init_stations():
    station_data = get_ubike_json()
    for key in station_data["retVal"].keys():
        station = Station(station_no=key)
        db.session.add(station)
    db.session.commit()
