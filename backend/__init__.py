from flask import Flask
from flask_cors import CORS

from backend.config import Config
from backend.db import db
from backend.admin import admin
from backend.blueprints import user_bp, token_bp, problem_bp

def create_app():
    # 初始化应用
    app = Flask(__name__)
    # 配置应用
    app.config.from_object(Config)
    # 注册插件
    db.init_app(app)
    admin.init_app(app)
    CORS(app, resources={r'/*': {'origins': '*'}})
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(problem_bp)
    # 返回app
    return app
