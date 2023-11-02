#!/usr/bin/env python3
from flask import request, session, make_response
from flask_restful import Resource
from config import app, db, api, socket_io, random
from models import User, Player, Game, ChatMessage
from flask_socketio import join_room, leave_room


# takes the user and game id and returns the info for the game that the user should have
def game_info(game_id, user_id):
    game = Game.query.filter(Game.id == game_id).first()
    player = Player.query.filter(Player.game_id == game_id).filter(Player.user_id == user_id).first()
    response_game = game.to_dict(only=('id', 'title', 'size', 'round', 'phase', 'room_code', 'percival', 'mordred', 'oberon', 'morgana', 'players.user.username', 'players.user.id', 'players.leader', 'players.id'))
    if not player:
        response_game["role"] = 'imposter'
    else:
        # if not player.role:
        #     response_game["role"] = None
        if player.role == "good":
            pass
        if player.role == 'evil' or player.role == 'merlin' or player.role == 'assassin':
            evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(Player.role == "evil").all()]
            response_game['baddies'] = evil_players
        response_game["role"] = player.role
        if player.owner:
            response_game["owner"] = True
    return response_game

# gets the info that needs to be sent out at the beginning of the quest team building phase
def quest_team_info(game):
    game.phase = 'team_building'
    game.round = game.round+1
    quest_size_dict = {
        5 : [2,3,2,3,3],
        6 : [2,3,4,3,4],
        7 : [2,3,3,4,4],
        8 : [3,4,4,5,5],
        9 : [3,4,4,5,5],
        10: [3,4,4,5,5]
    }
    return quest_size_dict[game.size][game.round-1]

####################### SOCKET STUFF #########################

@socket_io.on('connect')
def handle_connect():
    print('new connection')
    # print(request.sid)
    # session["user"] = request.sid

# client sends a message, add that message to the DB and emit the message to everyone in the same room
@socket_io.on('client-message')
def chat_message(playerID, message, room):
    # print(playerID)
    new_message = ChatMessage(player_id = playerID, message = message)
    db.session.add(new_message)
    # print(new_message.to_dict())
    db.session.commit()
    # print(new_message.to_dict())
    
    socket_io.emit('server-message', new_message.to_dict(), room = room)
    
# listen for client request to be set to a room
@socket_io.on('set-room')
def change_room(game_id, user_id, socket_id):
    # print(socket_id)
    room = f'game{game_id}'
    join_room(room)

    socket_io.emit('update-game', game_info(game_id, user_id), room = socket_id)


# listen for client request to be added to a game
@socket_io.on('join-game')
def add_player(player_info):
    # print(player_info)
    try:
        new_player = Player(
            user_id = player_info['userID'],
            game_id = player_info['gameID'],
            role = None,
            owner = False,
            winner = False
        )
        db.session.add(new_player)
        db.session.commit()

        socket_io.emit('update-game', game_info(new_player.game_id, new_player.user_id), room = player_info['socketID'])

        players = [p.to_dict() for p in Player.query.filter(Player.game_id == player_info['gameID']).all()]
        # print(players)

        socket_io.emit('player-change', players)

    except ValueError:
        socket_io.emit('join-error')

# listen for client request to leave game
@socket_io.on('leave-game')
def remove_player(game_id, user_id, sender_socket):
    player = Player.query.filter(Player.user_id == user_id).filter(Player.game_id == game_id).first()

    db.session.delete(player)
    db.session.commit()

    # send the client the new game info that they should have
    socket_io.emit('update-game', game_info(game_id, user_id), room = sender_socket)

    # send the other players in the game the new player list
    players = [p.to_dict() for p in Player.query.filter(Player.game_id == game_id).all()]
    # print(players)

    socket_io.emit('player-change', players, room=f'game{game_id}')

# listen for requests from a client for messages in a room
@socket_io.on('message-request')
def messages_by_game_id(game_id, socket_id):
    messages = [m.to_dict() for m in ChatMessage.query.join(Player).filter(Player.game_id == game_id).all()]
    socket_io.emit('messages-fetched', messages, room = socket_id)


# START THE GAME! EXCITING!
@socket_io.on('start-game')
def start_game(game_id):
    game = Game.query.filter(Game.id==game_id)
    
    # number of evil players in a game based on total size
    evil_size_dict = {
        5 : 2,
        6 : 2,
        7 : 3,
        8 : 3,
        9 : 3,
        10: 4,
    }

    # 
    # assign roles
    # first get/set the size of the game:
    game.size=len(game.players)

    # set all the players roles to good and then add them to our list of good players
    good_players = []
    for player in game.players:
        player.role = 'good'
        good_players.append(player)

    for i in range(evil_size_dict[game.size]):
        baddie = random.choice(good_players)
        if i == 0:
            baddie.role == 'assassin'
        else:
            baddie.role == 'evil'
        good_players.remove(baddie)
    
    



    game.round = 1
    game.phase


@socket_io.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")



######################### ROUTES!!!!! ##########################
@app.route('/')
def index():
    return '<h1>Avalon Server!</h1>'

######################## USER ROUTES ###########################


