from dataclasses import dataclass
from datetime import datetime
from pydoc import describe
from tokenize import String

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
class ProblemDetail(db.Model):
    id: int = db.Column(db.Integer, db.ForeignKey(
        'problem.id'), primary_key=True)
    # 题目描述
    description: str = db.Column(db.Unicode, nullable=False)
    # 时间空间限制
    time_limit: int = db.Column(db.Integer, nullable=False)
    mempry_limit: int = db.Column(db.Integer, nullable=False)
    # 样例路径
    example_path: str = db.Column(db.String(120), nullable=False)
    # 所有测试用例路径
    tests_path: str = db.Column(db.String(120), nullable=False)


@dataclass
class Contest(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(80), nullable=False)
    start_time: datetime = db.Column(db.DateTime, nullable=False)
    end_time: datetime = db.Column(db.DateTime, nullable=False)


@dataclass
class ContestProblem(db.Model):
    problem_id: int = db.Column(
        db.Integer, db.ForeignKey('problem.id'), primary_key=True)
    contest_id: int = db.Column(
        db.Integer, db.ForeignKey('contest.id'), primary_key=True)


@dataclass
class User(db.Model):
    username: str = db.Column(
        db.String(get_config('USERNAME_MAX_LEN')), primary_key=True)
    password: str = db.Column(
        db.String(get_config('PWD_HASHED_LEN')), nullable=False)
    email: str = db.Column(db.String(get_config(
        'EMAIL_MAX_LEN')), nullable=False, unique=True)
    is_admin: bool = db.Column(db.Boolean(), nullable=False, default=False)


@dataclass
class Submission(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    submission_time: datetime = db.Column(db.DateTime, nullable=False)
    problem_id: int = db.Column(
        db.Integer, db.ForeignKey('problem.id'), nullable=False,)
    username: str = db.Column(db.String(80), db.ForeignKey(
        'user.username'), nullable=False)
    result: str = db.Column(db.String(20), nullable=False)
    # time_cost ms
    time_cost: int = db.Column(db.Integer)
    # memory_cost KB
    memory_cost: int = db.Column(db.Integer)
