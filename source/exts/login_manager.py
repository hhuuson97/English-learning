# coding=utf-8
import logging

import flask
import flask_login

from source.core.api.v1.exception import on_error
from source.helpers import languages_helpers, contants
from source.models.user import User
from source.utils.users import auth

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

login_manager = flask_login.LoginManager()


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    login_manager.init_app(app)


class UserObject(object):
    """Provide User object for LoginManager class"""

    def __init__(self, user_id, user_obj):
        """
        :param str user_id: it is access token
        :param models.User obj: the user object
        """
        self.is_authenticated = True
        self.is_active = user_obj.get('need_update_info') is None  # Need update mean not already account
        self._id = user_id  # access token
        self.user = user_obj
        self.sid = user_obj.get('sid')
        self.user_id = user_obj.get('id')
        self.name = self.user.get('name')
        self.display_name = user_obj.get('display_name')
        self.email = self.user.get('email') or None
        self.phone = self.user.get('phone') or None
        self.role_id = self.user.get('role_id')
        self.action = self.user.get('action') or []

    def get_id(self):
        return self._id


@login_manager.request_loader
def load_user_from_request(request):
    """ Load Authenticated User from request

    :param flask.Request request: the request
    :return: User or None
    :rtype: User|None
    """
    access_token = None
    try:
        if 'Authorization' in flask.request.headers:
            access_token = flask.request.headers['Authorization']
        elif contants.COOKIE_KEY.ACCESS_TOKEN in flask.request.cookies:
            access_token = flask.request.cookies[contants.COOKIE_KEY.ACCESS_TOKEN]

    except KeyError:
        return None
    if not access_token:
        return None

    user_info = auth.validate_jwt_token(access_token)
    if user_info:
        return UserObject(
            user_id=access_token,
            user_obj=user_info,
        )

    return None


@login_manager.unauthorized_handler
def on_user_unauthorized():
    """ Be called when an unauthorized user need to be authenticated
    """
    if flask.has_app_context():
        content_type = flask.request.headers.get('Content-Type')
        if content_type and 'json' in content_type:
            return on_error(401, languages_helpers.get(contants.MESSAGES.HTTP_401))
    return flask.redirect("/auth/login")
