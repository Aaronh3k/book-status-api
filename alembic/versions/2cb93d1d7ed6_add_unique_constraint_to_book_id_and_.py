"""add unique constraint to book_id and list_id in book_ratings

Revision ID: 2cb93d1d7ed6
Revises: 1de117525c0c
Create Date: 2023-07-16 08:24:51.938594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cb93d1d7ed6'
down_revision = '1de117525c0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_book_list', 'book_ratings', ['book_id', 'list_id'])


def downgrade() -> None:
    op.drop_constraint('uq_book_list', 'book_ratings', type_='unique')
