import logging
import os

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

ENV_MODE = 'DEV'

DEBUG = True
TESTING = True

LOGGING_CONFIG_FILE = os.path.join('instance', 'logging-dev.ini')

FLASK_APP_SECRET_KEY = 'SL5@$yB9WFaP6|7l&cQfLxq_vYT*$fsIAE?Rl:Z6'
ERROR_404_HELP = False

RESTPLUS_VALIDATE = True

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://english-learning:280596dtph!@34.147.207.76:3306/mysql1?charset=utf8mb4"

# Caching
CACHE_TYPE = 'simple'
CACHE_KEY_PREFIX = "flask_cache_%s_" % (ENV_MODE)