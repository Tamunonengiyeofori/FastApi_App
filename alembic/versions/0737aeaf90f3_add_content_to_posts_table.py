"""add content to posts table

Revision ID: 0737aeaf90f3
Revises: 53eda498cc46
Create Date: 2022-05-31 22:21:40.106034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0737aeaf90f3'
down_revision = '53eda498cc46'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
