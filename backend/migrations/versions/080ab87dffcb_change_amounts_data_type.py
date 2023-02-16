"""change_amounts_data_type

Revision ID: 080ab87dffcb
Revises: c42cf70d7f10
Create Date: 2023-02-11 23:48:31.004163

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '080ab87dffcb'
down_revision = 'c42cf70d7f10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("productshoppinglist", "amount_to_buy", type_=sa.DECIMAL(10, 4))
    op.alter_column("productshoppinglist", "amount_bought", type_=sa.DECIMAL(10, 4))


def downgrade() -> None:
    op.alter_column("productshoppinglist", "amount_to_buy", type_=sa.Integer())
    op.alter_column("productshoppinglist", "amount_bought", type_=sa.Integer())