"""change subreddit_subscribers primary key id

Revision ID: 7509be5e0c53
Revises: b9d8f10d054c
Create Date: 2026-04-09 10:34:20.062542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7509be5e0c53'
down_revision: Union[str, Sequence[str], None] = 'b9d8f10d054c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE subreddit_subscribers
        ALTER COLUMN id DROP DEFAULT,
        ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE subreddit_subscribers
        ALTER COLUMN id DROP IDENTITY,
        ALTER COLUMN id SET DEFAULT nextval('subreddit_subscribers_id_seq')
    """)
