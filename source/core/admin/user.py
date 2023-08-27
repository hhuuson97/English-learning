import logging

__author__ = 'son.hh'
_logger = logging.getLogger(__name__)

# coding=utf-8
import logging

from source.models.user import User
from source.models.database import db_session
from source.utils.user_utils import hash_password, update_cache_user
from wtforms import StringField
from . import hq, ModelView

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


class UserView(ModelView):
    column_default_sort = ('id', True)
    column_filters = [
        'email',
        'phone',
        'role_id',
    ]
    column_list = [
        'email',
        'phone',
        'role_id',
    ]
    form_columns = [
        'phone',
        'role_id',
        'email',
        'new_password'
    ]

    form_extra_fields = {
        'new_password': StringField(
            default='',
            label='Mật khẩu'
        ),
    }

    def on_model_change(self, form, model, is_created):
        if form.new_password and form.new_password.data:
            model.password = hash_password(form.new_password.data)

    # def after_model_change(self, form, model, is_created):
    #     update_cache_user(model)


hq.add_view(UserView(User, db_session, name='Người dùng'))
