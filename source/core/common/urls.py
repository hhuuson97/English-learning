import flask
import flask_login
from . import common_api
from source.utils.users import auth
from source.helpers import languages_helpers, contants, string_helpers


def init_common_api_url():
    common_api.add_url_rule(rule='/', endpoint='home', view_func=redirect_to_home)
    common_api.add_url_rule(rule='/auth/login', endpoint='login', view_func=login, methods=('GET', 'POST',))
    common_api.add_url_rule(rule='/auth/logout', endpoint='logout', view_func=logout)
    common_api.add_url_rule(rule='/auth/forbidden', endpoint='forbidden', view_func=forbidden)
    common_api.add_url_rule(rule='/auth/message', endpoint='auth_message', view_func=auth_message)
    common_api.add_url_rule(rule='/pronunciation', endpoint='pronunciation', view_func=pronunciation)


@flask_login.login_required
def redirect_to_home():
    """ Redirect / to /web
    :return:
    """
    return flask.redirect('/pronunciation')


def login():
    message = None
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        redirect = flask.request.args.get('redirect') or '/'
        if username and password:
            result, message = auth.user_login(username, password)
            if result:
                resp = flask.make_response(flask.redirect(redirect))

                resp.set_cookie(contants.COOKIE_KEY.ACCESS_TOKEN,
                                (result.get(contants.COOKIE_KEY.ACCESS_TOKEN) or {}).get('token'),
                                max_age=7 * 24 * 60 * 60)
                return resp
        else:
            message = languages_helpers.get(contants.MESSAGES.LOGIN_MISS_DATA)
    return flask.render_template('admin/login.html', message=message), 200


def logout():
    auth.user_logout()
    resp = flask.make_response(flask.redirect("/"))

    resp.set_cookie(contants.COOKIE_KEY.ACCESS_TOKEN, max_age=-1)
    return resp


def forbidden():
    return flask.render_template('403.html', message=''), 403


def auth_message():
    return flask.render_template('api_v1/auth_message.html', message=flask.request.args.get("message")), 403

def pronunciation():
    return flask.render_template('pronunciation.html')
