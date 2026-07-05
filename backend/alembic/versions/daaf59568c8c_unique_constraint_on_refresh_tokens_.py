"""unique constraint on refresh_tokens.user_id

Revision ID: daaf59568c8c
Revises: 6ff1b6db3214
Create Date: 2026-07-05 17:56:02.810337

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'daaf59568c8c'
down_revision: Union[str, Sequence[str], None] = '6ff1b6db3214'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Unique index is equivalent to unique constraint in SQLite —
    # avoids batch_alter_table FK reflection issues
    op.execute("CREATE UNIQUE INDEX uq_refresh_tokens_user_id ON refresh_tokens (user_id)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_refresh_tokens_user_id")
