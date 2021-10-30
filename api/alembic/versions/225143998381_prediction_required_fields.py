"""prediction required fields

Revision ID: 225143998381
Revises: 93ef897d9487
Create Date: 2021-10-29 20:38:56.210317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '225143998381'
down_revision = '93ef897d9487'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('prediction', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('prediction', 'celebrity_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('prediction_result', 'prediction_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('prediction_result', 'prediction_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('prediction', 'celebrity_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('prediction', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
