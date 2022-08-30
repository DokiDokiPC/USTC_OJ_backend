from http import HTTPStatus

from flask import Blueprint
from sqlalchemy import exc
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.models import User
from backend.extensions.db import db
from backend.forms import RegisterForm

user_bp = Blueprint('user', __name__, url_prefix='/users')


# 返回指定id用户或用户列表
@user_bp.route('/', methods=['GET'], defaults={'username': None})
@user_bp.route('/<string:username>', methods=['GET'])
@jwt_required()
def get_users(username):
    if username:
        current_user = get_jwt_identity()
        return User.query.filter_by(username=username).all()
    return User.query.all()


# 创建用户成功返回空body, 状态码201CREATED; 创建用户失败返回错误原因列表
@user_bp.route('/', methods=['POST'])
def post_users():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            return [f'用户{form.username.data}已存在'], HTTPStatus.CONFLICT
        if User.query.filter_by(email=form.email.data).first():
            return [f'邮箱{form.email.data}已存在'], HTTPStatus.CONFLICT
        new_user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return '', HTTPStatus.CREATED
        except exc.SQLAlchemyError:
            return ['SQLAlchemyError'], HTTPStatus.NOT_ACCEPTABLE
    return [err for field in form for err in field.errors], HTTPStatus.NOT_ACCEPTABLE
