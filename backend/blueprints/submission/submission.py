from flask import Blueprint, request

from backend.models import Submission
from backend.extensions.db import quick_table_count
from backend.config import get_config

submission_bp = Blueprint('submissions', __name__, url_prefix='/submissions')


@submission_bp.route('/', methods=['GET'])
def get_submissions():
    offset = request.args.get('offset', 0, type=int)
    return {
        'submissions': Submission.query.offset(offset).limit(get_config('QUERY_LIMIT')).all(),
        'total_count': quick_table_count(Submission)
    }


@submission_bp.route('/<int:submission_id>', methods=['GET'])
def get_submission_detail(submission_id):
    return Submission.query.filter_by(id=submission_id).all()


@submission_bp.route('/', methods=['POST'])
def submit_solution():
    pass
