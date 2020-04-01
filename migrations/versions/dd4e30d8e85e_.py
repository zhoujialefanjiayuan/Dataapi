"""empty message

Revision ID: dd4e30d8e85e
Revises: 3da6782e74bf
Create Date: 2020-03-17 15:46:05.555950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd4e30d8e85e'
down_revision = '3da6782e74bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mobile_auth',
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('mobile_no', sa.String(length=50), nullable=False),
    sa.Column('isauth', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('mobile_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mobile_auth')
    # ### end Alembic commands ###
