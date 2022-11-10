from flask.testing import FlaskClient

from backend.models import ProblemLevel

prefix = '/problems/'

def test_create(client: FlaskClient):
    resp = client.post(prefix, data={
        'id': 2002,
        'name': '测试问题',
        'level': ProblemLevel.Easy,
        'ac_num': 2,
        'submit_num': 10,
        'description': '测试简介',
        'time_limit': 1000,
        'memory_limit': 10,
    })
