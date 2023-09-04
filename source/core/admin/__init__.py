# coding=utf-8
import logging
import os.path as op
import datetime
import copy

import flask
import flask_admin as fa
import flask_admin.form.fields
import flask_admin.model.form
import markupsafe
import sqlalchemy
from flask import json, current_app
from flask import redirect, request
from flask import url_for
from flask_admin.contrib.sqla import ModelView as AMV
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_login import current_user
from markupsafe import Markup
from werkzeug.utils import secure_filename
from wtforms import TextAreaField
from wtforms.widgets import TextArea


from source.utils.cipher import json_decode
from source.helpers import string_helpers, time_helpers
from source.models.user import UserRole

__author__ = 'VuTNT'
_logger = logging.getLogger(__name__)

hq = fa.Admin(
    name='Hub Connector Admin',
    base_template='my_master.html',
    template_mode='bootstrap4',
    url='/minad'
)

LIST_MODEL_ROLE = {
}


def update_column_formatters(new_value):
    old_data = copy.deepcopy(ModelView.column_formatters)
    old_data.update(new_value or {})
    return old_data


def check_allow_action(obj, action, default_handle):
    if hasattr(obj, 'model'):
        if current_user.role_id in [
            UserRole.super_admin.value
        ] and action == 'delete':
            return False

    return default_handle


def check_visible_menu(obj):
    if not current_user.is_authenticated:
        return False

    if current_user.role_id not in [
        UserRole.super_admin.value,
    ]:
        return False

    if current_user.role_id in [
        UserRole.super_admin.value
    ]:
        return True

    if hasattr(obj, 'model'):
        if obj.model in LIST_MODEL_ROLE.get(current_user.role_id, []):
            return True
    return False


class FilteredAjaxModelLoader(QueryAjaxModelLoader):
    additional_filters = []

    def get_list(self, term, offset=0, limit=10):
        filters = list(
            field.ilike(u'%%%s%%' % term) for field in self._cached_fields
        )
        add_filters = []
        for f in self.additional_filters:
            add_filters.append(f)

        query = self.session.query(self.model).filter(sqlalchemy.or_(*filters), *add_filters)
        return query.all()

    def __init__(self, name, session, model, **options):
        super(FilteredAjaxModelLoader, self).__init__(name, session, model, **options)
        self.additional_filters = options.get('filters') or []


