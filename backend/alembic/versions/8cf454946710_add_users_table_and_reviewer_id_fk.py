"""add users table and reviewer_id FK

Revision ID: 8cf454946710
Revises: d91265378ae2
Create Date: 2026-07-04 22:32:51.712834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cf454946710'
down_revision: Union[str, Sequence[str], None] = 'd91265378ae2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'reviewer', name='user_role'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # reviewer_id FK — use direct SQL to avoid batch mode reflection issues
    op.execute("PRAGMA foreign_keys=OFF")
    op.execute("""
        CREATE TABLE scores_new (
            id INTEGER NOT NULL PRIMARY KEY,
            candidate_id INTEGER NOT NULL REFERENCES candidates (id),
            category VARCHAR(255) NOT NULL,
            score INTEGER NOT NULL,
            reviewer_id INTEGER NOT NULL REFERENCES users (id),
            note TEXT,
            created_at DATETIME NOT NULL
        )
    """)
    op.execute("INSERT INTO scores_new SELECT id, candidate_id, category, score, reviewer_id, note, created_at FROM scores")
    op.execute("DROP TABLE scores")
    op.execute("ALTER TABLE scores_new RENAME TO scores")
    op.execute("CREATE INDEX ix_scores_candidate_id ON scores (candidate_id)")
    op.execute("CREATE INDEX ix_scores_reviewer_id ON scores (reviewer_id)")
    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_scores_reviewer_id")
    op.execute("DROP INDEX IF EXISTS ix_scores_candidate_id")
    op.execute("PRAGMA foreign_keys=OFF")
    op.execute("""
        CREATE TABLE scores_new (
            id INTEGER NOT NULL PRIMARY KEY,
            candidate_id INTEGER NOT NULL REFERENCES candidates (id),
            category VARCHAR(255) NOT NULL,
            score INTEGER NOT NULL,
            reviewer_id INTEGER NOT NULL,
            note TEXT,
            created_at DATETIME NOT NULL
        )
    """)
    op.execute("INSERT INTO scores_new SELECT id, candidate_id, category, score, reviewer_id, note, created_at FROM scores")
    op.execute("DROP TABLE scores")
    op.execute("ALTER TABLE scores_new RENAME TO scores")
    op.execute("PRAGMA foreign_keys=ON")

    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
