from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from backend.models import  User
from backend.db import db

admin = Admin(name='ustcoj', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
