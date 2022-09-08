from http import HTTPStatus

from flask import Blueprint, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_current_user,\
    create_access_token, set_access_cookies, unset_access_cookies
from argon2 import PasswordHasher

from backend.models import User
from backend.extensions.db import db
from backend.forms import RegisterForm, UpdateForm

user_bp = Blueprint('user', __name__, url_prefix='/users')
ph = PasswordHasher()


# 获取当前用户信息
@user_bp.route('/<string:username>', methods=['GET'])
@jwt_required()
def get_user(username):
    current_user = get_current_user()
    if not current_user:
        # 数据库中找不到用户, 可能是删除账号后未删除token
        return ['Your account has been deleted'], HTTPStatus.UNAUTHORIZED
    elif current_user.username != username:
        return ['Permission denied'], HTTPStatus.FORBIDDEN
    else:
        return jsonify(current_user)


# 创建新用户
@user_bp.route('/', methods=['POST'])
def create_user():
    form = RegisterForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.NOT_ACCEPTABLE
    if User.query.filter_by(username=form.username.data).first():
        return [f'username {form.username.data} already exists'], HTTPStatus.CONFLICT
    if User.query.filter_by(email=form.email.data).first():
        return [f'email {form.email.data} already exists'], HTTPStatus.CONFLICT
    new_user = User(username=form.username.data, password=ph.hash(form.password.data), email=form.email.data)
    try:
        db.session.add(new_user)
        db.session.commit()
        return '', HTTPStatus.CREATED
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.NOT_ACCEPTABLE


# 更改信息
@user_bp.route('/<string:username>', methods=['PUT'])
@jwt_required()
def update_user(username):
    form = UpdateForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.NOT_ACCEPTABLE
    current_user = get_current_user()
    if not current_user:
        # 数据库中找不到用户, 可能是删除账号后未删除token
        return ['Your account has been deleted'], HTTPStatus.UNAUTHORIZED
    if current_user.username != username:
        return ['Permission denied'], HTTPStatus.FORBIDDEN
    if hasattr(form, 'password'):
        form.password.data = ph.hash(form.password.data)
    form.populate_obj(current_user)
    try:
        # 更新用户信息
        current_user.save()
        response = make_response()
        if hasattr(form, 'password'):
            # 如果更改了密码, 重新设置access_token_cookie
            access_token = create_access_token(identity=current_user.username)
            set_access_cookies(response, access_token)
        return response
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.NOT_ACCEPTABLE


# 删除用户
@user_bp.route('/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    current_user = get_current_user()
    if not current_user:
        # 数据库中找不到用户, 可能是删除账号后未删除token
        return ['Your account has been deleted'], HTTPStatus.NO_CONTENT
    if current_user.username != username:
        return ['Permission denied'], HTTPStatus.FORBIDDEN
    try:
        db.session.delete(current_user)
        db.session.commit()
        # 删除用户后去除该用户的jwt
        response = make_response()
        unset_access_cookies(response)
        return response, HTTPStatus.NO_CONTENT
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.NOT_ACCEPTABLE
