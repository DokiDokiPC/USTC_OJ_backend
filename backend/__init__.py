from flask import Flask

from backend.config import Config
from backend.extensions import db, admin, jwt, docs, cors
from backend.blueprints import user_bp, token_bp, problem_bp
from backend.blueprints import blueprints


def create_app():
    # 初始化应用
    app = Flask(__name__)
    # 配置应用
    app.config.from_object(Config)
    # 注册插件
    db.init_app(app)
    admin.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)
    cors.init_app(app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(problem_bp)
    for bp in blueprints:
        app.register_blueprint(bp)

    # 自动生成文档
    app.config["API_DOC_MEMBER"] = ["problem"]
    app.config["API_DOC_MEMBER"] += ["user"]
    app.config["API_DOC_MEMBER"] += ["token"]
    app.config["API_DOC_MEMBER"] += ["status"]
    ApiDoc(
        app,
        title="USTCOJ",
        version="1.0.0",
        description="Online Judge",
    )
    # 返回app
    return app
