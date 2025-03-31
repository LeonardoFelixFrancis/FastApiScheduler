"""Created authentication

Revision ID: bdfaa381e849
Revises: a87d484b41b7
Create Date: 2025-03-19 20:30:01.323379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdfaa381e849'
down_revision: Union[str, None] = 'a87d484b41b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
