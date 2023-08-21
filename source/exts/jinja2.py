# coding=utf-8
import enum
import logging
import datetime
# from source.helpers import number_spelling

__author__ = 'Kee'
_logger = logging.getLogger(__name__)


def init_app(app, **kwargs):
    """ Init Jinja2 filters for an app

    :param flask.Flask app:
    :param kwargs:
    :return:
    """
    app.jinja_env.filters['enum_label'] = jinja2_enum_label_filter
    app.jinja_env.filters['compare_time'] = compare_time
    app.jinja_env.filters['complete_time'] = complete_time
    app.jinja_env.filters['convert_time_from'] = convert_time_from
    # app.jinja_env.filters['number_to_words'] = number_to_words
    app.jinja_env.filters['hash_text'] = hash_text


def jinja2_enum_label_filter(e):
    """ Give out the corresponding label for an enum value

    :param e:
    :return: the label
    :rtype: str
    >>> jinja2_enum_label_filter('aa')
    'aa'
    >>> class XXX(enum.Enum):
    ...     a = 'a'
    ...     b = 'b'
    >>> jinja2_enum_label_filter(XXX.a)
    'a'
    """
    labels = {
    }

    if not isinstance(e, enum.Enum):
        return e

    try:
        return labels[e]
    except KeyError:
        return e.value


def compare_time(t1, t2):
    """

    :param t1:
    :param t2:
    :return:
    >>> dt1 = datetime.datetime.now()
    >>> compare_time(dt1, dt1)
    False
    >>> compare_time(dt1, dt1 + datetime.timedelta(hours=1))
    True
    """

    time1 = t1.strftime('%Y:%m:%d %H:%M')
    time2 = t2.strftime('%Y:%m:%d %H:%M')

    if time1 >= time2:
        return False
    else:
        return True


def convert_time_from(t, format_str):
    """

    :param t:
    :param format_str:
    :return:
    >>> now = datetime.datetime(year=2030, month=10, day=10)
    >>> convert_time_from(now, '%Y')
    '2030'
    """
    return t.strftime(format_str)


intervals = (
    ('tuần', 604800),  # 60 * 60 * 24 * 7
    ('ngày', 86400),    # 60 * 60 * 24
    ('giờ', 3600),    # 60 * 60
    ('phút', 60),
)


def complete_time(start_time, end_time=None, granularity=2):
    """

    :param start_time:
    :param end_time:
    :param granularity:
    :return:

    >>> complete_time(datetime.datetime.now() - datetime.timedelta(days=-3))
    '-1 tuần, 4 ngày'
    >>> complete_time(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=8))
    '1 tuần, 1 ngày'
    """
    if not end_time:
        end_time = datetime.datetime.now()

    end_time = (end_time - datetime.datetime(1970, 1, 1)).total_seconds()
    start_time = (start_time - datetime.datetime(1970, 1, 1)).total_seconds()

    seconds = int(end_time - start_time)

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


# def number_to_words(number):
#     """
#     >>> number_to_words(1)
#     'một'
#     """
#     number = str(int(float(number)))
#     spelling = number_spelling.VietnameseNumberSpelling()
#
#     return spelling.number_to_word(number)


def hash_text(text):
    """

    :param text:
    :return:
    >>> hash_text('The quick brown fox jumps over the lazy dog')
    '4756ce3ec90d93f702bb3a6c153f30a0'
    """
    import hashlib

    random_str = 'random_string' + str(text)
    text = random_str.encode('utf-8')
    m = hashlib.md5()
    m.update(text)

    return m.hexdigest()
