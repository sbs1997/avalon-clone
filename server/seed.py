#!/usr/bin/env python3

# Standard library imports
# from random import randint, choice as rc
import random

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Player, Game, ChatMessage

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        
        print('Users')
        def create_users():
            users = []
            for i in range(20):
                new_user = User(
                    username = fake.first_name(),
                    password_hash = '1234'
                    )
                users.append(new_user)
            return users
        
        print("Games")
        def create_games():
            games=[]
            for i in range(5):
                new_game = Game(
                    size = 5,
                    round = 0,
                    phase = "pregame",
                    room_code = fake.word(),
                    percival = False,
                    mordred = False,
                    oberon = False,
                    morgana = False
                )
                games.append(new_game)
            return games
        
        print('Players')
        def create_players():
            players = []
            for i in range(5):
                for j in range (5):
                    random_num = random.randint(1,15)
                    new_player = Player(
                        user_id = random_num+j,
                        game_id = i+1,
                        owner = j == 0,
                        winner = False
                    )
                    players.append(new_player)
            return players
        
        User.query.delete()
        Game.query.delete()
        Player.query.delete()

        users = create_users()
        players = create_players()
        games = create_games()
        
        db.session.add_all(users)
        db.session.add_all(players)
        db.session.add_all(games)

        db.session.commit()
