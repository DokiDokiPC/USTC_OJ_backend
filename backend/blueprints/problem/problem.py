from flask import Blueprint, request

from backend.models import Problem
from backend.extensions.db import table_count
from backend.config import get_config

problem_bp = Blueprint('problem', __name__, url_prefix='/problems')


@problem_bp.route('/', methods=['GET'], defaults={'problem_id': None})
@problem_bp.route('/<int:problem_id>', methods=['GET'])
def get_problems(problem_id):
    """
    @@@
    ```python
    return 
    {'problems': Problem.query.offset(offset).limit(limit).all(), 'hint': Problem.query.count()}
    ```
    @@@
    """
    if problem_id:
        return Problem.query.filter_by(id=problem_id).all()
    offset = request.args.get('offset', 0, type=int)
    return {
        'problems': Problem.query.offset(offset).limit(get_config('QUERY_LIMIT')).all(),
        'total_count': table_count(Problem),
        'page_size': get_config('QUERY_LIMIT')
    }
