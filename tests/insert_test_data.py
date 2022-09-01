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
    for i in range(1, 19):
        db.session.add(Problem(id=1000 + i, title=f'A+B问题@{str(i).zfill(3)}',
                               level='Easy', ac_num=2, submit_num=10))
    
    ph = PasswordHasher()
    db.session.add(User(username='Nyan_the_cat', password=ph.hash('1234567a'),
                        email='aaa@aaa.com'))
    db.session.add(User(username='adminadmin', password=ph.hash('adminadmin1'),
                        email='admin@mail.com', is_admin=True))
    
    db.session.commit()
    
    db.session.add(Status(
        **{
            'submitTime': "2022-3-1",
            'problemId': "1001",
            'coder': "Nyan_the_cat",
            'status': "Accepted",
            'timeCost': "10",
            'memoryCost': "30"
        }
    ))
    
    db.session.add(Status(
        **{
            'submitTime': "2022-3-1",
            'problemId': "1002",
            'coder': "Nyan_the_cat",
            'status': "Compile Error",
            'timeCost': None,
            'memoryCost': None
        }
    ))
    
    db.session.commit()
