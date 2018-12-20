from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort
from ..modules import station

bp = Blueprint('station', __name__, url_prefix='/station')

# TODO: auth


@bp.route('/')
def index():
    return jsonify(station.get_ubike_json())


@bp.route('/<int:station_number>')
def get_by_station_number(station_number):
    if not station.is_station(station_number):
        abort(404)
    else:
        station_number = str(station_number).zfill(4)
        station_data = station.get_ubike_json()
        return jsonify(station_data["retVal"][station_number])


@bp.route('/<string:station_name>')
def get_by_station_name(station_name):
    station_name = station_name.strip()

    station_data = station.get_ubike_json()
    for cell in station_data["retVal"].values():
        if station_name == cell["sna"] or station_name == cell["snaen"]:
            return jsonify(cell)
    abort(404)


@bp.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return e
