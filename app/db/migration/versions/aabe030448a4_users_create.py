"""users_create

Revision ID: aabe030448a4
Revises: 
Create Date: 2024-02-13 11:47:46.239406

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'aabe030448a4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False, comment='ID'),
    sa.Column('uuid', sa.String(length=36), nullable=False, comment='UUID'),
    sa.Column('account_name', sa.String(length=100), nullable=False, comment='アカウント名'),
    sa.Column('id_account', sa.String(length=100), nullable=False, comment='アカウントID'),
    sa.Column('email', sa.String(length=100), nullable=False, comment='メールアドレス'),
    sa.Column('hashed_password', sa.String(length=100), nullable=False, comment='パスワード'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='アクティブフラグ True:ログイン中 False:ログアウト中'),
    sa.Column('birth_date', sa.Date(), nullable=False, comment='生年月日'),
    sa.Column('other_user_invitation_code', sa.String(length=36), nullable=True, comment='他ユーザー招待コード'),
    sa.Column('refresh_token', sa.String(length=100), nullable=True, comment='リフレッシュトークン'),
    sa.Column('expires_at', sa.DateTime(), nullable=True, comment='リフレッシュトークン有効期限'),
    sa.Column('deleted_at', sa.DateTime(), nullable=True, comment='削除日時とフラグ'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_account'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
