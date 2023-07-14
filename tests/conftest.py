import pytest
from src.app import app as flask_app
from src.app import db as _db

@pytest.fixture(scope='module')
def app():
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture(scope='module')
def db(app, request):
    with app.app_context():
        _db.create_all()

    def teardown():
        with app.app_context():
            _db.session.remove()
            _db.drop_all()

    request.addfinalizer(teardown)
    return _db