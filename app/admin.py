from flask import current_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .db import db
from .models import User


class UserModelView(ModelView):
    column_exclude_list = ["password"]


admin = Admin(current_app)
admin.add_view(UserModelView(User, db.session))
