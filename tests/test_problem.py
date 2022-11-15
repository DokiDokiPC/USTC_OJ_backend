from http import HTTPStatus

from flask.testing import FlaskClient

from backend.models import ProblemLevel
from backend.config import Config

prefix = '/problems/'
data = {
    'name': '测试问题',
    'level': ProblemLevel.Easy,
    'description': '测试简介',
    'time_limit': 1000,
    'memory_limit': 10,
}

def test_create(client: FlaskClient, login_client: FlaskClient, admin_client: FlaskClient):
    assert client.post(prefix, data=data).status_code == HTTPStatus.UNAUTHORIZED
    assert login_client.post(prefix, data=data).status_code == HTTPStatus.UNAUTHORIZED
    assert admin_client.post(prefix, data=data).status_code == HTTPStatus.CREATED

def test_get_list(client: FlaskClient, login_client: FlaskClient):
    assert client.get(prefix).status_code == HTTPStatus.UNAUTHORIZED
    resp = login_client.get(prefix)
    assert resp.status_code == HTTPStatus.OK
    data = resp.get_json()
    assert data['page_size'] == Config.QUERY_LIMIT
    assert len(data['problems']) == min(Config.QUERY_LIMIT, data['total'])
