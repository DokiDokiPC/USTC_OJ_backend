from http import HTTPStatus
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy

from backend.models import Problem
from backend.extensions.db import quick_table_count
from backend.config import get_config

from backend.extensions.db import db

from sqlalchemy.exc import SQLAlchemyError

problem_bp = Blueprint('problem', __name__, url_prefix='/problems')


# 获取问题列表
@problem_bp.route('/', methods=['GET'])
def get_problems():
    offset = request.args.get('offset', 0, type=int)
    return {
        'problems': Problem.query.offset(offset).limit(get_config('QUERY_LIMIT')).all(),
        'total_count': quick_table_count(Problem),
        'page_size': get_config('QUERY_LIMIT')
    }


# 获取问题详情
@problem_bp.route('/<int:problem_id>', methods=['GET'])
def get_problem_detail(problem_id):
    return Problem.query.filter_by(id=problem_id).all()


def problem_already_exist(problem_id: int) -> bool:
    return Problem.query.filter_by(id=problem_id).first() is not None


# 添加问题
@problem_bp.route('/', methods=['POST'])
def create_problem():
    data = request.get_json()
    new_problem = Problem(**data)
    if problem_already_exist(new_problem.id):
        return [f"Problem ID {new_problem.id} already exists"], HTTPStatus.CONFLICT
    try:
        db.session.add(new_problem)
        db.session.commit()
        return ["Create Success"], HTTPStatus.CREATED
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST


# 修改问题
@problem_bp.route('/<int:problem_id>', methods=['PUT'])
def change_problem(problem_id):
    data = request.get_json()
    new_problem = Problem(**data)
    now_problem = Problem.query().get(problem_id)
    try:
        now_problem.__dict__.update(new_problem.__dict__)
        db.session.commit()
        return ["Change Success"], HTTPStatus.OK
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST


# 删除问题
@problem_bp.route('/<int:problem_id>', methods=['PUT'])
def delete_problem(problem_id):
    if problem_already_exist(problem_id):
        pass
    else:
        return [f"cannot find the problem {problem_id} to delete."], HTTPStatus.CONFLICT
    now_problem = Problem.query().get(problem_id)
    try:
        db.session.delete(now_problem)
        db.session.commit()
        return ["Delete Success"], HTTPStatus.NO_CONTENT
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST
