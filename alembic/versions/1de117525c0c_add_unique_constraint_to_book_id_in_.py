"""add unique constraint to book_id in reading_lists

Revision ID: 1de117525c0c
Revises: 442e00a4d839
Create Date: 2023-07-15 21:02:44.852214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1de117525c0c'
down_revision = '442e00a4d839'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'reading_lists', ['book_id'])


def downgrade() -> None:
    op.drop_constraint(None, 'reading_lists', type_='unique')
