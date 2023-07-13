import pytest
from src.app import app as flask_app
from src.app import db as _db

@pytest.fixture(scope='module')
def app():
    return flask_app

@pytest.fixture(scope='module')
def db(app, request):
    with app.app_context():
        _db.create_all()

    def teardown():
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db
