import pytest
from datetime import datetime
import json
from app.routes import favorite
from app.modules import station
from app.models import FavoriteStation, db


def add_favorite_test_data():
    favorite_stations = [
        FavoriteStation(station_id=2, created_time=datetime.now()),
        FavoriteStation(station_id=1, created_time=datetime.now())
    ]
    db.session.bulk_save_objects(favorite_stations)
    db.session.commit()


def test_routes_index(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_empty = client.get('/favorite/')
    assert response_empty.is_json
    assert 'favorite_stations' in response_empty.get_json()
    assert response_empty.get_json()['favorite_stations'] == []

    with app.app_context():
        add_favorite_test_data()
    response = client.get('/favorite/')
    assert response.get_json()['favorite_stations'] == [1, 2]


def test_routes_insert(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    client.post('/favorite/', data=json.dumps(dict(
            station_id=2
        )),
        content_type='application/json'
    )

    response = client.get('/favorite/')
    assert response.get_json()['favorite_stations'] == [2]


def test_routes_delete(app, client, clear_db, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()
        add_favorite_test_data()

    client.delete('/favorite/', data=json.dumps(dict(
        station_id=2
        )),
        content_type='application/json'
    )

    response = client.get('/favorite/')
    assert response.get_json()['favorite_stations'] == [1]
