def create_app():
    # 放在里面import, 这样当tests中导入backend内文件时, 不会执行下面这些导入
    from flask import Flask

    from backend.config import Config
    from backend.extensions import jwt, cors, mq
    from backend import database
    from backend.blueprints import user_bp, token_bp, problem_bp, submission_bp
    # 初始化应用
    app = Flask(__name__)
    # 配置应用
    app.config.from_object(Config)
    # 注册插件
    # admin.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mq.init_app(app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(token_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(submission_bp)
    # 注册SQLAlchemy
    database.init_app(app)
    # 返回app
    return app
