"""add unique constraint and index to ISBN column in books table

Revision ID: 442e00a4d839
Revises: 83e85133ceca
Create Date: 2023-07-15 20:57:55.197839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '442e00a4d839'
down_revision = '83e85133ceca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'books', ['ISBN'])
    op.create_index(op.f('ixs_books_ISBN'), 'books', ['ISBN'], unique=True)


def downgrade() -> None:
    op.drop_constraint(None, 'books', type_='unique')
    op.drop_index(op.f('ixs_books_ISBN'), table_name='books')