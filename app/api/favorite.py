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


@bp.route('/', methods=['POST'])
def insert_favorite_station():
    new_station_id = request.json.get('station_id')

    if not is_station(new_station_id):
        return jsonify({'fail': 'station_id not exist'})
    else:
        favorite_station = FavoriteStation.query \
            .filter_by(station_id=new_station_id).first()
        if favorite_station is not None:
            return jsonify({'fail': 'duplicate'})

        new_favorite = FavoriteStation(
            station_id=new_station_id,
            created_time=datetime.now()
        )
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({'success': 'inserted'})


@bp.route('/', methods=['DELETE'])
def delete_favorite_station():
    to_delete_station_id = request.json.get('station_id')

    if not is_station(to_delete_station_id):
        return jsonify({'fail': 'station_id not exist'})
    else:
        favorite_station = FavoriteStation.query \
            .filter_by(station_id=to_delete_station_id).first()
        if favorite_station is None:
            return jsonify({'fail': 'station_id not in table'})

        FavoriteStation.query.filter_by(station_id=to_delete_station_id) \
            .delete()
        db.session.commit()

        return jsonify({'success': 'deleted'})
