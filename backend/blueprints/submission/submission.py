import json
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pika

from backend.extensions.db import db, quick_table_count
from backend.extensions import mq
from backend.models import Submission, Problem, SubmissionStatus, Compilers
from backend.forms import SubmissionForm
from backend.config import get_config


submission_bp = Blueprint('submissions', __name__, url_prefix='/submissions')


@submission_bp.route('/', methods=['GET'])
def get_submissions():
    offset = request.args.get('offset', 0, type=int)
    return {
        'submissions': Submission.query.offset(offset).limit(get_config('QUERY_LIMIT')).all(),
        'total_count': quick_table_count(Submission)
    }


@submission_bp.route('/', methods=['POST'])
@jwt_required()
def submit_solution():
    form = SubmissionForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.BAD_REQUEST
    if not Problem.query.filter_by(id=form.problem_id.data).first():
        return [f'Problem {form.problem_id.data} does not exist'], HTTPStatus.BAD_REQUEST
    if getattr(Compilers, form.compiler.data, None) is None:
        return [f'Compiler {form.compiler.data} is not supported'], HTTPStatus.BAD_REQUEST
    
    # 插入submission记录
    new_submission = Submission(
        username=get_jwt_identity(),
        problem_id=form.problem_id.data,
        compiler=form.compiler.data,
        status=SubmissionStatus.Waiting
    )
    try:
        db.session.add(new_submission)
        db.session.commit()
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST
    
    # 将判题请求发送至publisher
    message = {
        'submission_id': new_submission.id,
        'problem_id': form.problem_id.data,
        'username': get_jwt_identity(),
        'compiler': form.compiler.data,
        'source_code': form.source_code.data
    }
    mq.channel.basic_publish(
        exchange='',
        routing_key=get_config('QUEUE_NAME'),
        body=json.dumps(message, ensure_ascii=False),
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=pika.DeliveryMode.Transient
        )
    )
    
    return '', HTTPStatus.OK
