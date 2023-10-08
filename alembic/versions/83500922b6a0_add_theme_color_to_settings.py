"""add theme_color to settings

Revision ID: 83500922b6a0
Revises: 0e8ad111d87b
Create Date: 2023-10-07 23:03:04.342869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83500922b6a0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("settings", sa.Column("theme_color", sa.String(), default="lime"))


def downgrade() -> None:
    pass
