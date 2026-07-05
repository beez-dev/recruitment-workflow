"""rename refresh_tokens.token to token_hash

Revision ID: 6ff1b6db3214
Revises: a9570e567fb8
Create Date: 2026-07-05 17:23:11.262554

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '6ff1b6db3214'
down_revision: Union[str, Sequence[str], None] = 'a9570e567fb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite 3.25+ supports RENAME COLUMN natively — avoids batch mode FK reflection issues
    op.execute("ALTER TABLE refresh_tokens RENAME COLUMN token TO token_hash")
    op.execute("DROP INDEX IF EXISTS ix_refresh_tokens_token")
    op.execute("CREATE UNIQUE INDEX ix_refresh_tokens_token_hash ON refresh_tokens (token_hash)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_refresh_tokens_token_hash")
    op.execute("ALTER TABLE refresh_tokens RENAME COLUMN token_hash TO token")
    op.execute("CREATE UNIQUE INDEX ix_refresh_tokens_token ON refresh_tokens (token)")
