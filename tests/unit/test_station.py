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
