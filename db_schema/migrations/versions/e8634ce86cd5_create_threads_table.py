"""create threads table

Revision ID: e8634ce86cd5
Revises: 820e94dbaa4c
Create Date: 2026-04-02 11:52:10.865180

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e8634ce86cd5"
down_revision: Union[str, Sequence[str], None] = "820e94dbaa4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "threads",
        sa.Column("id", sa.TEXT, primary_key=True),
        sa.Column("title", sa.TEXT),
        sa.Column("text", sa.TEXT),
        sa.Column("author", sa.TEXT),
        sa.Column("permalink", sa.TEXT),
        sa.Column("comments", sa.Integer),
        sa.Column("upvotes", sa.Integer),
        sa.Column("downvotes", sa.Integer),
        sa.Column(
            "subreddit", sa.TEXT, sa.ForeignKey("subreddits.id", ondelete="CASCADE")
        ),
        sa.Column("created_date", sa.Date),
    )


def downgrade() -> None:
    op.drop_table("threads")
