# -*- coding: utf-8 -*-
import logging
import re
import config
import datetime

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def is_valid_username(username):
    """
    Kiểm tra username hợp lệ
    :param username:
    :return:
    """
    username_pattern = re.compile('^[a-z0-9_-]{3,15}$')
    if username_pattern.match(username):
        return True
    return False


def is_valid_phone_vn(phone):
    """
    Kiểm tra phone hợp lệ
    :param phone:
    :return:
    """
    if not phone:
        return False

    # Validate phone number, must start with 0,84, followed by 9->10 digits only
    phone_pattern = re.compile(r'^(\+)?(03|05|07|08|09|84)(\d{8,9})$')
    trimmed_phone = phone.strip()
    if phone_pattern.match(trimmed_phone):
        return True
    return False


def is_valid_email(email):
    if not email:
        return False
        # Validate email pattern

    email_pattern = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:"
                               "\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    trimmed_email = email.strip()
    if email_pattern.match(trimmed_email):
        return True
    return False


def is_valid_raw_password(password):
    # password_pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    password_pattern = r"(?=.{6,})"
    return bool(re.match(password_pattern, password))


def is_valid_file_extension(filename, extension=None):
    if not extension:
        extension = config.ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in extension


def validate_size(upload_size, save_size):
    return upload_size == save_size


def is_validate_letters_numbers(text):
    pattern = re.compile("^[A-Za-z0-9_-]*$")
    match = pattern.match(text)
    return bool(match)


def is_date_str(date_text, date_format='%Y-%m-%d'):
    try:
        datetime.datetime.strptime(date_text, date_format)
        return True
    except ValueError:
        return False
