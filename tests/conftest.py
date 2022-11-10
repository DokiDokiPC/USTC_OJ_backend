import pytest

from backend import create_app


@pytest.fixture()
def app():
    print('app fixture')
    app = create_app()
    app.testing = True
    yield app


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def login_client(app):
    login_client = app.test_client()
    login_client.post('/tokens/', data={'username': 'Tanix', 'password': '1111111a'})
    yield login_client


@pytest.fixture()
def admin_client(app):
    admin_client = app.test_client()
    admin_client.post('/tokens/', data={'username': 'admin', 'password': '1111111a'})
    yield admin_client


@pytest.fixture()
def runner(app):
    yield app.test_cli_runner()
