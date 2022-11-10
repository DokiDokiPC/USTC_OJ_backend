from flask_jwt_extended import JWTManager

from backend.models import User
from backend.database import Session

jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return Session.get(User, identity)
