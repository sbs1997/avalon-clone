"""added a column for how many times the quest team vote has failed

Revision ID: 61cce5bb13ae
Revises: 524caf942fcf
Create Date: 2023-11-03 08:08:40.607106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61cce5bb13ae'
down_revision = '524caf942fcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rounds', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team_votes_failed', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rounds', schema=None) as batch_op:
        batch_op.drop_column('team_votes_failed')

    # ### end Alembic commands ###