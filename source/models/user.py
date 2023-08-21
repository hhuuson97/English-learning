# coding=utf-8
import logging
from datetime import datetime
import enum
import sqlalchemy as sa

from .database import Base
from source.helpers.string_helpers import gen_uuid, build_static_image

_logger = logging.getLogger(__name__)


class UserRole(enum.Enum):
    """Enumerate Roles of User"""
    super_admin = 'super_admin'  # Super Admin, Admin hệ thống
    disabled = 'disabled'  # Bị khoá
    registered = 'registered'

    @classmethod
    def to_dict(cls):
        return cls.__members__.keys()


USER_ROLE_LEVEL = {
    UserRole.super_admin.value: 1,
    UserRole.registered.value: 7,
}


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.String(36), primary_key=True, index=True, default=gen_uuid)
    name = sa.Column(sa.String(80))
    display_name = sa.Column(sa.String(100))
    email = sa.Column(sa.String(120), unique=True)
    phone = sa.Column(sa.String(12), unique=True)
    role_id = sa.Column(sa.Enum(UserRole, native_enum=False), default=UserRole.disabled)
    created_at = sa.Column(sa.DATETIME, default=datetime.utcnow)
    updated_at = sa.Column(sa.DATETIME, onupdate=datetime.utcnow)
    extra_info_raw = sa.Column('extra_info', sa.TEXT, nullable=True)
    username = sa.Column(sa.String(120), unique=True)
    password = sa.Column(sa.String(250))
    avatar = sa.Column(sa.String(255))

    @property
    def role(self):
        return self.role_id

    @role.setter
    def role(self, val):
        self.role_id = val

    def __repr__(self):
        return '%s' % (
            # self.id,
                self.name or self.email or self.phone
        )

    @property
    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            display_name=self.display_name,
            phone=self.phone,
            email=self.email,
            username=self.username,
            role_id=self.role_id.value if self.role_id else None,
            avatar=build_static_image(self.avatar),
        )
