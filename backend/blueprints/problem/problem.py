from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import func, select
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from backend.config import Config
from backend.database import Session
from backend.models import Problem
from backend.forms import ProblemForm
from backend.extensions.jwt import admin_required

problem_bp = Blueprint('problem', __name__, url_prefix='/problems')


# 获取问题列表
@problem_bp.route('/', methods=['GET'])
@jwt_required()
def get_problems():
    offset = request.args.get('offset', 0, type=int)
    name = request.args.get('name', None)
    stmt = (
        select(Problem)
        .options(load_only(Problem.id, Problem.name, Problem.level, Problem.ac_num, Problem.submit_num))
        .offset(offset)
        .limit(Config.QUERY_LIMIT)
    )
    if name is not None:
        stmt = stmt.filter(Problem.name.contains(name))
    return {
        'problems': Session.scalars(stmt).all(),
        'total_count': Session.scalar(select(func.count('*')).select_from(Problem)),
        'page_size': Config.QUERY_LIMIT
    }


# 获取问题详情
@problem_bp.route('/<int:problem_id>', methods=['GET'])
@jwt_required()
def get_problem_detail(problem_id):
    return [Session.get(Problem, problem_id)]


# 添加问题
@problem_bp.route('/', methods=['POST'])
@admin_required()
def create_problem():
    form = ProblemForm()
    new_problem = Problem()
    form.populate_obj(new_problem)
    try:
        Session.add(new_problem)
        Session.commit()
        return '', HTTPStatus.CREATED
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST


# 修改问题
@problem_bp.route('/<int:problem_id>', methods=['PUT'])
@admin_required()
def change_problem(problem_id):
    form = ProblemForm()
    problem = Session.get(Problem, problem_id)
    form.populate_obj(problem)
    try:
        Session.commit()
        return ''
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST


# 删除问题
@problem_bp.route('/<int:problem_id>', methods=['DELETE'])
@admin_required()
def delete_problem(problem_id):
    problem = Session.get(Problem, problem_id)
    if problem is None:
        return [f'Problem {problem_id} does not exist.'], HTTPStatus.NO_CONTENT
    try:
        Session.delete(problem)
        Session.commit()
        return '', HTTPStatus.NO_CONTENT
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST
