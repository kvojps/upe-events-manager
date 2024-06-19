"""add sample data

Revision ID: b59d8aadf84c
Revises: 9ad42850aec4
Create Date: 2024-06-19 11:23:03.524739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b59d8aadf84c'
down_revision: Union[str, None] = '9ad42850aec4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
