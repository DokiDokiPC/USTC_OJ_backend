from flask import Flask
from flask_cors import CORS

from backend.config import Config
from backend.db import db
from backend.admin import admin
from backend.blueprints import blueprints

from flask_docs import ApiDoc


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
