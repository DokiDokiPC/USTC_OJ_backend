import sys
from tests.insert_test_data import add_data
from backend.extensions.admin import admin
from backend.extensions.db import db
from backend.config import Config
from flask import Flask
app = Flask(__name__)


# 配置应用
app.config.from_object(Config)

# 注册数据库
db.init_app(app)

# 注册admin
admin.init_app(app)

with app.app_context():
    add_data()

sys.exit()
