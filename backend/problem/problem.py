from flask import Blueprint
from backend.models import Problem

bp = Blueprint('problem', __name__, url_prefix='/problem')

@bp.route("/")
def problem():
    return {'status': 'success', 'problem': [p.to_dict() for p in Problem.query.all()]}