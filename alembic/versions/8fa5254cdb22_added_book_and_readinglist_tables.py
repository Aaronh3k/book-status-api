"""Added Book and ReadingList tables

Revision ID: 8fa5254cdb22
Revises: 
Create Date: 2023-07-12 10:41:41.495694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fa5254cdb22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create book table
    op.create_table(
        'books',
        sa.Column('book_id', sa.String(50)),
        sa.Column('ISBN', sa.String(100), nullable=False, index=True, unique=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('author', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
        sa.PrimaryKeyConstraint("book_id")
    )

    # create reading list table
    op.create_table(
        'reading_lists',
        sa.Column('list_id', sa.String(50)),
        sa.Column('book_id', sa.String(50), sa.ForeignKey('books.book_id'), nullable=False),
        sa.Column('status', sa.String(20), default='unread', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
        sa.PrimaryKeyConstraint("list_id")
    )


def downgrade() -> None:
    op.drop_table('reading_lists')
    op.drop_table('books')
