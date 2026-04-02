"""create subreddit_subscribers table

Revision ID: 820e94dbaa4c
Revises: 5f617c9b0ca7
Create Date: 2026-04-02 11:51:37.632993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "820e94dbaa4c"
down_revision: Union[str, Sequence[str], None] = "5f617c9b0ca7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subreddit_subscribers",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "subreddit_id", sa.Text, sa.ForeignKey("subreddits.id", ondelete="CASCADE")
        ),
        sa.Column("subscriber_count", sa.Integer),
        sa.Column("date", sa.Date, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("subreddit_subscribers")
