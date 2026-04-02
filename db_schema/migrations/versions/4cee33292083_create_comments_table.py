"""create comments table

Revision ID: 4cee33292083
Revises: e8634ce86cd5
Create Date: 2026-04-02 11:52:31.547381

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4cee33292083"
down_revision: Union[str, Sequence[str], None] = "e8634ce86cd5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.TEXT, primary_key=True),
        sa.Column(
            "thread_id", sa.TEXT, sa.ForeignKey("threads.id", ondelete="CASCADE")
        ),
        sa.Column("text", sa.TEXT),
        sa.Column("author", sa.TEXT),
        sa.Column("permalink", sa.TEXT),
        sa.Column("upvotes", sa.Integer),
        sa.Column("downvotes", sa.Integer),
        sa.Column("created_date", sa.Date),
    )


def downgrade() -> None:
    op.drop_table("comments")
