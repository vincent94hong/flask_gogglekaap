"""Added new field to memo model

Revision ID: bcb796111462
Revises: 6120a5980724
Create Date: 2023-03-13 10:41:07.286343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcb796111462'
down_revision = '6120a5980724'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('memo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('linked_image', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('memo', schema=None) as batch_op:
        batch_op.drop_column('linked_image')

    # ### end Alembic commands ###
