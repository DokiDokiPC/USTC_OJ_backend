from multiprocessing import Process, Pipe
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.extensions.db import db
from backend.models import Submission, Problem, SubmissionStatus
from backend.forms import SubmissionForm
from backend.extensions.db import quick_table_count
from backend.config import get_config
from backend.blueprints.submission.publisher import publisher


submission_bp = Blueprint('submissions', __name__, url_prefix='/submissions')

available_compilers = get_config('AVAILABLE_COMPILERS')

# 放哪里比较好结束子进程?
pipe_recv_end, pipe_send_end = Pipe(duplex=False)
publisher_process = Process(target=publisher, args=(pipe_recv_end,))
# publisher_process.terminate()
# publisher_process.join()
# pipe_send_end.close()

@submission_bp.route('/', methods=['GET'])
def get_submissions():
    offset = request.args.get('offset', 0, type=int)
    return {
        'submissions': Submission.query.offset(offset).limit(get_config('QUERY_LIMIT')).all(),
        'total_count': quick_table_count(Submission)
    }


@submission_bp.route('/', methods=['POST'])
@jwt_required
def submit_solution():
    form = SubmissionForm()
    if not form.validate_on_submit():
        # 返回所有表单验证错误信息
        return [err for field in form for err in field.errors], HTTPStatus.BAD_REQUEST
    if not Problem.query.filter_by(id=form.problem_id.data).first():
        return [f'Problem {form.problem_id.data} does not exist'], HTTPStatus.BAD_REQUEST
    if form.compiler.data not in available_compilers:
        return [f'Compiler {form.compiler.data} is not supported'], HTTPStatus.BAD_REQUEST
    
    # 插入submission记录
    new_submission = Submission(
        username=get_jwt_identity(),
        problem_id=form.problem_id.data,
        compiler=form.compiler.data,
        status=SubmissionStatus.COMPILING
    )
    try:
        db.session.add(new_submission)
        db.session.commit()
    except SQLAlchemyError:
        return ['SQLAlchemyError'], HTTPStatus.BAD_REQUEST
    
    # 将判题请求发送至publisher
    pipe_send_end.send({
        'submission_id': new_submission.id,
        'username': get_jwt_identity(),
        'problem_id': form.problem_id.data,
        'compiler': form.compiler.data,
        'source_code': form.source_code.data
    })
    return '', HTTPStatus.OK
