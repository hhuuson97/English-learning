# coding=utf-8
""" Module này chứa các phần liên quan đến phân quyền và cấu trúc quyền truy cập.

Sử dụng Flask-Principal

"""
import logging
import flask_login
import flask_principal as _fp

from source.models.user import UserRole

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

principal = _fp.Principal(skip_static=True, use_sessions=False)
super_admin_perm = _fp.Permission(_fp.RoleNeed(UserRole.super_admin.value))


class BasePermission(_fp.Permission):

    def __init__(self, need):
        super().__init__(*need)

    def init_base_need(self):
        """ Admin và super_admin có thể làm mọi hành động

        :return:
        """
        return super_admin_perm.needs

    def init_super_admin_need(self):
        """ Admin và super_admin có thể làm mọi hành động

        :return:
        """
        return super_admin_perm.needs


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    principal.init_app(app)

    _fp.identity_loaded.connect_via(app)(on_identity_loaded)


@principal.identity_loader
def _load_identity_from_request():
    """ Load identity before request
    """
    user = flask_login.current_user  # type: source.exts.login_manager.User
    if not user.is_authenticated:
        return None

    identity = _fp.Identity(user.user_id)
    return identity


def on_identity_loaded(app, identity):
    """ Called when the identity loaded. It will load all identity's providing
    needs

    :param flask.Flask app: current app
    :param _fp.Identity identity: the loaded identity
    :return:
    """
    user = flask_login.current_user  # type: source.exts.login_manager.User

    # Add user role
    identity.provides.add(_fp.RoleNeed(user.role_id))

    # Add chính User đó
    identity.provides.add(_fp.UserNeed(user.user_id))
