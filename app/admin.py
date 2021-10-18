from flask import current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from typing import Any

from .db import db
from .models import User, Celebrity


class BaseModelView:
    def is_accessible(self) -> bool:
        return current_user.is_authenticated


class SecureAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self) -> Any:
        if current_user.is_authenticated and current_user.is_staff:
            return super().index()

        return "Access denied", 403


class UserModelView(BaseModelView, ModelView):
    column_exclude_list = ["password"]


admin = Admin(current_app, index_view=SecureAdminIndexView())
admin.add_view(UserModelView(User, db.session))

# Need endpoint here to avoid collision with other celebrity route.
admin.add_view(ModelView(Celebrity, db.session, endpoint="celebrity_admin"))
