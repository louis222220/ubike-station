import pytest
from app.modules import station
from app.models import Station


@pytest.mark.first
def test_factory_before_first_request(
        app, client, mocker, mock_get_ubike_json):
    mocker.patch('app.modules.station.check_init_stations')

    client.get('/')
    station.check_init_stations.assert_called_once_with()


def test_init_stations(app, clear_db, mock_get_ubike_json):
    with app.app_context():
        station_row = Station.query.first()
        assert station_row is None

        station.init_stations()

        station_rows = Station.query.all()
        assert len(station_rows) == 3


def test_check_init_stations(app, clear_db, mock_get_ubike_json):
    with app.app_context():
        station_row = Station.query.first()
        assert station_row is None

        for i in range(2):
            station.check_init_stations()

            station_rows = Station.query.all()
            assert len(station_rows) == 3


def test_routes_index(client, mock_get_ubike_json):
    response = client.get('/station/')
    assert response.is_json
    assert 'retVal' in response.get_json()


def test_routes_get_by_station_number(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_exist = client.get('/station/1')
    assert response_exist.is_json
    assert 'sno' in response_exist.get_json()

    response_not_exist = client.get('/station/4')
    assert response_not_exist.status_code == 404

    # TODO: 404 condition
    # TODO: return json if error


def test_routes_get_by_station_name(app, client, mock_get_ubike_json):
    with app.app_context():
        station.check_init_stations()

    response_exist = client.get('/station/捷運市政府站(3號出口)')
    assert response_exist.is_json
    assert 'sno' in response_exist.get_json()

    response_not_exist = client.get('/station/abc')
    assert response_not_exist.status_code == 404
