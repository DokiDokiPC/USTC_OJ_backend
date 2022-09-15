import sys
from pathlib import Path

from argon2 import PasswordHasher
from flask import Flask

sys.path.append(str(Path(__file__).parent.parent))

from backend.config import Config
from backend.models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    for i in range(1001, 2001):
        db.session.add(Problem(id=i, title=f'A+B问题@{i}',
                               level='Easy', ac_num=2, submit_num=10))
    
    ph = PasswordHasher()
    db.session.add(User(username='Nyan', password=ph.hash('1111111a'),
                        email='aaa@aaa.com'))
    db.session.add(User(username='admin', password=ph.hash('1111111a'),
                        email='admin@mail.com', is_admin=True))
    
    db.session.commit()
    
    db.session.add(Submission(
        **{
            'submission_time': "2022-3-1",
            'problem_id': "1001",
            'username': "Nyan",
            'result': "Accepted",
            'time_cost': "10",
            'memory_cost': "30"
        }
    ))
    
    db.session.add(Submission(
        **{
            'submission_time': "2022-3-1",
            'problem_id': "1002",
            'username': "Nyan",
            'result': "Compile Error",
            'time_cost': None,
            'memory_cost': None
        }
    ))
    
    db.session.commit()
