"""empty message

Revision ID: 7bd8c2b048bc
Revises: dd4e30d8e85e
Create Date: 2020-03-18 16:46:45.468746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bd8c2b048bc'
down_revision = 'dd4e30d8e85e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mobile_recharge',
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('mobile_no', sa.String(length=50), nullable=False),
    sa.Column('topup_0_30', sa.String(length=20), nullable=True),
    sa.Column('topup_0_60', sa.String(length=20), nullable=True),
    sa.Column('topup_0_90', sa.String(length=20), nullable=True),
    sa.Column('topup_0_180', sa.String(length=20), nullable=True),
    sa.Column('topup_0_360', sa.String(length=20), nullable=True),
    sa.Column('topup_30_60', sa.String(length=20), nullable=True),
    sa.Column('topup_60_90', sa.String(length=20), nullable=True),
    sa.Column('topup_90_180', sa.String(length=20), nullable=True),
    sa.Column('topup_180_360', sa.String(length=20), nullable=True),
    sa.Column('topup_360_720', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('mobile_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mobile_recharge')
    # ### end Alembic commands ###
