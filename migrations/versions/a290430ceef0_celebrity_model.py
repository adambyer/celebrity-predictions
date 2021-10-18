"""celebrity model

Revision ID: a290430ceef0
Revises: b72ff442d5b7
Create Date: 2021-10-17 17:26:51.542094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a290430ceef0'
down_revision = 'b72ff442d5b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('celebrity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('twitter_id', sa.Integer(), nullable=False),
    sa.Column('twitter_username', sa.String(length=100), nullable=False),
    sa.Column('twitter_name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('twitter_id'),
    sa.UniqueConstraint('twitter_username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('celebrity')
    # ### end Alembic commands ###
