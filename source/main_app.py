# coding=utf-8
import json
import logging
import flask
import os
import flask_migrate
from flask_cors import CORS
from source import helpers
from .models.database import db_session, init_db, init_engine_all, Base
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_babelex import Babel

__author__ = 'son.hh'
_logger = logging.getLogger('root')


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = "*"

    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    return response


def teardown_appcontext(exception=None):
    try:
        db_session.commit()
    except Exception as e:
        _logger.warning('teardown_request: commit db session fail: %s' % str(e))

    db_session.remove()


def teardown_request(exception=None):
    try:
        db_session.commit()
    except Exception as e:
        _logger.warning('teardown_request: commit db session fail: %s' % str(e))

    db_session.remove()


def get_env(name, default, env_mode):
    """ Get configuration from environment in priorities:
      1. the env var with prefix of $ENV_MODE
      2. the env var with the same name (in upper case)
      3. the default value

    :param str name: configuration name
    :param default: default value
    :param env_mode: env str
    """

    def _bool(val):
        if not val:
            return False
        return val not in ('0', 'false', 'no')

    # make sure configuration name is upper case
    name = name.upper()

    # try to get value from env vars
    val = default
    for env_var in ('%s_%s' % (env_mode, name), name):
        try:
            val = os.environ[env_var]
            break
        except KeyError:
            pass
    else:
        env_var = None

    # convert to the right types
    if isinstance(default, bool):
        val = _bool(val)

    if isinstance(default, int):
        val = int(val)
    return env_var, val


def load_config_os(app):
    _settings = {}
    env_mode = app.config.get('ENV_MODE')
    _IGNORED_CONFIG = app.config.get('_IGNORED_CONFIG')
    _vars = list(app.config.keys())
    for name in _vars:
        if name in _IGNORED_CONFIG:
            continue
        if not name.startswith('_') and name.isupper():
            env_var, val = get_env(name, app.config.get(name), env_mode)
            if env_var:
                _settings[name] = val

    app.config.update(_settings)


def load_config_current_db(app):
    if app.config.get('DB_HOST'):
        db_path = '{driver}://{user}:{pass}@{host}:{port}/{database}?charset={charset}'.format(**{
            "driver": app.config.get('DB_DRIVER'),
            "host": app.config.get('DB_HOST'),
            "port": app.config.get('DB_PORT'),
            "user": app.config.get('DB_USERNAME'),
            "pass": app.config.get('DB_PASSWORD'),
            "database": app.config.get('DB_DATABASE'),
            'charset': app.config.get('DB_CHARSET') or 'utf8mb4'
        })
        app.config.update({
            "SQLALCHEMY_DATABASE_URI": db_path
        })


def load_app_config(app):
    # instance_config_file = 'config_%s.py' % config.ENV_MODE.lower()
    # import config
    # app.config.from_object(config)
    app.config.from_pyfile('../config.py', silent=True)
    app.config.from_pyfile('../instance/config.py', silent=True)
    app.static_folder = app.config.get('STATIC_FOLDER')

    if app.config.get('ALL_CONFIGS'):
        additional_config = json.loads(app.config.get('ALL_CONFIGS'))
        app.config.update(additional_config)

    load_config_os(app)
    load_config_current_db(app)


def config_logger(app):
    import logging.config
    logging.config.fileConfig(app.config['LOGGING_CONFIG_FILE'],
                              disable_existing_loggers=False)


def create_app():
    """ Create Flask application based on env_name
    :rtype: flask.Flask
    """
    app = flask.Flask(
        __name__,
        instance_relative_config=True,
    )
    app.url_map.strict_slashes = False

    load_app_config(app)
    config_logger(app)
    app.instance_path = os.path.join(app.config.get('ROOT_DIR'), 'instance')
    app.secret_key = app.config.get('FLASK_APP_SECRET_KEY')

    # app.after_request(after_request)
    app.teardown_appcontext(teardown_appcontext)
    app.teardown_request(teardown_request)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    return app


def init_exts(app):
    from .exts import init_app
    init_app(app)


def init_migrate(app, db):
    migrate = flask_migrate.Migrate(db=Base)
    migrate.init_app(app)


def init_api(app):
    from source.core import init_app
    init_app(app)


def init_cmd(app):
    from source.commands import init_cmds
    init_cmds(app)


def init_cors(app):
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


def init_language(app):
    from source.helpers.languages_helpers import init_languages
    init_languages(app)


def init_cache(app):
    from source.utils.setting_utils import init_all_setting
    init_all_setting()


def init_babel(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        if flask.request.args.get('lang'):
            flask.session['lang'] = flask.request.args.get('lang')
        return flask.session.get('lang', 'vi')


def init_app(app):
    db_config = {
        "echo": False,
        "pool_pre_ping": True,
        "isolation_level": "READ COMMITTED"
    }
    init_engine_all(app.config, **db_config)
    init_db(app)
    init_babel(app)
    init_exts(app)
    init_migrate(app, db_session)
    init_language(app)
    init_api(app)
    init_cmd(app)
    init_cors(app)
    init_cache(app)
    _logger.debug('Start app with database: %s' % app.config['SQLALCHEMY_DATABASE_URI'])
