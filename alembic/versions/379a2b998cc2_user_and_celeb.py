"""user and celeb

Revision ID: 379a2b998cc2
Revises: efcd3d1f51fa
Create Date: 2021-10-23 10:52:31.915572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '379a2b998cc2'
down_revision = 'efcd3d1f51fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('celebrity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('twitter_username', sa.String(length=100), nullable=False),
    sa.Column('twitter_id', sa.BigInteger(), nullable=True),
    sa.Column('twitter_name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('twitter_id'),
    sa.UniqueConstraint('twitter_username')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email_address', sa.String(length=120), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('celebrity')
    # ### end Alembic commands ###