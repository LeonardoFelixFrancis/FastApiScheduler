"""Added username

Revision ID: 7746c33ee5f0
Revises: bdfaa381e849
Create Date: 2025-03-31 20:09:30.830290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7746c33ee5f0'
down_revision: Union[str, None] = 'bdfaa381e849'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
