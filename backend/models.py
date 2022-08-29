from flask_sqlalchemy import SQLAlchemy

from backend.config import get_config

from backend.db import db

# convert model into dict or inverse.
class MyModel():
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def to_model(cls, **kwargs):
        res = Problem()
        columns = [c.name for c in cls.__table__.columns]
        for k, v in kwargs.items():
            if k in columns:
                setattr(res, k, v)
        return res


class Problem(db.Model, MyModel):
    __tablename__ = 'Problem'
    ID = db.Column(db.Integer,
                           nullable=False, primary_key=True)
    Title = db.Column(db.String(80), nullable=False)


class User(db.Model, MyModel):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(get_config(
        'USERNAME_MAX_LEN')), unique=True, nullable=False)
    password = db.Column(db.String(get_config('PWD_MAX_LEN')), nullable=False)
    email = db.Column(db.String(get_config('EMAIL_MAX_LEN')),
                      unique=True, nullable=False)
    nickname = db.Column(
        db.String(get_config('NICKNAME_MAX_LEN')), nullable=False)
