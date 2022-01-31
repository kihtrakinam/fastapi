"""adding default value as empty string to phone number

Revision ID: c45cae9073a9
Revises: 643975186d84
Create Date: 2022-01-28 08:38:04.943283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45cae9073a9'
down_revision = '643975186d84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", column_name = "phone_number", server_default = "", nullable = False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", column_name = "phone_number", server_default = False, nullable = True)
    # ### end Alembic commands ###