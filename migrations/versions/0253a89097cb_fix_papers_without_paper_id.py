"""fix papers without paper_id

Revision ID: 0253a89097cb
Revises: 66fc6eb0e931
Create Date: 2024-07-03 15:04:02.747002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0253a89097cb'
down_revision: Union[str, None] = '66fc6eb0e931'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE papers SET pdf_id = 'paper_' || id;
        """
    )


def downgrade() -> None:
    pass
