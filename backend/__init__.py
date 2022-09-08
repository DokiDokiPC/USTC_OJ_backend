from flask import Flask

from backend.config import Config
from backend.extensions import db, admin, jwt, cors
from backend.blueprints import user_bp, token_bp, problem_bp, status_bp


def create_app():
    # 初始化应用
    app = Flask(__name__)
    # 配置应用
    app.config.from_object(Config)
    # 注册插件
    db.init_app(app)
    admin.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(status_bp)
    # 返回app
    return app
