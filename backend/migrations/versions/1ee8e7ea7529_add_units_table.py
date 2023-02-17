"""add_units_table

Revision ID: 1ee8e7ea7529
Revises: 080ab87dffcb
Create Date: 2023-02-13 22:49:58.707600

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '1ee8e7ea7529'
down_revision = '080ab87dffcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("unit",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=32), nullable=False),
                    sa.Column("precision", sa.Integer(), default=0, nullable=False),
                    sa.PrimaryKeyConstraint("id")
                    )
    op.execute("INSERT INTO public.unit (name, precision) VALUES ('kg', 3)")
    op.execute("INSERT INTO public.unit (name, precision) VALUES ('un', 0)")
    op.add_column('product', sa.Column('unit_id', sa.Integer(), sa.ForeignKey('unit.id')))


def downgrade() -> None:
    op.drop_column('unit_id', 'product')
    op.drop_table('unit')
