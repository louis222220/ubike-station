import pytest
from datetime import datetime
import json
from app.api import favorite
from app.modules import station
from app.models import FavoriteStation, db

api_url_prefix = '/api/v1'


def get_api_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


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

    response_empty = client.get(
        api_url_prefix + '/favorite/',
        headers=get_api_headers())
    assert response_empty.is_json
    assert 'favorite_stations' in response_empty.get_json()
    assert response_empty.get_json()['favorite_stations'] == []

    with app.app_context():
        add_favorite_test_data()
    response = client.get(
        api_url_prefix + '/favorite/',
        headers=get_api_headers())
    assert response.get_json()['favorite_stations'] == [1, 2]


def test_favorite_insert_success(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_insert = client.post(
        api_url_prefix + '/favorite/',
        data=json.dumps(dict(
            station_id=2
        )),
        headers=get_api_headers()
    )
    assert response_insert.is_json
    assert response_insert.get_json()['success'] == 'inserted'

    response = client.get(
        api_url_prefix + '/favorite/',
        headers=get_api_headers())
    assert response.get_json()['favorite_stations'] == [2]


def test_favorite_insert_duplicate(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()
        add_favorite_test_data()

    response_insert = client.post(
        api_url_prefix + '/favorite/',
        data=json.dumps(dict(
            station_id=2
        )),
        headers=get_api_headers()
    )
    assert response_insert.is_json
    assert response_insert.get_json()['fail'] == 'duplicate'


def test_favorite_insert_not_exist(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_insert = client.post(
        api_url_prefix + '/favorite/',
        data=json.dumps(dict(
            station_id=600
        )),
        headers=get_api_headers()
    )
    assert response_insert.is_json
    assert response_insert.get_json()['fail'] == 'station_id not exist'


def test_favorite_delete_success(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()
        add_favorite_test_data()

    response_delete = client.delete(
        api_url_prefix + '/favorite/',
        data=json.dumps(dict(
            station_id=2
        )),
        headers=get_api_headers()
    )
    assert response_delete.is_json
    assert response_delete.get_json()['success'] == 'deleted'

    response = client.get(
        api_url_prefix + '/favorite/',
        headers=get_api_headers())
    assert response.get_json()['favorite_stations'] == [1]


def test_favorite_delete_not_in_table(
        app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_delete = client.delete(
        api_url_prefix + '/favorite/',
        data=json.dumps(dict(
            station_id=2
        )),
        headers=get_api_headers()
    )
    assert response_delete.is_json
    assert response_delete.get_json()['fail'] == 'station_id not in table'


def test_favorite_delete_not_exist(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_delete = client.delete(
        api_url_prefix + '/favorite/',
        data=json.dumps(dict(
            station_id=600
        )),
        headers=get_api_headers()
    )
    assert response_delete.is_json
    assert response_delete.get_json()['fail'] == 'station_id not exist'


def test_station_index(client, mock_get_ubike_json):
    response = client.get(
        api_url_prefix + '/station/',
        headers=get_api_headers())
    assert response.is_json
    assert 'retVal' in response.get_json()


def test_station_get_by_station_number(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_exist = client.get(
        api_url_prefix + '/station/1',
        headers=get_api_headers())
    assert response_exist.is_json
    assert 'sno' in response_exist.get_json()

    response_not_exist = client.get(
        api_url_prefix + '/station/4',
        headers=get_api_headers())
    assert response_not_exist.status_code == 404
    assert response_exist.is_json


def test_station_get_by_station_name(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_exist = client.get(
        api_url_prefix + '/station/捷運市政府站(3號出口)',
        headers=get_api_headers())
    assert response_exist.is_json
    assert 'sno' in response_exist.get_json()

    response_not_exist = client.get(
        api_url_prefix + '/station/abc',
        headers=get_api_headers())
    assert response_not_exist.status_code == 404


def test_page_not_found(app, client):
    response = client.get(
        '/wrong/url',
        headers=get_api_headers())
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()['error'] == 'not found'
