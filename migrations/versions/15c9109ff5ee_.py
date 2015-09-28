"""empty message

Revision ID: 15c9109ff5ee
Revises: 3aacee1d7e81
Create Date: 2015-09-28 17:10:01.785274

"""

# revision identifiers, used by Alembic.
revision = '15c9109ff5ee'
down_revision = '3aacee1d7e81'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link_list', sa.Column('admin_user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'link_list', 'user', ['admin_user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'link_list', type_='foreignkey')
    op.drop_column('link_list', 'admin_user_id')
    ### end Alembic commands ###
