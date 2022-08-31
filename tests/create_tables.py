import sys
from pathlib import Path

from flask import Flask

sys.path.append(str(Path(__file__).parent.parent))

from backend.config import Config
from backend.extensions.db import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()
