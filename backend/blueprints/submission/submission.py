import json
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from sqlalchemy.orm import load_only
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pika

from backend.database import Session
from backend.extensions import mq
from backend.models import Submission, Problem, SubmissionStatus, SubmissionCompiler
from backend.forms import SubmissionForm
from backend.config import Config


submission_bp = Blueprint('submissions', __name__, url_prefix='/submissions')


@submission_bp.route('/', methods=['GET'])
def get_submissions():
    offset = request.args.get('offset', 0, type=int)
    stmt = select(Submission).options(load_only(
        Submission.id, Submission.submission_time, Submission.username, Submission.problem_id, Submission.compiler,
        Submission.status, Submission.time_cost, Submission.memory_cost
    )).offset(offset).limit(Config.QUERY_LIMIT)
    return {
        'submissions': Session.scalars(stmt).all(),
        'total_count': Session.scalar(select(func.count('*')).select_from(Submission)),
        'page_size': Config.QUERY_LIMIT
    }


@submission_bp.route('/', methods=['POST'])
@jwt_required()
def submit_solution():
    form = SubmissionForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.BAD_REQUEST
    if Session.get(Problem, form.problem_id.data) is None:
        return [f'Problem {form.problem_id.data} does not exist'], HTTPStatus.BAD_REQUEST
    if getattr(SubmissionCompiler, form.compiler.data, None) is None:
        return [f'Compiler {form.compiler.data} is not supported'], HTTPStatus.BAD_REQUEST

    # 插入submission记录
    new_submission = Submission(
        username=get_jwt_identity(),
        problem_id=form.problem_id.data,
        compiler=form.compiler.data,
        status=SubmissionStatus.Waiting
    )
    try:
        Session.add(new_submission)
        Session.commit()
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
        routing_key=Config.QUEUE_NAME,
        body=json.dumps(message, ensure_ascii=False),
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=pika.DeliveryMode.Transient
        )
    )

    return ''
