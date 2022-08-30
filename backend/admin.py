from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from backend.models import User, Problem
from backend.db import db

admin = Admin(name='ustcoj', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session, name='Users', endpoint='admin_user'))
admin.add_view(ModelView(Problem, db.session, name='Problems', endpoint='admin_problem'))
