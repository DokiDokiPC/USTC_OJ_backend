from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from flask_jwt_extended import jwt_required, get_current_user,\
    create_access_token, set_access_cookies, unset_access_cookies
from argon2 import PasswordHasher

from backend.models import User
from backend.database import Session, get_dicts
from backend.forms import RegisterForm, UserUpdateForm
from backend.config import Config

user_bp = Blueprint('user', __name__, url_prefix='/users')
ph = PasswordHasher()


# 获取用户列表
@user_bp.route('/', methods=['GET'])
def get_user_list():
    # 获取url参数
    offset = request.args.get('offset', 0, type=int)

    # 构造查询语句
    stmt = (select(User.username, User.solved).offset(offset)
            .limit(Config.QUERY_LIMIT).order_by(User.solved.desc()))
    count_stmt = select(func.count('*')).select_from(User)

    # 执行查询并返回
    return {
        'users': get_dicts(stmt),
        'total': Session.scalar(count_stmt),
        'page_size': Config.QUERY_LIMIT
    }


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
        return [err for field in form for err in field.errors], HTTPStatus.BAD_REQUEST
    if Session.get(User, form.username.data) is not None:
        return [f'Username "{form.username.data}" already exists'], HTTPStatus.CONFLICT
    if Session.get(User, {'email': form.email.data}) is not None:
        return [f'Email {form.email.data} already exists'], HTTPStatus.CONFLICT
    new_user = User(
        username=form.username.data,
        password=ph.hash(form.password.data),
        email=form.email.data
    )
    try:
        Session.add(new_user)
        Session.commit()
        # 创建成功了也返回一个JWT, 直接登录成功
        response = make_response()
        access_token = create_access_token(identity=form.username.data)
        set_access_cookies(response, access_token)
        return response, HTTPStatus.CREATED
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST


# 更改信息
@user_bp.route('/<string:username>', methods=['PUT'])
@jwt_required()
def update_user(username):
    form = UserUpdateForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.BAD_REQUEST
    current_user = get_current_user()
    if current_user is None:
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
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST


# 删除用户
@user_bp.route('/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    current_user = get_current_user()
    if not current_user:
        # 数据库中找不到用户, 可能是删除账号后未删除token
        return ['Your account has been deleted'], HTTPStatus.CONFLICT
    if current_user.username != username:
        return ['Permission denied'], HTTPStatus.FORBIDDEN
    try:
        Session.delete(current_user)
        Session.commit()
        # 删除用户后去除该用户的jwt
        response = make_response()
        unset_access_cookies(response)
        return response, HTTPStatus.NO_CONTENT
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST
