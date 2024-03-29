"""empty message

Revision ID: 81c98a3e3dcc
Revises: bcb796111462
Create Date: 2023-03-13 11:57:35.348387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81c98a3e3dcc'
down_revision = 'bcb796111462'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('memo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('memo', schema=None) as batch_op:
        batch_op.drop_column('is_deleted')

    # ### end Alembic commands ###
