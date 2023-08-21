import base64
import binascii
import copy
import datetime
import enum
import hashlib
import json
import os
import uuid
import re
from decimal import Decimal
from urllib.parse import urlencode

from flask import current_app, has_app_context, has_request_context, request as flask_request, url_for

from .time_helpers import date_str_to_utc_obj, datetime_to_utc
from .validate import is_valid_phone_vn


def gen_str_uuid():
    return str(uuid.uuid4())


def gen_uuid():
    return gen_str_uuid().replace("-", "")


def md5(str):
    if not str:
        return None
    return hashlib.md5(str.encode('utf-8')).hexdigest()


def base64_enc(message, url_safe=False):
    message_bytes = message.encode('utf-8') if not isinstance(message, bytes) else message
    base64_bytes = base64.urlsafe_b64encode(message_bytes) if url_safe else base64.b64encode(message_bytes)
    return base64_bytes.decode('utf-8')


def base64_dec(message):
    base64_bytes = message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')


def random_prefix(length=6, map=None):
    rand_int = int(os.urandom(length).hex(), 16)
    # const_map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    const_map = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789"
    if map:
        const_map = map
    rand_str = ""
    len_str = len(const_map)
    for i in range(length):
        rand_str += const_map[rand_int % len_str]
        rand_int //= len_str
    return rand_str[::-1]


def random_prefix_uncase(length=6):
    return random_prefix(length, map="ABCDEFGHJKMNPQRSTUVWXYZ23456789")


def random_numberic(length=6):
    return random_prefix(length, map="0123456789")


def unique_from_timestamp():
    return '%s%s' % (
        base64_enc(str(round(datetime.datetime.utcnow().microsecond / 1000)).zfill(3), True),
        int((datetime.datetime.utcnow() - datetime.datetime(2020, 1, 2, 3, 4, 5, 678910)).total_seconds())
    )


def format_us_currency(value, split_group=',', symbol='$'):
    if not value:
        return ""
    value = str(value).split('.')[0]
    if value.count(split_group) == 0:
        b, n, v = '', 1, value
        value = value[:value.rfind('.')]
        for i in value[::-1]:
            b = split_group + i + b if n == 2 else i + b
            n = 1 if n == 3 else n + 1
        b = b[1:] if b and len(b) > 0 and b[0] == split_group else b
        value = (b or "") + v[v.rfind('.'):]
    return symbol + (value.rstrip('0').rstrip('.') if '.' in value else value)


def format_vn_currency(value, split_group=None, symbol=''):
    if split_group is None:
        split_group = [',', '.']
    if not value:
        return ""
    value = str(value).split('.')
    r = ''
    i = 0
    if len(value) > 1:
        r += value[1][::-1] + split_group[1]
    for v in value[0][::-1]:
        if i % 3 == 0 and i > 0:
            r += split_group[0]
        r += v
        i += 1
    ret = r[::-1]
    if symbol:
        ret += " " + symbol
    return ret


def is_int(key, default=None):
    try:
        return int(key)
    except:
        return default


def is_decimal(key, default=0):
    try:
        return float(key)
    except:
        return default


def is_bool(key):
    if isinstance(key, (bool)):
        return key
    return key and key.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


def build_static_image(image, with_domain=True, with_real_path=False):
    if not image:
        return ""
    if image.startswith("http"):
        return image
    if with_real_path or not has_request_context():
        return current_app.config['STATIC_FOLDER'].rstrip("/") + "/" + image

    if with_domain:
        return current_app.config.get('DOMAIN_STATIC', '').strip("/") + url_for('static', filename=image)

    return url_for('static', filename=image)


def build_static_audio(image, with_domain=True, with_real_path=False):
    return build_static_image(image, with_domain, with_real_path)


def build_static_upload(file_path, with_domain=True, with_real_path=False):
    return build_static_image(file_path, with_domain, with_real_path)


def mapping_domain_static(image):
    if not image:
        return ""
    if image.startswith("http"):
        return image
    return current_app.config.get('DOMAIN_STATIC', '').strip("/") + image


def hash_password(password):
    """
    Mã hoá mật khẩu của user
    :param password:
    :return:
    """
    if not password:
        return None
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        current_app.config.get('PASS_SALT').encode('utf-8'),
        100000
    )
    return binascii.hexlify(dk).decode("utf-8")


def check_password(password, hash_str):
    """
    Kiễm tra chuỗi mật khẩu của user
    :param password:
    :param hash_str:
    :return:
    """
    str_enc = hash_password(password)
    return str_enc == hash_str


