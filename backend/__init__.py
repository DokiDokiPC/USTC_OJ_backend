from flask import Flask
app = Flask(__name__)

from backend.config import Config, getc
from backend.models import db, User
from backend.admin import admin
import backend.views

# 配置应用
app.config.from_object(Config)

# 注册数据库
db.init_app(app)

# 注册admin
admin.init_app(app)
