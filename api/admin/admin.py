from flask import current_app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

# TODO: auth
# from flask_login import current_user
from typing import Any

from ..db import Session
from ..models import User, Celebrity, Prediction, PredictionResult


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
    form_excluded_columns = ["predictions"]


class CelebrityModelView(BaseModelView):
    column_exclude_list = ["twitter_profile_image_url", "twitter_description"]
    form_excluded_columns = ["predictions"]


class PredictionModelView(BaseModelView):
    form_excluded_columns = ["results"]


admin = Admin(current_app, index_view=SecureAdminIndexView())
admin.add_view(UserModelView(User, Session()))
admin.add_view(CelebrityModelView(Celebrity, Session()))
admin.add_view(PredictionModelView(Prediction, Session()))
admin.add_view(BaseModelView(PredictionResult, Session()))
