from backend.db import db
from backend.models import *

def add_data():
    db.session.add(Problem.to_model(**{'ID': '1001', 'Title': 'A+B问题'}))
    db.session.commit()
