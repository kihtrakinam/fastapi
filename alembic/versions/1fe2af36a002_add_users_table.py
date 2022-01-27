"""add users table

Revision ID: 1fe2af36a002
Revises: 6334336de7dc
Create Date: 2022-01-26 22:28:10.997137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fe2af36a002'
down_revision = '6334336de7dc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
    sa.Column("id", sa.Integer, nullable = False),
    sa.Column("email", sa.String, nullable = False),
    sa.Column("password", sa.String, nullable = False),
    sa.Column("created_at", sa.TIMESTAMP(timezone = True), server_default = sa.text("now()"), nullable = False),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("email")
    )


def downgrade():
    op.drop_table("users")
