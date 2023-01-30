"""add_completed_field

Revision ID: c42cf70d7f10
Revises: b33a82bea515
Create Date: 2023-01-30 15:19:24.670882

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'c42cf70d7f10'
down_revision = 'b33a82bea515'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('productshoppinglist', sa.Column("completed", sa.Boolean()))


def downgrade() -> None:
    op.drop_column('productshoppinglist', 'completed')
