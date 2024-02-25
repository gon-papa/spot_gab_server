"""create_email_verifications_1_on_1_change

Revision ID: 770998b477ca
Revises: 80bbbe1d7643
Create Date: 2024-02-25 04:20:25.335281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             


# revision identifiers, used by Alembic.
revision: str = '770998b477ca'
down_revision: Union[str, None] = '80bbbe1d7643'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'email_verifications', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'email_verifications', type_='unique')
    # ### end Alembic commands ###
