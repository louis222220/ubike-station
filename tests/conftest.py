import pytest
from flask_migrate import Migrate, upgrade, downgrade
from app import create_app, db
from app.models import Station


@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')

    migrate = Migrate(app, db)

    with app.app_context():
        upgrade()
        # TODO: load test data?
        # get_db().executescript(_data_sql)

    yield app

    with app.app_context():
        db.session.remove()
        db.reflect()
        db.drop_all()


@pytest.fixture
def clear_db(app):
    """Clear the database for some test."""
    with app.app_context():
        db.reflect()
        db.drop_all()
        db.create_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_get_ubike_json(mocker):
    from app.modules.station import get_ubike_json
    import os
    import json

    ubike_test_json = {}
    json_path = os.path.join(os.path.dirname(__file__), 'mock_ubike.json')
    with open(json_path) as json_data:
        ubike_test_json = json.loads(json_data.read())

    mocker.patch(
        'app.modules.station.get_ubike_json',
        return_value=ubike_test_json)
