# coding=utf-8
""" Store configurations for Flask in 3 main modes:
  Development & Testing & Production

"""
import logging
import os

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

ROOT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
))
# The environment to run this config. This value will affect to the
# configuration loading
#
# it can be: dev, test, stag, prod
ENV_MODE = os.environ.get('ENV_MODE', '').upper()

DEBUG = False
TESTING = False
LOGGING_CONFIG_FILE = os.path.join(ROOT_DIR, 'logging.ini')

SEEDS_DIR = os.path.join(
    ROOT_DIR,
    'migrations',
    'seeds',
)

FLASK_APP_SECRET_KEY = 'SL5@$yB9WFaP6|7l&cQfLxq_vYT*$fsIAE?Rl:Z6'
ERROR_404_HELP = False

STATIC_FOLDER = os.path.join(ROOT_DIR, 'source/templates', 'static')
RESTPLUS_VALIDATE = True

SQLALCHEMY_DATABASE_URI = None
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

ACCESS_TOKEN_COOKIE_NAME = 'access_token'
CELERY_BROKER_URL = 'redis://localhost:6379',
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Caching
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = '6379'

CACHE_KEY_PREFIX = "flask_cache_%s_%s_" % ("GAM", ENV_MODE)
# Swagger
SWAGGER_UI_REQUEST_DURATION = True
SWAGGER_UI_DEFAULT_MODELS_EXPAND_DEPTH = "-1"

# CDN static
DOMAIN_STATIC = 'http://127.0.0.1:5000/'

_IGNORED_CONFIG = (
    'ROOT_DIR',
    'STATIC_DIR',
    'ENV_MODE',
    'CACHE_KEY_PREFIX'
)

# FILE UPLOAD CONFIG
UPLOAD_FOLDER = "uploads"
UPLOAD_FOLDER_PATH = "%s/%s" % (STATIC_FOLDER, UPLOAD_FOLDER)
ALLOWED_EXTENSIONS_IMAGE = ['webp', 'svg', 'bmp', 'png', 'jpg', 'jpeg', 'jpe', 'gif', "webp"]
ALLOWED_EXTENSIONS_VIDEO = ['webm', 'ogg', 'mp4', "webm"]
ALLOWED_EXTENSIONS_AUDIO = ['aac', 'ogg', 'mp3']
ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS_IMAGE + ALLOWED_EXTENSIONS_VIDEO + ALLOWED_EXTENSIONS_AUDIO

MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
URL_DOWNLOAD = "/uploads/%s"  # config nginx

JWT_TOKEN = 'wescan2020#@'
JWT_ALG = 'HS256'

PASS_SALT = "124xvs5dv"

TIME_CACHE_USER = 7 * 24 * 60 * 60

COUPON_RANDOM_LENGTH = 8

MAX_LIMIT_PER_PAGE = 1000

DOMAIN_API = ""
