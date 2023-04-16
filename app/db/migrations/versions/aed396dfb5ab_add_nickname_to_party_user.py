"""Add nickname to Party User

Revision ID: aed396dfb5ab
Revises: c05656d1efc4
Create Date: 2023-02-24 22:01:23.201851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aed396dfb5ab'
down_revision = 'c05656d1efc4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('partyuser', sa.Column('nickname', sa.String(length=20), nullable=True))
    op.create_unique_constraint(None, 'partyuser', ['nickname'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'partyuser', type_='unique')
    op.drop_column('partyuser', 'nickname')
    # ### end Alembic commands ###
