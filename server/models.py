from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True)
    _password_hash = db.Column(db.String, nullable = False)

    # relationships
    players = db.relationship('Player', back_populates = 'user')

    #password code
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8')
        )
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )
    
class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    # can either be "good", "evil", "merlin"
    role = db.Column(db.String)
    leader = db.Column(db.Boolean)
    owner = db.Column(db.Boolean)
    winner = db.Column(db.Boolean)

    # relationships
    user = db.relationship('User', back_populates = 'players')
    game = db.relationship('Game', back_populates = 'players')
    chat_messages = db.relationship('ChatMessage', back_populates = 'player')
    votes = db.relationship("Vote", back_populates = 'player')
    questers = db.relationship("Quester", back_populates = 'player')


    serialize_rules = ('-user.players', '-game.players', '-chat_messages', '-user._password_hash')

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    size = db.Column(db.Integer)
    round = db.Column(db.Integer)
    phase = db.Column(db.String)
    # options are "pregame", "team_building", "qt_voting" "quest_voting"
    room_code = db.Column(db.String)
    percival = db.Column(db.Boolean)
    mordred = db.Column(db.Boolean)
    oberon = db.Column(db.Boolean)
    morgana = db.Column(db.Boolean)

    # relationships
    players = db.relationship('Player', back_populates = 'game')
    rounds = db.relationship('Round', back_populates = 'game')

    serialize_rules = ('-players.game', '-players.user._password_hash', '-rounds.game', '-players.votes')

class ChatMessage(db.Model, SerializerMixin):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    message = db.Column(db.String)
    time = db.Column(db.DateTime, server_default = db.func.now())

    player = db.relationship('Player', back_populates = 'chat_messages')
    
    serialize_only = ('player.user.username', 'player.user.id', 'player.game_id', 'message', 'time')

class Round(db.Model, SerializerMixin):
    __tablename__ = 'rounds'

    id = db.Column(db.Integer, primary_key = True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    number = db.Column(db.Integer)
    quest_size = db.Column(db.Integer)
    winner = db.Column(db.String)
    team_votes_failed = db.Column(db.Integer)
    last_votes_for = db.Column(db.Integer)

    game = db.relationship('Game', back_populates = 'rounds')
    votes = db.relationship('Vote', back_populates = 'round', cascade="all, delete")
    questers = db.relationship('Quester', back_populates = 'round', cascade="all, delete")

    serialize_only = ('number', 'quest_size', 'winner', 'team_votes_failed', 'questers.player.user.id', 'questers.player.user.username', 'last_votes_for')

class Vote(db.Model, SerializerMixin):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'))
    # types are "team" or "success"
    vote_type = db.Column(db.String)
    voted_for = db.Column(db.Boolean)

    player = db.relationship('Player', back_populates = "votes")
    round = db.relationship('Round', back_populates = 'votes')

    serialize_rules = ('-player.votes', )

class Quester(db.Model, SerializerMixin):
    __tablename__ = 'questers'

    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.id'))

    player = db.relationship('Player', back_populates = "questers")
    round = db.relationship('Round', back_populates = 'questers')

    serialize_only = ('player.user.username', 'player.user.id', 'id', 'player.leader')


