"""create_unaccent_extension

Revision ID: b33a82bea515
Revises: 1affaad0e7eb
Create Date: 2023-01-25 11:16:13.152818

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'b33a82bea515'
down_revision = '1affaad0e7eb'
branch_labels = None
depends_on = None


def upgrade() -> None:    
    op.execute("CREATE EXTENSION unaccent")


def downgrade() -> None:    
    op.execute("DROP EXTENSION unaccent")