def json_default(o, input_format=None, output_date_format=None, convert_date=None, iso_date=False, convert_bool=None, format_image=None):
    if convert_date and output_date_format:
        timezone = 7
        if has_app_context() and has_request_context():
            query = flask_request.args or {}
            timezone = is_int(query.get('timezone'), 7)

        if isinstance(o, (datetime.date, datetime.datetime)):
            obj_date = datetime_to_utc(o)
            if obj_date:
                return (obj_date + datetime.timedelta(hours=timezone)).strftime(output_date_format)
        if isinstance(o, str):
            obj_date = date_str_to_utc_obj(o, format_str=input_format, timezone='UT')
            if obj_date:
                return (obj_date + datetime.timedelta(hours=timezone)).strftime(output_date_format)
    if isinstance(o, (datetime.date, datetime.datetime)):
        if iso_date:
            return o.isoformat()
        elif output_date_format:
            return o.strftime(output_date_format)
        return o.strftime("%d/%m/%Y")
    if isinstance(o, float):
        return int(format(o, '.0f'))
    if isinstance(o, enum.Enum):
        return o.value
    if isinstance(o, Decimal):
        return float(format(o, '.0f'))
    if convert_bool:
        return is_bool(o)
    if format_image:
        return build_static_image(o)
    return o


def json_dumps(data, default=None, new_line=True):
    if not data:
        return default

    try:
        value = json.dumps(data, sort_keys=True, indent=1, default=json_default)
        if not new_line:
            value = value.replace('\n', '')
        return value
    except Exception as e:
        return default


def json_loads(data, default=None):
    if not data:
        return default

    try:
        return json.loads(data)
    except:
        return default


def json_find_path(path, data, default=None):
    keys = path.split('.')
    rv = data
    for xkey in keys:
        matches = re.search(r"(.*)\[(\d)\]", xkey, re.DOTALL)
        key = xkey
        index = None
        if matches:
            key = matches.group(1)
            index = int(matches.group(2))
        if not isinstance(rv, (dict, tuple)) or key not in rv:
            rv = default
            break
        rv = rv[key]
        if index is not None and isinstance(rv, list):
            if index >= len(rv):
                rv = default
                break
            rv = rv[index]
    return rv or default


def to_phone_number_international(phone):
    if not is_valid_phone_vn(phone):
        return phone

    if phone.startswith("+84"):
        return phone[3:]

    if phone.startswith("84"):
        return "0" + phone[2:]
    return phone


def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def parse_vnpay_datetime(dt):
    if len(dt) != 14:
        return datetime.datetime.now()
    par_time = datetime.datetime.strptime(dt, '%Y%m%d%H%M%S')
    if par_time <= datetime.datetime.now():
        return par_time
    return datetime.datetime.now()


def parse_momo_datetime(dt):
    par_time = datetime.datetime.strptime(dt, '%d/%m/%Y - %H:%M')
    if par_time <= datetime.datetime.now():
        return par_time
    return datetime.datetime.now()


def asdict_json(obj, date_field=None, date_format=None, output_format=None, iso_date=False, bool_field=None, image_field=None):
    if not obj:
        return obj
    if not isinstance(obj, dict):
        _dict = copy.deepcopy(obj._asdict())
    else:
        _dict = obj
    if not date_format:
        date_format = "%d/%m/%Y"
    if not date_field:
        date_field = []
    if not bool_field:
        bool_field = []
    if not image_field:
        image_field = []

    for (key, value) in _dict.items():
        _dict[key] = json_default(value, input_format=date_format, output_date_format=output_format,
                                  convert_date=key in date_field, iso_date=iso_date, convert_bool=key in bool_field,
                                  format_image=key in image_field)
    return _dict


def as_currency(amount, symbol='$', sym_left=False):
    return (symbol if sym_left else "") + '{:,.0f}'.format(amount) + (symbol if not sym_left else "")


def hide_phone_number(phone):
    if not phone:
        return phone
    return phone[:2] + "***" + phone[-3:]


def create_sig_params(key=None, **kwargs):
    data = key or "abc124"
    for k, v in kwargs.items():
        data += str(k) + "=" + str(v) + "&"
    return md5(data)


def validate_sig_params(key=None, sig=None, **kwargs):
    valid_sig = create_sig_params(key=key, **kwargs)
    return valid_sig == sig


def dict_to_query_str(**kwargs):
    return urlencode(query=kwargs)


def replace_html_template(text, data):
    if not data:
        return text

    for k, v in data.items():
        text = text.replace("{{" + str(k) + "}}", v)
    return text


def replace_list_str(data, search_str, replace_str):
    if not data or search_str is None or replace_str is None:
        return data

    if not isinstance(search_str, (list)):
        search_str = [search_str]

    if not isinstance(replace_str, (list)):
        replace_str = [replace_str]

    for text in search_str:
        index = search_str.index(text)
        data = data.replace(text, replace_str[index] if index < len(replace_str) else replace_str[0])
    return data


def parse_number_from_str(text):
    # m = re.search(r"(\d*\.?\d*)", text)
    data = re.findall(r'\d+', text)
    return "".join(data)


def to_list(data, split_str=","):
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.split(split_str)


def build_regex_filter(regex_list):
    return "|".join(["(" + regex + ")" for regex in regex_list])


def build_regex_filter_words(regex_list):
    return "|".join(["(" + regex + "\\b)" for regex in regex_list])
