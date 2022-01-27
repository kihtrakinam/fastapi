"""add foreign key to post table

Revision ID: 971e8d49aab6
Revises: 1fe2af36a002
Create Date: 2022-01-26 22:35:28.501142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '971e8d49aab6'
down_revision = '1fe2af36a002'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable = False))
    op.create_foreign_key(constraint_name = "posts_users_fkey", source_table = "posts", referent_table = "users",\
         local_cols = ["user_id"], remote_cols = ["id"], ondelete = "RESTRICT", onupdate = "CASCADE")


def downgrade():
    op.drop_constraint(constraint_name = "posts_users_fkey", table_name = "posts")
    op.drop_column(table_name = "posts", column_name = "user_id")
