"""add to users column telegram_id

Revision ID: e57aa7622157
Revises: a6ab280ab596
Create Date: 2024-12-13 16:46:33.881029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e57aa7622157'
down_revision: Union[str, None] = 'a6ab280ab596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column telegram_id to the users table
    op.add_column('users', sa.Column('telegram_id', sa.String(length=50), unique=True, nullable=True))


def downgrade() -> None:
    # Remove the telegram_id column from the users table
    op.drop_column('users', 'telegram_id')
