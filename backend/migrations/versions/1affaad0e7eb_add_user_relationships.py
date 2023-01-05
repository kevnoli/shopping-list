"""add_user_relationships

Revision ID: 1affaad0e7eb
Revises: 1aa0fc063351
Create Date: 2023-01-04 22:35:10.621176

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '1affaad0e7eb'
down_revision = '1aa0fc063351'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('usershoppinglist',
        sa.Column('shopping_list_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('owner', sa.Boolean(), default=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(['shopping_list_id'], ['shoppinglist.id'], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint('user_id', 'shopping_list_id')
    )


def downgrade() -> None:
    op.drop_table('usershoppinglist')
