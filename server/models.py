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


    serialize_rules = ('-user.players', '-game.players', '-chat_messages', '-user._password_hash')

class Game(db.Model, SerializerMixin):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    size = db.Column(db.Integer)
    round = db.Column(db.Integer)
    phase = db.Column(db.String)
    room_code = db.Column(db.String)
    percival = db.Column(db.Boolean)
    mordred = db.Column(db.Boolean)
    oberon = db.Column(db.Boolean)
    morgana = db.Column(db.Boolean)

    # relationships
    players = db.relationship('Player', back_populates = 'game')
    serialize_rules = ('-players.game', '-players.user._password_hash',)

class ChatMessage(db.Model, SerializerMixin):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    message = db.Column(db.String)
    time = db.Column(db.DateTime, server_default = db.func.now())

    player = db.relationship('Player', back_populates = 'chat_messages')
    
    serialize_only = ('player.user.username', 'player.user.id', 'player.game_id', 'message', 'time')