class EnumField(flask_admin.form.fields.Select2Field):
    def __init__(self, column, **kwargs):
        assert isinstance(column.type, sqlalchemy.sql.sqltypes.Enum)

        def coercer(value):
            # coerce incoming value into an enum value
            if isinstance(value, column.type.enum_class):
                return value
            elif isinstance(value, str):
                return column.type.enum_class[value]
            else:
                assert False

        super(EnumField, self).__init__(
            choices=[(v, v) for v in column.type.enums],
            coerce=coercer,
            **kwargs)

    def pre_validate(self, form):
        # we need to override the default SelectField validation because it
        # apparently tries to directly compare the field value with the choice
        # key; it is not clear how that could ever work in cases where the
        # values and choice keys must be different types

        for (v, _) in self.choices:
            if self.data == self.coerce(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class CustomAdminConverter(flask_admin.contrib.sqla.form.AdminModelConverter):
    @flask_admin.model.form.converts("sqlalchemy.sql.sqltypes.Enum")
    def conv_enum(self, field_args, **extra):
        return EnumField(column=extra["column"], **field_args)


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class BaseView(fa.BaseView):
    def is_visible(self):
        return check_visible_menu(self)

    def is_accessible(self):
        return current_user.is_authenticated


class ModelView(AMV):
    model_form_converter = CustomAdminConverter
    can_delete = False
    page_size = 20
    can_set_page_size = True
    can_view_details = True

    column_display_pk = True
    column_default_sort = ('id', True)

    can_create = True
    can_edit = True

    can_export = True
    export_types = ['xls']

    def __init__(self, model, session,
                 name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super().__init__(model, session,
                         name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)

    def is_visible(self):
        return check_visible_menu(self)

    def is_accessible(self):

        if not current_user.is_authenticated:
            return False
        self.can_create = check_allow_action(self, 'create', self.can_create)
        self.can_delete = check_allow_action(self, 'delete', self.can_delete)
        self.can_edit = check_allow_action(self, 'edit', self.can_edit)
        self.can_export = check_allow_action(self, 'export', self.can_export)
        return check_visible_menu(self)

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('app_customer.login', next=request.url))

        return redirect(url_for('app_customer.forbidden', next=request.url))

    def get_value_field(self, model, name):
        value = None
        if '.' in name:
            for itm in name.split('.'):
                if value is None:
                    value = model
                if hasattr(value or model, itm):
                    value = getattr(value or model, itm)
                else:
                    value = None
                    break
        else:
            value = getattr(model, name) if hasattr(model, name) else None

        if value and hasattr(value, 'value'):
            value = getattr(value, 'value')

        return value

    def money_formatter(self, context, model, name):
        value = self.get_value_field(model, name)

        return string_helpers.as_currency(value or 0, symbol='')

    def model_sub_formatter(self, context, model, name):

        id = None
        value = None
        cls_model = None
        if '.' in name:
            cls_model = "".join(name.split(".")[-2:-1])
            for itm in name.split('.'):
                if value is None:
                    value = model
                if hasattr(value or model, itm):
                    id = getattr(value or model, 'id')
                    value = getattr(value or model, itm)
                else:
                    value = None
                    break
        return self._format_item_data(id, value, cls_model)

    def _format_item_data(self, id, value, cls_model):
        lb_code = None
        if id and value:
            if hasattr(value, 'code'):
                lb_code = getattr(value, 'code')
            if hasattr(value, 'id'):
                id = getattr(value, 'id')
            if hasattr(value, 'name'):
                value = getattr(value, 'name')
            label = "%s%s" % (lb_code + "-" if lb_code else '', value)
            return Markup('<a href="%s">%s</a>' % (
                url_for('%s.details_view' % (ModelView.maps_view.get(cls_model) or cls_model), id=id),
                label
            ))
        return ''

    def model_formatter(self, context, model, name):
        id = None
        value = None
        if '.' in name:
            cls_model = "".join(name.split(".")[-1])
            for itm in name.split('.'):
                if hasattr(value or model, itm):
                    id = getattr(value or model, 'id')
                    value = getattr(value or model, itm)
                else:
                    value = None
                    break
        else:
            cls_model = name
            if hasattr(model, name):
                id = getattr(model, 'id')
                value = getattr(model, name)
            else:
                value = None
        return self._format_item_data(id, value, cls_model)

    def _format_json(self, context, model, name):
        val = model.__getattribute__(name)
        if val:
            try:
                val = json.dumps(json_decode(val), indent=2, ensure_ascii=False)
            except ValueError:
                pass
        return markupsafe.Markup('<pre><code>%(val)s</code></pre>') % {
            'val': val,
        }

    def _format_log(self, context, model, name):
        return markupsafe.Markup('<pre><code>%(log)s</code></pre>') % {
            'log': model.__getattribute__(name),
        }

    def _format_status(self, context, model, name):
        """
        :param context:
        :param m.ReceivedMsg model:
        :param name:
        :return:
        """
        return markupsafe.Markup('<span class="label label-%(type)s">%(status)s</span>') % {
            'status': model.status,
            'type': {
                model.Status.ok: 'success',
                model.Status.init: 'info',
            }.get(model.status, 'danger')
        }

    def _format_link_to_object(self, obj):
        cls_name = obj.__class__.__name__
        endpoint = '%s.edit_view' % cls_name.lower()
        link = flask.url_for(
            endpoint,
            id=sqlalchemy.inspect(obj).identity
        )
        return markupsafe.Markup(
            '<a href="%(link)s" target="_blank">%(text)s</a>') % {
                   'link': link,
                   'text': str(obj)
               }

    def _format_link_to_model(self, context, model, name):
        obj = model.__getattribute__(name)
        if obj is None:
            return markupsafe.Markup('<code>None</code>')

        if not isinstance(obj, list):
            return self._format_link_to_object(obj)

        lis = []
        for o in obj:
            li = markupsafe.Markup('<li>%s</li>' % self._format_link_to_object(o))
            lis.append(li)
        return markupsafe.Markup('<ol>%s</ol>' % ''.join(lis))

    def date_utc_format(self, context, model, name):
        if hasattr(model, name) and getattr(model, name):
            return time_helpers.format_db_time_to_user_time(getattr(model, name), format_str='%d/%m/%Y %H:%M:%S')
        return getattr(model, name)

    def prefix_name(obj, file_data):
        parts = op.splitext(file_data.filename)
        name = secure_filename('%s-%s%s' % (string_helpers.gen_uuid(), parts[0], parts[1]))
        return op.join(current_app.config.get('UPLOAD_FOLDER'), "admin", datetime.datetime.utcnow().strftime("%Y%m%d"), name)

    column_formatters = {
        'created_at': date_utc_format,
        'updated_at': date_utc_format,
    }

    form_excluded_columns = [
        'updated_at', 'created_at'
    ]

    USER_GROUP = 'User'
    PAYMENT_GROUP = 'Payment'
    COUPON = 'Coupon'
    TRANSACTION_GROUP = 'Transaction Logs'
    LANGUAGE_FILTER = 'Language Filter'
    MEDIA_GROUP = "Media"


class CustomImageUploadInput(flask_admin.form.ImageUploadInput):
    def get_url(self, field):
        if field.data and field.data.startswith("http"):
            uri = string_helpers.mapping_domain_static(field.data)
        else:
            uri = super().get_url(field)
        return uri


class CustomUploadForm(flask_admin.form.ImageUploadField):
    def __init__(self, label=None, validators=None,
                 base_path=None, relative_path=None,
                 namegen=ModelView.prefix_name, allowed_extensions=None,
                 max_size=None,
                 thumbgen=None, thumbnail_size=(100, 100, False),
                 permission=0o666,
                 url_relative_path=None, endpoint='static',
                 **kwargs):
        if base_path is None:
            base_path = current_app.config.get('STATIC_FOLDER')
        if allowed_extensions is None:
            allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS_IMAGE')

        super().__init__(label, validators,
                         base_path=base_path,
                         relative_path=relative_path,
                         namegen=namegen,
                         allowed_extensions=allowed_extensions,
                         permission=permission,
                         max_size=max_size,
                         thumbgen=thumbgen,
                         thumbnail_size=thumbnail_size,
                         url_relative_path=url_relative_path,
                         endpoint=endpoint,
                         **kwargs)
        self.keep_image_formats = ('GIF', 'PNG',)
        self.widget = CustomImageUploadInput()


def init_app(app, **kwargs):
    """
    Extension initialization point.
    """
    hq.init_app(app)
    # from .user import user
    # from . import http_log
