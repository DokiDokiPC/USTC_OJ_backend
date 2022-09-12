from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, get_current_user

from backend.models import User, Problem, Submission
from backend.extensions.db import db
from backend.forms import LoginForm


class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        form = LoginForm()
        return self.render('admin/index.html', form=form)


class AdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(AdminView, self).__init__(model, *args, **kwargs)

    @jwt_required()
    def is_accessible(self):
        return get_current_user() and get_current_user().is_admin


admin = Admin(name='ustcoj', template_mode='bootstrap3', index_view=HomeView('login'))
admin.add_view(AdminView(User, db.session, name='Users', endpoint='admin_user'))
admin.add_view(AdminView(Problem, db.session, name='Problems', endpoint='admin_problem'))
admin.add_view(AdminView(Submission, db.session, name='Submissions', endpoint='admin_submission'))
