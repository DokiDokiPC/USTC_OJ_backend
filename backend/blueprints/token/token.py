from datetime import datetime, timezone, timedelta
from http import HTTPStatus

from flask import Blueprint
import jwt

from backend.config import get_config
from backend.models import User
from backend.forms import LoginForm

token_bp = Blueprint('token', __name__, url_prefix='/tokens')


# 创建token成功返回token, 状态码200OK; 创建token失败返回错误原因列表
@token_bp.route('/', methods=['POST'])
def post_tokens():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            return [f'用户{form.username.data}不存在'], HTTPStatus.UNAUTHORIZED
        if form.password.data != user.password:
            return ['密码错误'], HTTPStatus.UNAUTHORIZED
        return jwt.encode(
            {
                'exp': datetime.now(tz=timezone.utc) + timedelta(hours=get_config('JWT_EXP_HOURS')),
                'username': form.username.data
            },
            get_config('JWT_SECRET'),
            get_config('JWT_ALGORITHM')
        )
    return [err for field in form for err in field.errors], HTTPStatus.UNAUTHORIZED
