from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, get_current_user

from backend.models import User, Problem, ProblemLevel, Submission, SubmissionStatus
from backend.extensions.db import db
from backend.forms import LoginForm


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        form = LoginForm()
        return self.render('admin/index.html', form=form)


class AdminView(ModelView):
    page_size = 10
    
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.column_sortable_list = self.column_list
        super(AdminView, self).__init__(model, *args, **kwargs)

    @jwt_required()
    def is_accessible(self):
        return get_current_user() and get_current_user().is_admin


class UserAdminView(AdminView):
    can_view_details = True
    column_exclude_list = ['password']
    column_searchable_list = ['username', 'email']
    form_columns = ['username', 'password', 'email', 'is_admin']


class ProblemAdminView(AdminView):
    can_view_details = True
    column_exclude_list = ['description']
    column_searchable_list = ['id', 'name', 'description']
    form_choices = {
        'level': [(v, v) for k, v in ProblemLevel.__dict__.items() if not k.startswith('_')],
    }


class SubmissionAdminView(AdminView):
    column_searchable_list = ['submission_time', 'username', 'problem_id', 'compiler', 'status']
    form_choices = {
        'compiler': [('GCC', 'GCC'), ('G++', 'G++')],
        'status': [(v, v) for k, v in SubmissionStatus.__dict__.items() if not k.startswith('_')]
    }
    form_columns = ['submission_time', 'username', 'problem_id', 'compiler', 'status', 'time_cost', 'memory_cost']


admin = Admin(name='ustcoj', template_mode='bootstrap3', index_view=HomeView('login'))
admin.add_view(UserAdminView(User, db.session, name='Users', endpoint='admin_user'))
admin.add_view(ProblemAdminView(Problem, db.session, name='Problems', endpoint='admin_problem'))
admin.add_view(SubmissionAdminView(Submission, db.session, name='Submissions', endpoint='admin_submission'))
