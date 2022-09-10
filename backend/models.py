from dataclasses import dataclass
from datetime import datetime

from backend.config import get_config
from backend.extensions.db import db


@dataclass
class Problem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(80), nullable=False)
    level: str = db.Column(db.String(20), nullable=False)
    ac_num: int = db.Column(db.Integer, nullable=False, default=0)
    submit_num: int = db.Column(db.Integer, nullable=False, default=0)


@dataclass
class User(db.Model):
    username: str = db.Column(db.String(get_config('USERNAME_MAX_LEN')), primary_key=True)
    password: str = db.Column(db.String(get_config('PWD_HASHED_LEN')), nullable=False)
    email: str = db.Column(db.String(get_config('EMAIL_MAX_LEN')), nullable=False, unique=True)
    is_admin: bool = db.Column(db.Boolean(), nullable=False, default=False)


@dataclass
class Status(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    submit_time: datetime = db.Column(db.DateTime, nullable=False)
    problem_id: int = db.Column(
        db.Integer, db.ForeignKey('problem.id'), nullable=False,)
    coder: str = db.Column(db.String(80), db.ForeignKey(
        'user.username'), nullable=False)
    status: str = db.Column(db.String(20), nullable=False)
    # time_cost ms
    time_cost: int = db.Column(db.Integer)
    # memory_cost KB
    memory_cost: int = db.Column(db.Integer)
