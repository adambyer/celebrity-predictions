from flask import current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
# from flask_login import current_user
from typing import Any

from ..api.db import Session
from ..api.models import User, Celebrity


class BaseModelView(ModelView):
    column_display_pk = True

    # def is_accessible(self) -> bool:
    #     return current_user.is_authenticated


class SecureAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self) -> Any:
        # if current_user.is_authenticated and current_user.is_staff:
        return super().index()

        # return "Access denied", 403


class UserModelView(BaseModelView):
    column_exclude_list = ["password"]


admin = Admin(current_app, index_view=SecureAdminIndexView())
admin.add_view(UserModelView(User, Session()))

# Need endpoint here to avoid collision with other celebrity route.
admin.add_view(BaseModelView(Celebrity, Session(), endpoint="celebrity_admin"))
