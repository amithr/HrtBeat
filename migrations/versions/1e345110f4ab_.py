"""empty message

Revision ID: 1e345110f4ab
Revises: 1cff8aa5fbb5
Create Date: 2015-09-27 18:45:16.224354

"""

# revision identifiers, used by Alembic.
revision = '1e345110f4ab'
down_revision = '1cff8aa5fbb5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('linkLists_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('link_list_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['link_list_id'], ['link_list.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('linkLists_users')
    ### end Alembic commands ###
