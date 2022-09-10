from datetime import datetime, timezone
from http import HTTPStatus

from flask import Blueprint, make_response
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity, set_access_cookies,\
    unset_access_cookies, jwt_required
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

from backend.config import get_config
from backend.models import User
from backend.forms import LoginForm

token_bp = Blueprint('token', __name__, url_prefix='/tokens')
ph = PasswordHasher()


# 使用after_request回调函数, 刷新将在JWT_REFRESH_WITHIN_HOURS内过期的token
@token_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + get_config('JWT_REFRESH_WITHIN_HOURS'))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


# 获取一个jwt
@token_bp.route('/', methods=['POST'])
def get_token():
    form = LoginForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.UNAUTHORIZED
    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return [f'Username "{form.username.data}" does not exist'], HTTPStatus.UNAUTHORIZED
    try:
        ph.verify(user.password, form.password.data)
        response = make_response()
        access_token = create_access_token(identity=form.username.data)
        set_access_cookies(response, access_token)
        return response
    except VerifyMismatchError:
        return ['Wrong password'], HTTPStatus.UNAUTHORIZED
    except InvalidHash:
        return ['InvalidHash, please contact the administrator'], HTTPStatus.UNAUTHORIZED


# 删除jwt
@token_bp.route('/', methods=['DELETE'])
def delete_token():
    response = make_response()
    unset_access_cookies(response)
    return response


# 测试jwt是否有效, 如果没有或者无效, 会返回401-UNAUTHORIZED
@token_bp.route('/', methods=['HEAD'])
@jwt_required()
def test_token():
    return '', HTTPStatus.OK
