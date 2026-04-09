"""make subreddit_subscribers date & subscriber count unique together

Revision ID: b9d8f10d054c
Revises: 4cee33292083
Create Date: 2026-04-09 10:03:33.025797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9d8f10d054c'
down_revision: Union[str, Sequence[str], None] = '4cee33292083'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_subreddit_subscribers_subreddit_id_date",
        "subreddit_subscribers",
        ["subreddit_id", "date"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_subreddit_subscribers_subreddit_id_date",
        "subreddit_subscribers",
    )
