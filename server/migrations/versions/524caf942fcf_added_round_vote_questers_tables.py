"""added round vote questers tables

Revision ID: 524caf942fcf
Revises: 1f7d6825647a
Create Date: 2023-11-02 16:22:30.233783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524caf942fcf'
down_revision = '1f7d6825647a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('quest_size', sa.Integer(), nullable=True),
    sa.Column('successful_quest', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], name=op.f('fk_rounds_game_id_games')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rounds'))
    )
    op.create_table('questers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('round_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], name=op.f('fk_questers_player_id_players')),
    sa.ForeignKeyConstraint(['round_id'], ['rounds.id'], name=op.f('fk_questers_round_id_rounds')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_questers'))
    )
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('round_id', sa.Integer(), nullable=True),
    sa.Column('vote_type', sa.String(), nullable=True),
    sa.Column('voted_for', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], name=op.f('fk_votes_player_id_players')),
    sa.ForeignKeyConstraint(['round_id'], ['rounds.id'], name=op.f('fk_votes_round_id_rounds')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_votes'))
    )
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_column('round')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('round', sa.INTEGER(), nullable=True))

    op.drop_table('votes')
    op.drop_table('questers')
    op.drop_table('rounds')
    # ### end Alembic commands ###
