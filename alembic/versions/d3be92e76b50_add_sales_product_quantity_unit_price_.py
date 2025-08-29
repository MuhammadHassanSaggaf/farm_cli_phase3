"""add sales product/quantity/unit_price/total_amount cols

Revision ID: d3be92e76b50
Revises: 86593a4508eb
Create Date: 2025-08-29 04:30:18.571929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3be92e76b50'
down_revision: Union[str, Sequence[str], None] = '86593a4508eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
