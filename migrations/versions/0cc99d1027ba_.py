"""empty message

Revision ID: 0cc99d1027ba
Revises: b2a226d215cb
Create Date: 2016-11-16 11:40:20.581000

"""

# revision identifiers, used by Alembic.
revision = '0cc99d1027ba'
down_revision = 'b2a226d215cb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###