class UserById(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        return make_response(user.to_dict(), 200)
    
    def patch(self, id):
        user = User.query.filter(User.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(user, field, data[field])
            db.session.add(user)
            db.session.commit()
            
            return make_response(user.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        db.session.delete(user)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(UserById, '/users/<int:id>')
    
class Users(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_user = User(
                username = data.get("username"),
                _password_hash = data.get("password")
            )
            db.session.add(new_user)
            db.session.commit()
        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Users, '/users')

class PlayersByUser(Resource):
    def get(self, user_id):
        players = [p.to_dict() for p in Player.query.filter(Player.user_id == user_id).all()]
        make_response(players, 200)

api.add_resource(PlayersByUser, '/users/<int:id>/players')


####################### Games routes ######################
class GameById(Resource):
    def get(self, id):
        game = Game.query.filter(Game.id == id).first()
        if not game:
            return make_response(({"error": "game not found"}),404)
        return make_response(game.to_dict(), 200)
    
    def patch(self, id):
        game = Game.query.filter(Game.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(game, field, data[field])
            db.session.add(game)
            db.session.commit()
            
            return make_response(game.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        game = Game.query.filter(Game.id == id).first()
        db.session.delete(game)
        db.session.commit()

        return make_response({}, 204)

api.add_resource(GameById, '/games/<int:id>')


class Games(Resource):
    def get (self):
        games = [g.to_dict() for g in Game.query.all()]
        return make_response(games, 200)
    
    def post(self):
        data = request.get_json()

        try:
            new_game = Game(
                size = data.get("size"),
                round = 0,
                phase = "pregame",
                room_code = data.get('roomCode'),
                percival = data.get('percival'),
                mordred = data.get('mordred'),
                oberon = data.get('oberon'),
                morgana = data.get('morgana')
            )
            db.session.add(new_game)
            db.session.commit()
        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Games, '/games')

# class PlayersByGame(Resource):
#     def get(self, game_id):
#         players = [p.to_dict() for p in Player.query.filter(Player.game_id == game_id).all()]
#         make_response(players, 200)

# api.add_resource(PlayersByGame, '/games/<int:id>/players')

class GameForPlayer(Resource):
    def get(self, game_id, user_id):
        game = Game.query.filter(Game.id == game_id).first()
        player = Player.query.filter(Player.game_id == game_id).filter(Player.user_id == user_id).first()
        response_game = game.to_dict(only=('id', 'title', 'size', 'round', 'phase', 'room_code', 'percival', 'mordred', 'oberon', 'morgana', 'players.user.username', 'players.user.id', 'players.leader', 'players.id'))
        if not player:
            response_game["role"] = 'imposter'
        else:
            if player.role == "good":
                pass
            if player.role == 'evil' or player.role == 'merlin':
                evil_players = [p.user_id for p in Player.query.filter(Player.game_id == game_id).filter(Player.role == "evil").all()]
                response_game['evils'] = evil_players
            response_game["role"] = player.role
            if player.owner:
                response_game["owner"] = True
        return make_response(response_game, 200)
    
api.add_resource(GameForPlayer, '/games/<int:game_id>/<int:user_id>')


######################################## player routes ############################################

class PlayerById(Resource):
    def get(self, id):
        player = Player.query.filter(Player.id == id).first()
        return make_response(player.to_dict(), 200)
    
    def patch(self, id):
        player = Player.query.filter(Player.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(player, field, data[field])
            db.session.add(player)
            db.session.commit()
            
            return make_response(player.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        player = Player.query.filter(Player.id == id).first()
        db.session.delete(player)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(PlayerById, '/players/<int:id>')


class Players(Resource):
    def post(self):
        data = request.get_json()

        try:
            new_player = Player(
                user_id = data.get('userID'),
                game_id = data.get('gameID'),
                role = data.get('role'),
                owner = data.get('owner'),
                winner = False
            )
            db.session.add(new_player)
            db.session.commit()

            return make_response(new_player.to_dict(), 201)

        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Players, '/players')



################################ Chat Messages ###########################

class MessageById(Resource):
    def get(self, id):
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        return make_response(message.to_dict(), 200)
    
    def patch(self, id):
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        data = request.get_json()
        try:
            for field in data:
                setattr(message, field, data[field])
            db.session.add(message)
            db.session.commit()
            
            return make_response(message.to_dict(), 202)
        except ValueError as e:
            print(e.str())
            return make_response(({"error": ["validation errors"]}), 406)
    def delete(self, id):
        message = ChatMessage.query.filter(ChatMessage.id == id).first()
        db.session.delete(message)
        db.session.commit()

        return make_response({}, 204)
    
api.add_resource(MessageById, '/messages/<int:id>')


class Messages(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_message = ChatMessage(
                player_id = data.get('playerID'),
                message = data.get('message')
            )
            db.session.add(new_message)
            db.session.commit()
            return make_response(new_message.to_dict(), 201)
        
        except ValueError:
            return make_response({"error": ["validation errors"]},406)
        
api.add_resource(Messages, '/messages')


class MessagesByRoom(Resource):
    def get(self, id):
        messages = [m.to_dict() for m in ChatMessage.query.join(Player).filter(Player.game_id == id).all()]
        return make_response(messages, 200)

api.add_resource(MessagesByRoom, '/messages/game/<int:id>')


########################################### log in stuff #######################################
class Login(Resource):
    def post(self):
        data = request.get_json()
        username= data['username']
        password= data['password']
        user = User.query.filter(User.username == username).first()
        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
            else:
                return {"Error": "password is wrong"}, 401
        return {"Error": "User doesn't exist"}, 401

api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict(only=('username', 'id'))
        else:
            return {'message': 'Not Authorized'}, 401
        
api.add_resource(CheckSession, '/check_session')


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204
    
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    # app.run(port=5555, debug=True)
    socket_io.run(app, port=5555)