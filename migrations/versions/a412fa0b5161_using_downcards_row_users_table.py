"""using downcards row users table

Revision ID: a412fa0b5161
Revises: 2dc71fd2a1f3
Create Date: 2020-04-13 16:12:16.113096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a412fa0b5161'
down_revision = '2dc71fd2a1f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('usingDownCards', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'usingDownCards')
    # ### end Alembic commands ###
