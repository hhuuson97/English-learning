"""Init database

Revision ID: 409e91ec78c2
Revises: 
Create Date: 2023-08-22 12:25:37.134530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '409e91ec78c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dictionary',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word', sa.String(length=80), nullable=True),
    sa.Column('ipa', sa.String(length=80), nullable=True),
    sa.Column('mean', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('env_settings',
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('group', sa.String(length=256), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('display_for_web', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('http_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('header', sa.Text(), nullable=True),
    sa.Column('method', sa.String(length=20), nullable=True),
    sa.Column('param', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('response', sa.Text(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('user_agent', sa.String(length=400), nullable=True),
    sa.Column('client_ip', sa.String(length=50), nullable=True),
    sa.Column('uri_pattern', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('http_logs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_http_logs_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_http_logs_uri_pattern'), ['uri_pattern'], unique=False)
        batch_op.create_index(batch_op.f('ix_http_logs_user_id'), ['user_id'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('display_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.Column('role_id', sa.Enum('super_admin', 'disabled', 'registered', name='userrole', native_enum=False), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('extra_info', sa.TEXT(), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=250), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_id'))

    op.drop_table('users')
    with op.batch_alter_table('http_logs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_http_logs_user_id'))
        batch_op.drop_index(batch_op.f('ix_http_logs_uri_pattern'))
        batch_op.drop_index(batch_op.f('ix_http_logs_created_at'))

    op.drop_table('http_logs')
    op.drop_table('env_settings')
    op.drop_table('dictionary')
    # ### end Alembic commands ###