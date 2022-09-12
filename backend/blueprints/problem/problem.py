from flask import Blueprint, request

from backend.models import Problem
from backend.extensions.db import quick_table_count
from backend.config import get_config

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
