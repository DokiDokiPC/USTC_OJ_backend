import json
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pika

from backend.database import Session, get_dicts
from backend.extensions import mq
from backend.models import Submission, Problem, SubmissionStatus, SubmissionCompiler
from backend.forms import SubmissionForm
from backend.config import Config


submission_bp = Blueprint('submissions', __name__, url_prefix='/submissions')


@submission_bp.route('/', methods=['GET'])
def get_submissions():
    # 获取url参数
    username = request.args.get('username', None, type=str)
    offset = request.args.get('offset', 0, type=int)

    # 构造submission的查询语句, 以及统计数量的语句
    stmt = (select(Submission).offset(offset).limit(Config.QUERY_LIMIT)
            .order_by(Submission.id.desc()))  # submission逆序
    count_stmt = select(func.count('*')).select_from(Submission)
    if username is not None:
        username = func.binary(username)  # 使username区分大小写
        stmt = stmt.filter(Submission.username == username)
        count_stmt = count_stmt.filter(Submission.username == username)

    # 执行查询并返回
    return {
        'submissions': get_dicts(stmt),
        'total': Session.scalar(count_stmt),
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

    return '', HTTPStatus.OK
