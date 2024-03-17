"""create_password_reset

Revision ID: 4b72a833bdc3
Revises: 5c3fa0bfa365
Create Date: 2024-03-14 23:18:56.648988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             


# revision identifiers, used by Alembic.
revision: str = '4b72a833bdc3'
down_revision: Union[str, None] = '5c3fa0bfa365'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('password_reset_verifications',
    sa.Column('id', sa.Integer(), nullable=False, comment='ID'),
    sa.Column('user_id', sa.Integer(), nullable=False, comment='ユーザーID'),
    sa.Column('email', sa.String(length=100), nullable=False, comment='メールアドレス'),
    sa.Column('verify_token', sa.String(length=100), nullable=True, comment='パスワードリセットトークン'),
    sa.Column('verified_expired_at', sa.TIMESTAMP(timezone=True), nullable=True, comment='パスワードリセット有効期限'),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('password_reset_verifications')
    # ### end Alembic commands ###
