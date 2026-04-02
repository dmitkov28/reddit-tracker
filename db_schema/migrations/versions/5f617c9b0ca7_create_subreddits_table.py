"""create subreddits table

Revision ID: 5f617c9b0ca7
Revises:
Create Date: 2026-04-02 11:50:40.682689

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f617c9b0ca7"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subreddits",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("name", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("subreddits")