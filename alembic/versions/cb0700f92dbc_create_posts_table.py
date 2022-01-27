"""create_posts_table

Revision ID: cb0700f92dbc
Revises: 
Create Date: 2022-01-26 21:55:51.322870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0700f92dbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer, nullable = False, primary_key = True), \
        sa.Column("title", sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
