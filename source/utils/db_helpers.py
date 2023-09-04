# coding=utf-8
import logging

from sqlalchemy import text
from source.models.database import get_engine
from source.helpers.contants import MESSAGES

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)


def add_debug_sql(obj_orm):
    from sqlalchemy.dialects import mysql
    print(str(obj_orm.statement.compile(
        dialect=mysql.dialect(),
        compile_kwargs={"literal_binds": True})))


def get_current_enum(table, column):
    results = []
    sql = "SHOW COLUMNS FROM %s WHERE Field = '%s';" % (table, column)
    data = get_engine().execute(text(sql))
    for row in data:
        if 'enum(' in row[1]:
            col_type = row[1].replace('enum(', '').replace(')', '').replace("'", "")
            results = col_type.split(',')
    return results


def update_enum_table(table, column, new_value=None, old_list=None, force_empty=False):
    if old_list is None:
        old_list = get_current_enum(table, column)

    # Từ chối cập nhật nếu danh sách enum là rỗng. Có thể account của bạn không đủ quyền lấy danh sách enum của field
    if len(old_list) == 0 and not force_empty:
        return
    if new_value:
        if not isinstance(new_value, list):
            new_value = [new_value]
        for value in new_value:
            if value not in old_list:
                old_list.append(value)

    str_enum = "'" + ("','".join(old_list)) + "'"
    sql = """ALTER TABLE `{table}` CHANGE COLUMN `{col}` `{col}` ENUM( {enum}) NULL DEFAULT NULL ;""".format(**{
        "table": table,
        "col": column,
        "enum": str_enum
    })
    get_engine().execute(text(sql))


def delete_row_and_update_enum(table, column, rm_ls_enum, default_value=None):
    if not table or not column or not rm_ls_enum:
        return
    if not isinstance(rm_ls_enum, list):
        rm_ls_enum = [rm_ls_enum]
    ls_enum = get_current_enum(table, column)
    for rm_enum in rm_ls_enum:
        if rm_enum in ls_enum:
            sql = "UPDATE `{table}` SET `{col}` = NULL WHERE `{col}` = '{value}';".format(**{
                "table": table,
                "col": column,
                "value": rm_enum
            })
            get_engine().execute(text(sql))
            ls_enum.remove(rm_enum)

    update_enum_table(table, column, ls_enum)


def parse_concat(data, fields, is_list=True, field_concat='|', group_concat='||', func_mapping=None):
    if not data or not fields:
        return [] if is_list else {}

    parse_data = data.split(group_concat)
    results = []
    for itm in parse_data:
        result = {}
        itm_data = itm.split(field_concat) or []
        idx = 0
        for field in fields:
            value = (func_mapping(field, itm_data[idx]) if func_mapping else itm_data[idx]) if idx < len(
                itm_data) else None
            if value == MESSAGES.NULL_KEY:
                value = ""
            result[field] = value
            idx += 1
        results.append(result)

    return results if is_list else (results[0] if len(results) > 0 else {})


class MakeObjectSubscriptAble(object):
    def __init__(self, info):
        for key in info:
            self.__setattr__(key, info[key])

    def __getitem__(self, item):
        return self.__getattribute__(item)
