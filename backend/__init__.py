from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


from backend.config import Config
from backend.db import db
from backend.admin import admin

# 配置应用
app.config.from_object(Config)

# 注册数据库
db.init_app(app)
with app.app_context():
    db.create_all()

# 注册admin
admin.init_app(app)

# 蓝图problem
from backend.problem import problem
app.register_blueprint(problem.bp)