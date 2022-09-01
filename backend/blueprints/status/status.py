from flask import Blueprint, request

from backend.models import Status

status_bp = Blueprint('status', __name__, url_prefix='/status')


@status_bp.route('/', methods=['GET'], defaults={'status_id': None})
@status_bp.route('/<int:status_id>', methods=['GET'])
def get_status(status_id):
    """
    @@@
    ```python
    return 
    {'status': Status.query.offset(offset).limit(limit).all(), 'hint': Status.query.count()}
    ```
    @@@
    """
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    if status_id:
        return Status.query.filter_by(id=status_id).all()
    return {'status': Status.query.offset(offset).limit(limit).all(), 'hint': Status.query.count()}
