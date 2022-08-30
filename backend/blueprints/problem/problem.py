from flask import Blueprint, request

from backend.models import Problem

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
        return Problem.query.filter_by(ID=problem_id).all()
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    return {'problems': Problem.query.offset(offset).limit(limit).all(), 'hint': Problem.query.count()}
