"""create-users

Revision ID: a9b68e4450aa
Revises: 
Create Date: 2024-02-03 16:26:26.523683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision: str = 'a9b68e4450aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False)            , default=uuid.uuid4, nullable=False, comment='ID'),
    sa.Column('account_name', sa.String(length=100), nullable=False, comment='アカウント名'),
    sa.Column('id_account', sa.String(length=100), nullable=False, comment='アカウントID'),
    sa.Column('email', sa.String(length=100), nullable=False, comment='メールアドレス'),
    sa.Column('hashed_password', sa.String(length=100), nullable=False, comment='パスワード'),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='アクティブフラグ True:ログイン中 False:ログアウト中'),
    sa.Column('birth_date', sa.Date(), nullable=False, comment='生年月日'),
    sa.Column('other_user_invitation_code', sqlalchemy_utils.types.uuid.UUIDType(binary=False)            , default=uuid.uuid4, nullable=True, comment='他ユーザー招待コード'),
    sa.Column('deleted_at', sa.Date(), nullable=True, comment='削除日時とフラグ'),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp on update current_timestamp'), nullable=False, comment='更新日時'),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_account'),
    sa.UniqueConstraint('uuid'),
    comment='ユーザー情報テーブル'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###