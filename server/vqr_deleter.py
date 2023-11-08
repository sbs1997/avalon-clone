#!/usr/bin/env python3

# Standard library imports
# from random import randint, choice as rc
import random

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Player, Game, Vote, Round, Quester, ChatMessage

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():

        games = Game.query.all()
        for game in games:
            game.phase = 'pregame'
            game.round = 0
            db.session.add(game)
        Vote.query.delete()
        Round.query.delete()
        Quester.query.delete()


        db.session.commit()