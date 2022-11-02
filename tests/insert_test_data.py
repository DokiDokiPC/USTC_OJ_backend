from argon2 import PasswordHasher
from flask import Flask

from backend.models import *
from backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    for i in range(1001, 2001):
        db.session.add(Problem(id=i,
                               name=f'A+B问题@{i}',
                               level='Easy',
                               ac_num=2,
                               submit_num=10,
                               description="输入两个数字a和b，输出a+b",
                               time_limit=1000,  # ms
                               memory_limit=10240,  # KB
                               ))

    ph = PasswordHasher()
    db.session.add(User(username='admin', password=ph.hash('1111111a'), email='admin@mail.com', is_admin=True))
    db.session.add(User(username='Nyan', password=ph.hash('1111111a'), email='aaa@aaa.com'))
    db.session.add(User(username='Tanix', password=ph.hash('1111111a'), email='tanix@tanix.com'))

    db.session.commit()

    db.session.add(Submission(
        **{
            'submission_time': "2022-3-1",
            'username': "Nyan",
            'problem_id': "1001",
            'compiler': 'GCC',
            'status': SubmissionStatus.Waiting,
            'time_cost': "10",
            'memory_cost': "30"
        }
    ))
    db.session.add(Submission(
        **{
            'submission_time': "2022-3-1",
            'username': "Nyan",
            'problem_id': "1001",
            'compiler': 'GCC',
            'status': SubmissionStatus.WrongAnswer,
            'time_cost': "10",
            'memory_cost': "30"
        }
    ))

    for i in range(1000):
        db.session.add(Submission(
            **{
                'username': "Nyan",
                'problem_id': "1002",
                'compiler': "GCC",
                'status': SubmissionStatus.Accepted,
                'time_cost': 100,
                'memory_cost': 5000
            }
        ))

    db.session.commit()
