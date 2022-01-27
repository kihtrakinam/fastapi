"""add content column to posts table

Revision ID: 6334336de7dc
Revises: cb0700f92dbc
Create Date: 2022-01-26 22:21:31.566459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6334336de7dc'
down_revision = 'cb0700f92dbc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable = False))


def downgrade():
    op.drop_column("posts", "content")
