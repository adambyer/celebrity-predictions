"""celebrity - twitter_name is nullable

Revision ID: a62f6ebf35c1
Revises: 7be9a1a42e71
Create Date: 2021-10-17 17:46:18.955669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a62f6ebf35c1'
down_revision = '7be9a1a42e71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('celebrity', 'twitter_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('celebrity', 'twitter_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###