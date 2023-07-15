"""create book_ratings table

Revision ID: 83e85133ceca
Revises: 8fa5254cdb22
Create Date: 2023-07-15 16:03:42.608428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83e85133ceca'
down_revision = '8fa5254cdb22'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create book_ratings table
    op.create_table(
        'book_ratings',
        sa.Column('rating_id', sa.String(50)),
        sa.Column('book_id', sa.String(50), sa.ForeignKey('books.book_id'), nullable=False),
        sa.Column('list_id', sa.String(50), sa.ForeignKey('reading_lists.list_id'), nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('notes', sa.String(500)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
        sa.PrimaryKeyConstraint("rating_id")
    )

def downgrade() -> None:
    op.drop_table('book_ratings')
