"""initial config

Revision ID: 1aa0fc063351
Revises: 
Create Date: 2022-12-27 03:28:13.045290

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '1aa0fc063351'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('product',
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shoppinglist',
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=16), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=320), nullable=False),
        sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
        sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('password', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table('productshoppinglist',
        sa.Column('shopping_list_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('amount_to_buy', sa.Integer(), nullable=True),
        sa.Column('amount_bought', sa.Integer(), nullable=True),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(['shopping_list_id'], ['shoppinglist.id'], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint('product_id', "shopping_list_id")
    )


def downgrade() -> None:
    op.drop_table('productshoppinglist')
    op.drop_table('user')
    op.drop_table('shoppinglist')
    op.drop_table('product')
