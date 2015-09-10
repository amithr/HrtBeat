"""empty message

Revision ID: 218a0d9e0be0
Revises: 2a1c8dce1bbd
Create Date: 2015-09-10 11:42:15.168150

"""

# revision identifiers, used by Alembic.
revision = '218a0d9e0be0'
down_revision = '2a1c8dce1bbd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('connection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.String(length=255), nullable=True),
    sa.Column('provider_user_id', sa.String(length=255), nullable=True),
    sa.Column('access_token', sa.String(length=255), nullable=True),
    sa.Column('secret', sa.String(length=255), nullable=True),
    sa.Column('display_name', sa.String(length=255), nullable=True),
    sa.Column('profile_url', sa.String(length=512), nullable=True),
    sa.Column('image_url', sa.String(length=512), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('connection')
    ### end Alembic commands ###
