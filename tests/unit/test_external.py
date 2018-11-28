import pytest
from app.modules import station


def test_get_ubike_json():
    import json
    station_data = station.get_ubike_json()
    assert type(station_data) == dict
    assert 'retVal' in station_data

# TODO: error condition
