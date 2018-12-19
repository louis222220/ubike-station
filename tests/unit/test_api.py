import pytest
from datetime import datetime
import json
from app.api import favorite
from app.modules import station
from app.models import FavoriteStation, db

api_url_prefix = '/api/v1'


def add_favorite_test_data():
    favorite_stations = [
        FavoriteStation(station_id=2, created_time=datetime.now()),
        FavoriteStation(station_id=1, created_time=datetime.now())
    ]
    db.session.bulk_save_objects(favorite_stations)
    db.session.commit()


def test_favorite_index(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_empty = client.get(api_url_prefix + '/favorite/')
    assert response_empty.is_json
    assert 'favorite_stations' in response_empty.get_json()
    assert response_empty.get_json()['favorite_stations'] == []

    with app.app_context():
        add_favorite_test_data()
    response = client.get(api_url_prefix + '/favorite/')
    assert response.get_json()['favorite_stations'] == [1, 2]


def test_favorite_insert(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    client.post(api_url_prefix + '/favorite/', data=json.dumps(dict(
            station_id=2
        )),
        content_type='application/json'
    )

    response = client.get(api_url_prefix + '/favorite/')
    assert response.get_json()['favorite_stations'] == [2]


def test_favorite_delete(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()
        add_favorite_test_data()

    client.delete(api_url_prefix + '/favorite/', data=json.dumps(dict(
        station_id=2
        )),
        content_type='application/json'
    )

    response = client.get(api_url_prefix + '/favorite/')
    assert response.get_json()['favorite_stations'] == [1]


def test_station_index(client, mock_get_ubike_json):
    response = client.get(api_url_prefix + '/station/')
    assert response.is_json
    assert 'retVal' in response.get_json()


def test_station_get_by_station_number(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_exist = client.get(api_url_prefix + '/station/1')
    assert response_exist.is_json
    assert 'sno' in response_exist.get_json()

    response_not_exist = client.get(api_url_prefix + '/station/4')
    assert response_not_exist.status_code == 404

    # TODO: 404 condition
    # TODO: return json if error


def test_station_get_by_station_name(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_exist = client.get(api_url_prefix + '/station/捷運市政府站(3號出口)')
    assert response_exist.is_json
    assert 'sno' in response_exist.get_json()

    response_not_exist = client.get(api_url_prefix + '/station/abc')
    assert response_not_exist.status_code == 404
