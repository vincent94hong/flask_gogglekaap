"""Added label model

Revision ID: e0d3a4d6acfa
Revises: 81c98a3e3dcc
Create Date: 2023-03-13 12:39:10.229091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0d3a4d6acfa'
down_revision = '81c98a3e3dcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('label',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('content', 'user_id', name='uk_content_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('label')
    # ### end Alembic commands ###