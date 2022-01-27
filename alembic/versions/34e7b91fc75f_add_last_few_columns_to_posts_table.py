"""add last few columns to posts table

Revision ID: 34e7b91fc75f
Revises: 971e8d49aab6
Create Date: 2022-01-26 22:44:13.567677

"""
from http import server
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34e7b91fc75f'
down_revision = '971e8d49aab6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable = False, server_default = "False"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone = True), server_default = sa.text("now()"), nullable = False))


def downgrade():
    op.drop_column(table_name = "posts", column_name = "published")
    op.drop_column(table_name = "posts", column_name = "created_at")
