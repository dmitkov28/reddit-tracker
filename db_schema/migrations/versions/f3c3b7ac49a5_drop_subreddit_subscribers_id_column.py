"""drop subreddit_subscribers id column

Revision ID: f3c3b7ac49a5
Revises: 0ca04725c77c
Create Date: 2026-04-09 11:12:42.270156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3c3b7ac49a5'
down_revision: Union[str, Sequence[str], None] = '0ca04725c77c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("subreddit_subscribers_pkey", "subreddit_subscribers", type_="primary")
    op.drop_column("subreddit_subscribers", "id")
    op.drop_constraint("uq_subreddit_subscribers_subreddit_id_date", "subreddit_subscribers")
    op.create_primary_key("subreddit_subscribers_pkey", "subreddit_subscribers", ["subreddit_id", "date"])


def downgrade() -> None:
    op.drop_constraint("subreddit_subscribers_pkey", "subreddit_subscribers", type_="primary")
    op.add_column("subreddit_subscribers", sa.Column("id", sa.Integer, autoincrement=True))
    op.create_primary_key("subreddit_subscribers_pkey", "subreddit_subscribers", ["id"])
    op.create_unique_constraint("uq_subreddit_subscribers_subreddit_id_date", "subreddit_subscribers", ["subreddit_id", "date"])
