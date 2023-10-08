"""fill theme_color

Revision ID: f1b65a093bdd
Revises: 83500922b6a0
Create Date: 2023-10-07 23:10:24.913775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1b65a093bdd"
down_revision: Union[str, None] = "83500922b6a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("settings") as batch_op:
        batch_op.drop_column("theme_color")
        batch_op.add_column(
            sa.Column("theme_color", sa.String(), server_default="lime")
        )


def downgrade() -> None:
    pass
