from flask import request, Blueprint, jsonify
from datetime import datetime
from ..__init__ import db
from ..models import FavoriteStation
from ..modules.station import is_station

bp = Blueprint('favorite', __name__, url_prefix='/favorite')


@bp.route('/')
def index():
    favorite_station_rows = FavoriteStation.query \
        .order_by(FavoriteStation.station_id.asc())

    favorite_stations = [
        favorite_station.station_id
        for favorite_station in favorite_station_rows]
    return jsonify({"favorite_stations": favorite_stations})


# TODO: refactor to be cleaner
@bp.route('/', methods=['POST'])
def insert_favorite_station():
    new_station_id = request.json.get('station_id')

    if not is_station(new_station_id):
        # TODO: use json in every return
        return "station {} doesn't exist" . format(new_station_id)
    else:
        favorite_station = FavoriteStation.query \
            .filter_by(station_id=new_station_id).first()
        if favorite_station is not None:
            return "station {} already in table" . format(new_station_id)

        # TODO: time zone

        new_favorite = FavoriteStation(
            station_id=new_station_id,
            created_time=datetime.now()
        )
        db.session.add(new_favorite)
        db.session.commit()

        return "success in inserting"


@bp.route('/', methods=['DELETE'])
def delete_favorite_station():
    to_delete_station_id = request.json.get('station_id')

    if not is_station(to_delete_station_id):
        return "station {} doesn't exist" . format(to_delete_station_id)
    else:
        favorite_station = FavoriteStation.query \
            .filter_by(station_id=to_delete_station_id).first()
        if favorite_station is None:
            return "station {} is not in table" . format(to_delete_station_id)

        FavoriteStation.query.filter_by(station_id=to_delete_station_id) \
            .delete()
        db.session.commit()

        return "success in deleting"
