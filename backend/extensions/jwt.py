from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user

from backend.models import User
from backend.database import Session

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return Session.get(User, identity)


def admin_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_current_user()
            if current_user and current_user.is_admin:
                return func(*args, **kwargs)
            else:
                return 'Admin only', HTTPStatus.UNAUTHORIZED
        return decorator
    return wrapper
