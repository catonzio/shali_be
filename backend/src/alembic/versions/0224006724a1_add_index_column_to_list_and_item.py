"""Add index column to list and item

Revision ID: 0224006724a1
Revises: e3b7a49756e7
Create Date: 2023-10-06 16:55:03.369679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0224006724a1'
down_revision: Union[str, None] = 'e3b7a49756e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('lists', sa.Column('index', sa.INTEGER(), nullable=False))
    op.add_column('items', sa.Column('index', sa.INTEGER(), nullable=False))


def downgrade() -> None:
    op.drop_column('lists', 'index')
    op.drop_column('items', 'index')
